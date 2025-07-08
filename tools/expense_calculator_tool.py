from utils.expense_calculator import Calculator
from typing import List
from langchain.tools import tool

class CalculatorTool:
    def __init__(self):
        self.calculator = Calculator()
        self.calculator_tool_list = self._setup_tools()

    def _setup_tools(self) -> List:
        """Setup all tools for the calculator tool"""
        @tool
        def estimate_total_hotel_cost(price_per_night:str, total_days:float) -> float:
            """Calculate total hotel cost"""
            return self.calculator.multiply(price_per_night, total_days)
        
        @tool
        def calculate_total_expense(costs: List[float]) -> float:
            """Calculate total expense of the trip"""
            return self.calculator.calculate_total(*costs)

        
        @tool
        def calculate_daily_expense_budget(total_cost: float, days: int) -> float:
            """Calculate daily expense"""
            return self.calculator.calculate_daily_budget(total_cost, days)
        
        return [estimate_total_hotel_cost, calculate_total_expense, calculate_daily_expense_budget]
    



# Testing
def main():
    # Initialize the tool
    calculator_tool = CalculatorTool()

    # Extract the tool functions
    estimate_total_hotel_cost = calculator_tool.calculator_tool_list[0]
    calculate_total_expense = calculator_tool.calculator_tool_list[1]
    calculate_daily_expense_budget = calculator_tool.calculator_tool_list[2]

    # ==== Test 1: Estimate total hotel cost ====
    print("== Hotel Cost Test ==")
    hotel_cost_result = estimate_total_hotel_cost.invoke({
        "price_per_night": "90.5",  # string input to simulate user input
        "total_days": 3
    })
    print(f"Total hotel cost: {hotel_cost_result}")

    # ==== Test 2: Calculate total expense ====
    print("\n== Total Expense Test ==")
    total_expense_result = calculate_total_expense.invoke({
        "costs": [120.0, 75.5, 89.9, 45]  # list of float costs
    })
    print(f"Total trip expense: {total_expense_result}")

    # ==== Test 3: Calculate daily budget ====
    print("\n== Daily Budget Test ==")
    daily_budget_result = calculate_daily_expense_budget.invoke({
        "total_cost": 330.9,
        "days": 5
    })
    print(f"Daily budget: {daily_budget_result}")

if __name__ == "__main__":
    main()