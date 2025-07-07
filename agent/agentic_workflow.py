from utils.model_loader import ModelLoader
from utils.config_loader import ConfigLoader
from prompt_library.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool

class GraphBuilder():
    def __init__(self):
        # Initialize config loader and model loader as per your definition
        self.config_loader = ConfigLoader()
        self.model_loader = ModelLoader(self.config_loader)
        
        # Load the Groq model
        self.groq_client = self.model_loader.get_model()
        self.model_name = self.model_loader.model_name
        
        self.tools = []
        
        self.weather_tools = WeatherInfoTool()
        self.place_search_tools = PlaceSearchTool()
        self.calculator_tools = CalculatorTool()
        self.currency_converter_tools = CurrencyConverterTool()
        
        self.tools.extend([* self.weather_tools.weather_tool_list, 
                           * self.place_search_tools.place_search_tool_list,
                           * self.calculator_tools.calculator_tool_list,
                           * self.currency_converter_tools.currency_converter_tool_list])
        
        # Note: Since Groq doesn't directly support tool binding like LangChain models,
        # we'll handle tool calls in the agent function
        
        self.graph = None
        
        self.system_prompt = SYSTEM_PROMPT
    
    
    def agent_function(self, state: MessagesState):
        """Main agent function using Groq model"""
        user_messages = state["messages"]
        
        # Prepare the conversation with system prompt
        conversation = []
        
        # Add system prompt
        conversation.append({"role": "system", "content": self.system_prompt})
        
        # Add user messages
        for message in user_messages:
            if hasattr(message, 'content'):
                role = "user" if message.type == "human" else "assistant"
                conversation.append({"role": role, "content": message.content})
            else:
                conversation.append({"role": "user", "content": str(message)})
        
        try:
            # Use the Groq client to generate response
            response = self.groq_client.chat.completions.create(
                model=self.model_name,
                messages=conversation,
                max_tokens=1000,
                temperature=0.7
            )
            
            response_content = response.choices[0].message.content
            
            # Create a response message compatible with LangGraph
            from langchain_core.messages import AIMessage
            ai_message = AIMessage(content=response_content)
            
            return {"messages": [ai_message]}
            
        except Exception as e:
            # Handle errors gracefully
            from langchain_core.messages import AIMessage
            error_message = AIMessage(content=f"Error generating response: {str(e)}")
            return {"messages": [error_message]}
    
    def build_graph(self):
        graph_builder = StateGraph(MessagesState)
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)
        self.graph = graph_builder.compile()
        return self.graph
        
    def __call__(self):
        return self.build_graph()