class Calculator:
    @staticmethod
    def multiply(a, b) -> float:
        """
        Multiply two values after converting to float.

        Args:
            a: First number (can be str, int, or float)
            b: Second number (can be str, int, or float)

        Returns:
            float: The product of a and b.
        """
        return float(a) * float(b)
    
    @staticmethod
    def calculate_total(*x) -> float:
        """
        Calculate sum of the given values.

        Args:
            x: Variable number of inputs (float/int)

        Returns:
            float: The sum of the numbers
        """
        return sum(float(i) for i in x)
    
    @staticmethod
    def calculate_daily_budget(total, days) -> float:
        """
        Calculate daily budget

        Args:
            total: Total cost (float/int/str)
            days: Total number of days (int/str)

        Returns:
            float: Expense for a single day
        """
        total = float(total)
        days = int(days)
        return total / days if days > 0 else 0
