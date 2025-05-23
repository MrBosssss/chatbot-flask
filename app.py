# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1x-YQxH0C4-6ZbqRfOBBxi1c8li0dyE3h
"""

from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

expense_file = "expenses.csv"

# Load or create the expenses file
if os.path.exists(expense_file):
    df = pd.read_csv(expense_file)
else:
    df = pd.DataFrame(columns=["Category", "Amount"])
    df.to_csv(expense_file, index=False)

@app.route('/chat', methods=['POST'])
def chat():
    global df
    user_input = request.json.get('message', '')

    if "add" in user_input.lower():
        try:
            parts = user_input.split()
            category = parts[1]
            amount = float(parts[2])
            new_expense = pd.DataFrame([[category, amount]], columns=["Category", "Amount"])
            df = pd.concat([df, new_expense], ignore_index=True)
            df.to_csv(expense_file, index=False)
            return jsonify({'response': f"✅ Added {category} - ₹{amount}"})
        except:
            return jsonify({'response': "⚠️ Please say 'add Food 500' to log expenses."})

    elif "view" in user_input.lower():
        if df.empty:
            return jsonify({'response': "📌 No expenses recorded yet."})
        else:
            return jsonify({'response': df.to_string(index=False)})

    elif "budget" in user_input.lower():
        category_totals = df.groupby("Category")["Amount"].sum()
        if category_totals.empty:
            return jsonify({'response': "📌 No expenses recorded yet."})
        response = []
        for category, amount in category_totals.items():
            if category in ["Food", "Shopping"] and amount > 5000:
                response.append(f"🚨 ₹{amount} on {category} is high. Try discounts or budget-friendly options.")
            elif category == "Transport" and amount > 3000:
                response.append(f"🚇 ₹{amount} on Transport. Metro passes could help.")
            else:
                response.append(f"✅ {category} spending looks fine.")
        return jsonify({'response': "\n".join(response)})

    else:
        return jsonify({'response': "🤖 Hi! You can say 'add Food 500', 'view', or 'budget'."})

if __name__ == '__main__':
    app.run(debug=True)