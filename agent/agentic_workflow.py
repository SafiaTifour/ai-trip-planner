from utils.model_loader import ModelLoader
from utils.config_loader import ConfigLoader
from langgraph.graph import StateGraph, MessagesState, END, START
from langgraph.prebuilt import ToolNode, tools_condition
from tools.weather_info_tool import WeatherInfoTool
from tools.place_search_tool import PlaceSearchTool
from tools.expense_calculator_tool import CalculatorTool
from tools.currency_conversion_tool import CurrencyConverterTool
from tools.arithmetic_opr_tool import multiply, add
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from prompt_library.prompt import TRAVEL_AGENT_SYSTEM_PROMPT


class AgenticWorkflow:
    def __init__(self):
        load_dotenv()
        
        
        self.config_loader = ConfigLoader()
        self.model_loader = ModelLoader(self.config_loader)
        
        
        self.model_loader.load_model()
        
    
        self.llm = ChatGroq(
            model=self.model_loader.model_name,  
            temperature=0.1,
            api_key=os.environ.get("GROQ_API_KEY"),
            max_tokens=1000
        )
        
        
        self.tools = self._setup_tools()
        
       
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        self.graph = self._build_graph()
    
    def _setup_tools(self) -> List:
        """Setup all available tools"""
        tools = []
        
        tools.extend([multiply, add])

        currency_tool = CurrencyConverterTool()
        tools.extend(currency_tool.get_tools())
        

        place_tool = PlaceSearchTool()
        tools.extend(place_tool.place_search_tool_list)
        
        weather_tool = WeatherInfoTool()
        tools.extend(weather_tool.weather_tool_list)
        
        return tools
    
    def agent_function(self, state: MessagesState) -> Dict[str, Any]:
        """Agent function that processes messages and decides on tool usage"""
        messages = state['messages']
        
       
        if not messages or not any(TRAVEL_AGENT_SYSTEM_PROMPT in str(msg.content) for msg in messages):
            system_msg = SystemMessage(content=TRAVEL_AGENT_SYSTEM_PROMPT)
            messages = [system_msg] + messages

        response = self.llm_with_tools.invoke(messages)

        return {"messages": [response]}
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        # Create the state graph
        graph_builder = StateGraph(MessagesState)
        
        # Add nodes
        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        
        # Add edges
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)
        
        # Compile and return the graph
        self.graph = graph_builder.compile()
        return self.graph
    
    def run(self, user_input: str) -> str:
        """Run the agentic workflow with user input"""
        try:
            initial_state = {
                "messages": [HumanMessage(content=user_input)]
            }
            
           
            result = self.graph.invoke(initial_state)

            final_message = result['messages'][-1]
            
            if isinstance(final_message, AIMessage):
                return final_message.content
            else:
                return str(final_message)
                
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    def stream_run(self, user_input: str):
        """Stream the agentic workflow execution"""
        try:
            
            initial_state = {
                "messages": [HumanMessage(content=user_input)]
            }
           
            for chunk in self.graph.stream(initial_state):
                yield chunk
                
        except Exception as e:
            yield {"error": f"Error processing request: {str(e)}"}
    
    def generate_direct_response(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generate a direct response using the ModelLoader (bypassing tools)"""
        try:
            return self.model_loader.generate_response(prompt, max_tokens, temperature)
        except Exception as e:
            return f"Error generating direct response: {str(e)}"


# Example usage and testing
if __name__ == "__main__":
    # Initialize the workflow
    workflow = AgenticWorkflow()
    
    # Test cases for travel planning
    test_cases = [
        "Plan a 3-day trip to Paris, France",
        "I want to visit Tokyo for 5 days with a budget of $2000",
        "Plan a weekend trip to New York City",
        "Create a 7-day itinerary for Bali, Indonesia",
        "What's the weather like in London?",
        "Convert 1000 USD to EUR",
        "Find restaurants in Rome",
        "Search for activities in Barcelona"
    ]
    
    print("🧳 Testing Travel Agent Workflow")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔹 Test {i}: {test_case}")
        print("-" * 30)
        
        try:
            response = workflow.run(test_case)
            print(f"✅ Response: {response}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
    
    # Interactive mode
    print("\n" + "=" * 50)
    print("🌍 Interactive Travel Planning Mode (type 'quit' to exit)")
    print("=" * 50)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            print("🤖 Agent: ", end="")
            response = workflow.run(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")