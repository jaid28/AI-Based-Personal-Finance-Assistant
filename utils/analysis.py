import pandas as pd
import numpy as np

class FinancialAnalysis:
    @staticmethod
    def calculate_basic_metrics(df):
        if df.empty:
            return {
                'total_expenses': 0,
                'average_expense': 0,
                'highest_expense': 0,
                'most_common_category': 'N/A'
            }
        
        metrics = {
            'total_expenses': df['amount'].sum(),
            'average_expense': df['amount'].mean(),
            'highest_expense': df['amount'].max(),
            'most_common_category': df['category'].mode().iloc[0] if not df['category'].empty else 'N/A'
        }
        return metrics

    @staticmethod
    def analyze_spending_by_category(df):
        if df.empty:
            return pd.DataFrame()
        return df.groupby('category')['amount'].sum().reset_index()

    @staticmethod
    def generate_monthly_trend(df):
        if df.empty:
            return pd.DataFrame()
        df['date'] = pd.to_datetime(df['date'])
        monthly = df.groupby(df['date'].dt.strftime('%Y-%m'))['amount'].sum().reset_index()
        return monthly

    @staticmethod
    def suggest_budget(df):
        if df.empty:
            return {}
        
        monthly_expenses = df.groupby('category')['amount'].sum() / len(df['date'].unique())
        suggested_budget = {}
        
        for category in monthly_expenses.index:
            # Add 10% buffer to average monthly expense
            suggested_budget[category] = monthly_expenses[category] * 1.1
            
        return suggested_budget
