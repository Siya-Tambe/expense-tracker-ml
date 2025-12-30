"""
Expense Tracker with ML-Based Prediction
Author: Siya
Description: Tracks expenses, analyzes spending patterns,
and predicts future expenses using Linear Regression.
"""

import csv
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_next_expense(amounts):
    if len(amounts) < 3:
        print("\nNot enough data for prediction.")
        return 
    
    # X = 0,1,2,... for each past expense
    X = np.array(range(len(amounts))).reshape(-1,1)
    y = np.array(amounts)

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]

    # Predict next expense
    next_index = np.array([[len(amounts)]])

    prediction = model.predict(next_index)
    print("\n Predicted next expense amount:", round(prediction[0],2))

    average_spending = sum(amounts)/len(amounts)
    if prediction[0] > average_spending * 1.3:
        print("⚠️ Overspending Alert: Your next expense is much higher than usual!")   
    if slope > 0:
        print("📈 Spending trend: Increasing")
    elif slope < 0:
        print("📉 Spending trend: Decreasing")
    else:
        print("➖ Spending trend: Stable")

def add_expense():
    file = open("expenses.csv", "a", newline="")
    writer = csv.writer(file)

    date = datetime.now().strftime("%Y-%m-%d")
    amount = input("Enter amount:")
    category = input("Enter category:")
    note = input("Optional note:")
    
    writer.writerow([date, category, amount, note])
    file.close()

    print("Expense saved!")

def view_expenses():
    file = open("expenses.csv", "r")
    reader = csv.reader(file)

    total = 0
    category_totals = {}
    print("\n--- Your expenses ---")

    amounts = []

    for row in reader:
        # skip empty rows or header row
        if len(row) != 4 or row[2]=="amount":
            continue

        date = row[0]
        category = row[1]
        amount = float(row[2])
        amounts.append(amount)
        note = row[3]

        total += amount

        # category wise total
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

        print(
            "Date : ",row[0],
            "| Category : ",row[1],
            "| Amount : ",row[2],
            "| Note : ",row[3]
            )

    file.close()
    print("\nTotal spent :", total)

    print("\n--- Category wise sepndings ---")
    for category in category_totals:
        print(category, ":", category_totals[category]) 
    
    if category_totals:
        highest_category = max(category_totals, key=category_totals.get)
        print("\nHighest spending category:", highest_category)

        predict_next_expense(amounts)

while True:
    print("\n=== Expense Tracker ===")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Exit")
    choice = input("Enter your choice:")

    if choice == '1':
        add_expense()
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        print("Exiting program")
        break
else:
    print("Invalid choice")





