import pandas as pd
from datetime import datetime
import io

DEFAULT_CATEGORIES = [
    "Food & Dining", "Transportation", "Housing", "Utilities",
    "Healthcare", "Entertainment", "Shopping", "Education"
]

class DataHandler:
    @staticmethod
    def create_empty_dataframe():
        return pd.DataFrame({
            'date': [],
            'amount': [],
            'category': [],
            'description': []
        })

    @staticmethod
    def validate_expense_data(date, amount, category, description):
        try:
            # Validate date
            datetime.strptime(date, '%Y-%m-%d')
            # Validate amount
            float(amount)
            # Validate category and description
            if not category or not description:
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def export_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    @staticmethod
    def import_from_csv(file):
        try:
            df = pd.read_csv(file)
            required_columns = ['date', 'amount', 'category', 'description']
            if not all(col in df.columns for col in required_columns):
                return None
            return df
        except Exception:
            return None
