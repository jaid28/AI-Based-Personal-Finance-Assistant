import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.data_handler import DataHandler, DEFAULT_CATEGORIES
from utils.analysis import FinancialAnalysis

# Page configuration
st.set_page_config(
    page_title="Personal Finance Assistant",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'expenses_df' not in st.session_state:
    st.session_state.expenses_df = DataHandler.create_empty_dataframe()

# Custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Sidebar
st.sidebar.title("💰 Finance Assistant")
action = st.sidebar.radio("Choose Action", ["Dashboard", "Add Expense", "Import/Export"])

if action == "Dashboard":
    st.title("Financial Dashboard")
    
    # Basic metrics
    metrics = FinancialAnalysis.calculate_basic_metrics(st.session_state.expenses_df)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Expenses", f"${metrics['total_expenses']:.2f}")
    with col2:
        st.metric("Average Expense", f"${metrics['average_expense']:.2f}")
    with col3:
        st.metric("Highest Expense", f"${metrics['highest_expense']:.2f}")
    with col4:
        st.metric("Most Common Category", metrics['most_common_category'])

    # Expense by Category
    st.subheader("Expenses by Category")
    category_data = FinancialAnalysis.analyze_spending_by_category(st.session_state.expenses_df)
    if not category_data.empty:
        fig = px.pie(category_data, values='amount', names='category', 
                     title='Expense Distribution')
        st.plotly_chart(fig)

    # Monthly Trend
    st.subheader("Monthly Spending Trend")
    monthly_trend = FinancialAnalysis.generate_monthly_trend(st.session_state.expenses_df)
    if not monthly_trend.empty:
        fig = px.line(monthly_trend, x='date', y='amount',
                      title='Monthly Spending Trend')
        st.plotly_chart(fig)

    # Budget Suggestions
    st.subheader("Suggested Monthly Budget")
    suggested_budget = FinancialAnalysis.suggest_budget(st.session_state.expenses_df)
    if suggested_budget:
        budget_df = pd.DataFrame(suggested_budget.items(), 
                               columns=['Category', 'Suggested Amount'])
        st.table(budget_df)

elif action == "Add Expense":
    st.title("Add New Expense")
    
    with st.form("expense_form"):
        date = st.date_input("Date", datetime.today())
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01)
        category = st.selectbox("Category", DEFAULT_CATEGORIES)
        description = st.text_input("Description")
        
        submitted = st.form_submit_button("Add Expense")
        
        if submitted:
            if DataHandler.validate_expense_data(
                date.strftime('%Y-%m-%d'), amount, category, description
            ):
                new_expense = pd.DataFrame({
                    'date': [date.strftime('%Y-%m-%d')],
                    'amount': [amount],
                    'category': [category],
                    'description': [description]
                })
                st.session_state.expenses_df = pd.concat(
                    [st.session_state.expenses_df, new_expense], 
                    ignore_index=True
                )
                st.success("Expense added successfully!")
            else:
                st.error("Please check your input values.")

else:  # Import/Export
    st.title("Import/Export Data")
    
    # Import
    st.subheader("Import Expenses")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        imported_df = DataHandler.import_from_csv(uploaded_file)
        if imported_df is not None:
            st.session_state.expenses_df = imported_df
            st.success("Data imported successfully!")
        else:
            st.error("Invalid file format. Please check your CSV file.")
    
    # Export
    st.subheader("Export Expenses")
    if not st.session_state.expenses_df.empty:
        csv_data = DataHandler.export_to_csv(st.session_state.expenses_df)
        st.download_button(
            label="Download Expenses CSV",
            data=csv_data,
            file_name="expenses.csv",
            mime="text/csv"
        )
    else:
        st.info("No expenses to export.")

# Display current expenses
# if not st.session_state.expenses_df.empty:
#     st.subheader("Recent Expenses")
#     st.dataframe(
#         st.session_state.expenses_df.sort_values('date', ascending=False).head(5),
#         use_container_width=True
#     )            // Some Error in this line of code

if not st.session_state.expenses_df.empty:
    # Convert the 'date' column to datetime format
    st.session_state.expenses_df['date'] = pd.to_datetime(st.session_state.expenses_df['date'], errors='coerce')

    # Sort the DataFrame by date
    st.session_state.expenses_df = st.session_state.expenses_df.sort_values('date', ascending=False)

    # Display the dataframe
    st.subheader("Recent Expenses")
    st.dataframe(st.session_state.expenses_df.head(5), use_container_width=True)
