import pandas as pd
import datetime

data = {
    'loan number': list(range(1, 11)),
    'loan amount': [35000.00, 40000.00, 40000.00, 40000.00, 40000.00, 40000.00, 40000.00, 40000.00, 40000.00, 40000.00],
    'interest_rate': [0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08],
    'start_date': ['9/1/2023', '10/1/2023', '11/1/2023', '12/1/2023', '1/1/2024', '2/1/2024', '3/1/2024', '4/1/2024', '5/1/2024', '6/1/2024'],
    'term': [36, 12, 48, 60, 72, 60, 72, 60, 72, 60],
    'payment frequency': ['Monthly', 'Monthly', 'Monthly', 'Monthly', 'Monthly', 'Monthly', 'Monthly', 'Monthly', 'Monthly', 'Monthly'],
    'CPR (Conditional Prepayment Rate)': [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
}

initial_data = pd.DataFrame(data)

# Calculate and add the monthly payment as a new column
initial_data['monthly_interest_rate'] = initial_data['interest_rate'] / 12
initial_data['monthly_payment'] = (initial_data['loan amount'] * initial_data['monthly_interest_rate'] * (1 + initial_data['monthly_interest_rate'])**initial_data['term']) / ((1 + initial_data['monthly_interest_rate'])**initial_data['term'] - 1)

# Add the 'single_monthly_mortality' column with a value of 0.43% (0.0043 as a decimal)
initial_data['single_monthly_mortality'] = 0.043

# Display the DataFrame with the new 'single_monthly_mortality' column
print(initial_data)




def display_dataframes():
    all_data = initial_data
    all_data.fillna(0, inplace=True)
    
    new_data = all_data.to_dict(orient='dict')
        
    loan_amount_data = new_data['loan amount']
    loan_term_data = new_data['term']
    index = 0

    for _ in all_data:
        # Define the loan details
        loan_amount = loan_amount_data[index]
        loan_term = loan_term_data[index]
        annual_interest_rate = 0.08  # 8% annual interest rate
        start_date = '9/1/2023'  # Start date

        # Convert the start_date to a datetime object
        start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')

        # Create an empty DataFrame with the specified columns
        columns = ['period', 'date', 'opening balance', 'payment', 'pre-payment', 'interest rate', 'monthly interest rate', 'interest', 'principal', 'closing balance']
        df = pd.DataFrame(columns=columns)

        # Calculate the monthly interest rate
        monthly_interest_rate = annual_interest_rate / 12

        # Initialize the first row of the DataFrame with the opening balance and no pre-payment
        opening_balance = loan_amount
        prepayment_amount = 0  # No pre-payment in September
        df.loc[0] = [1, start_date, opening_balance, None, prepayment_amount, annual_interest_rate, monthly_interest_rate, None, None, opening_balance - prepayment_amount]

        monthly_payment = (loan_amount * monthly_interest_rate * (1 + monthly_interest_rate)**loan_term) / ((1 + monthly_interest_rate)**loan_term - 1)
        df.fillna(0, inplace=True)
        # Calculate values for subsequent rows based on the first row
        for i in range(1, loan_term + 1):
            previous_balance = df.at[i - 1, 'closing balance']
            interest = previous_balance * monthly_interest_rate
            principal = monthly_payment - interest

            # Start pre-payment from October onward
            prepayment_amount = previous_balance * 0.0042655  # 0.43% as a decimal

            # Calculate the principal by adding the pre-payment to it
            principal = principal + prepayment_amount

            closing_balance = previous_balance - principal
            
            # Calculate the next date by adding one month to the previous date
            next_date = df.at[i - 1, 'date'] + datetime.timedelta(days=30)
            
            # Update the pre-payment value for this row
            df.loc[i] = [i + 1, next_date, previous_balance, monthly_payment, prepayment_amount, annual_interest_rate, monthly_interest_rate, interest, principal, closing_balance]

        # Display the DataFrame
        if not df.apply(lambda x: x.eq(0).all()).any():
            print(df)

        index+=1

display_dataframes()
