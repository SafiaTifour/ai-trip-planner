import os
from utils.place_info_search import TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv

class PlaceSearchTool:
    def __init__(self):
        load_dotenv()
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the place search tool using only Tavily"""
        @tool
        def search_attractions(place: str) -> str:
            """Search attractions of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_attractions(place)
                return f"Following are the attractions of {place}: {tavily_result}"
            except Exception as e:
                return f"Unable to find attractions for {place} due to: {str(e)}"
        
        @tool
        def search_restaurants(place: str) -> str:
            """Search restaurants of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_restaurants(place)
                return f"Following are the restaurants of {place}: {tavily_result}"
            except Exception as e:
                return f"Unable to find restaurants for {place} due to: {str(e)}"
        
        @tool
        def search_activities(place: str) -> str:
            """Search activities of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_activity(place)
                return f"Following are the activities in and around {place}: {tavily_result}"
            except Exception as e:
                return f"Unable to find activities for {place} due to: {str(e)}"
        
        @tool
        def search_transportation(place: str) -> str:
            """Search transportation of a place"""
            try:
                tavily_result = self.tavily_search.tavily_search_transportation(place)
                return f"Following are the modes of transportation available in {place}: {tavily_result}"
            except Exception as e:
                return f"Unable to find transportation information for {place} due to: {str(e)}"
        
        return [search_attractions, search_restaurants, search_activities, search_transportation]
    





# Testing
def test_place_search_tools(place: str):
    tool_runner = PlaceSearchTool()

    print(f"\n🔍 Testing place search tools for: {place}\n{'=' * 50}")

    for tool_func in tool_runner.place_search_tool_list:
        print(f"\n🛠️ Tool: {tool_func.name}")
        try:
            result = tool_func.invoke({"place": place})
            print(f"✅ Result:\n{result}")
        except Exception as e:
            print(f"❌ Error while running {tool_func.name}: {e}")

if __name__ == "__main__":
    test_place_search_tools("Paris")