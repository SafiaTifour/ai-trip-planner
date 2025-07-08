import os
from typing import List
from langchain.tools import tool
from dotenv import load_dotenv
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

class CurrencyConverterTool:
    def __init__(self):
        load_dotenv()
        # Use AlphaVantage API key instead of Exchange Rate API
        self.api_key = os.environ.get("ALPHAVANTAGE_API_KEY")
        self.alpha_vantage = AlphaVantageAPIWrapper()
        self.currency_converter_tool_list = self._setup_tools()

    def _convert_currency(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Internal method to convert currency using Alpha Vantage API
        
        Args:
            amount (float): Amount to convert
            from_currency (str): Source currency code
            to_currency (str): Target currency code
            
        Returns:
            float: Converted amount
        """
        try:
            # Set the API key in environment for AlphaVantage
            os.environ["ALPHAVANTAGE_API_KEY"] = self.api_key
            
            # Get exchange rate
            response = self.alpha_vantage._get_exchange_rate(from_currency, to_currency)
            exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
            
            # Calculate converted amount
            converted_amount = amount * float(exchange_rate)
            return converted_amount
            
        except Exception as e:
            print(f"Error in currency conversion: {e}")
            return None

    def _setup_tools(self) -> List:
        """Setup all tools for the currency converter tool"""
        
        @tool
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
            """
            Convert amount from one currency to another using Alpha Vantage API.
            
            Args:
                amount (float): The amount to convert
                from_currency (str): Source currency code (e.g., 'USD', 'EUR')
                to_currency (str): Target currency code (e.g., 'EUR', 'GBP')
                
            Returns:
                float: Converted amount, or None if conversion failed
            """
            return self._convert_currency(amount, from_currency, to_currency)
        
        return [convert_currency]

    def get_tools(self) -> List:
        """Get the list of available tools"""
        return self.currency_converter_tool_list

    def test_conversion(self, amount: float = 100.0, from_curr: str = "USD", to_curr: str = "EUR"):
        """
        Test the currency conversion functionality
        
        Args:
            amount (float): Amount to test with
            from_curr (str): Source currency
            to_curr (str): Target currency
        """
        print(f"Testing currency conversion:")
        print(f"Converting {amount} {from_curr} to {to_curr}")
        
        result = self._convert_currency(amount, from_curr, to_curr)
        
        if result is not None:
            print(f"Result: {amount} {from_curr} = {result:.2f} {to_curr}")
        else:
            print("Conversion failed. Please check your API key and currency codes.")
        
        return result




# Example usage and testing
if __name__ == "__main__":
    # Initialize the tool
    converter_tool = CurrencyConverterTool()
    
    # Test the conversion
    converter_tool.test_conversion(100.0, "USD", "EUR")
    converter_tool.test_conversion(50.0, "EUR", "GBP")
    
    # Get the tools for use with LangChain
    tools = converter_tool.get_tools()
    print(f"\nAvailable tools: {len(tools)}")
    
    # Test using the tool directly
    convert_tool = tools[0]
    result = convert_tool.invoke({"amount": 100, "from_currency": "USD", "to_currency": "JPY"})
    print(f"Tool result: {result}")