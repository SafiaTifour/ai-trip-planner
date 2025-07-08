import os
from dotenv import load_dotenv
load_dotenv()
from langchain.tools import tool
from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper

@tool
def multiply(a: int, b: int) -> int:
    """
    Multiply two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The product of a and b.
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    Add two integers.

    Args:
        a (int): The first integer.
        b (int): The second integer.

    Returns:
        int: The sum of a and b.
    """
    return a + b




import os
from dotenv import load_dotenv
load_dotenv()

def currency_converter(from_curr: str, to_curr: str, value: float) -> float:
    """
    Convert currency using Alpha Vantage API.
    
    Args:
        from_curr (str): Source currency code (e.g., 'USD')
        to_curr (str): Target currency code (e.g., 'EUR')
        value (float): Amount to convert
    
    Returns:
        float: Converted amount
    """
    try:
        from langchain_community.utilities.alpha_vantage import AlphaVantageAPIWrapper
        
        os.environ["ALPHAVANTAGE_API_KEY"] = os.getenv('ALPHAVANTAGE_API_KEY')
        alpha_vantage = AlphaVantageAPIWrapper()
        response = alpha_vantage._get_exchange_rate(from_curr, to_curr)
        exchange_rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
        return value * float(exchange_rate)
    
    except Exception as e:
        print(f"Error in currency conversion: {e}")
        return None

# Test the currency converter
if __name__ == "__main__":
    # Test cases
    test_cases = [
        ("USD", "EUR", 100.0),
        ("EUR", "USD", 50.0),
        ("USD", "GBP", 75.0),
        ("JPY", "USD", 1000.0)
    ]
    
    print("Testing Currency Converter:")
    print("-" * 40)
    
    for from_curr, to_curr, amount in test_cases:
        result = currency_converter(from_curr, to_curr, amount)
        if result is not None:
            print(f"{amount} {from_curr} = {result:.2f} {to_curr}")
        else:
            print(f"Failed to convert {amount} {from_curr} to {to_curr}")
    
    # Interactive test
    print("\nInteractive Test:")
    print("-" * 40)
    try:
        from_currency = input("Enter source currency (e.g., USD): ").upper()
        to_currency = input("Enter target currency (e.g., EUR): ").upper()
        amount = float(input("Enter amount to convert: "))
        
        result = currency_converter(from_currency, to_currency, amount)
        if result is not None:
            print(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        else:
            print("Conversion failed. Please check your API key and currency codes.")
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except ValueError:
        print("Invalid amount entered.")
    except Exception as e:
        print(f"An error occurred: {e}")