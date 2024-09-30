# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    #checks the request method is POST
    if request.method == "POST":
        #Create new transaction object using field form values
        transaction = {
            'id': len(transactions) + 1,             #create a new ID off the current length of the transaction list
            'date': request.form['date'],           #get the date field from the form
            'amount': float(request.form['amount']) #get the amount value from the form and convert to a float
        }
        # append the new transaction to the transaction list
        transactions.append(transaction)

        # redirect to the transaction list page after adding the transaction
        return redirect(url_for("get_transactions"))

    # when the request method if GET, render the form template to display the add transaction form
    return render_template("form.html")

# Update operation
@app.route('/edit/<int:transaction_id>', methods=["GET", "POST"])
def edit_transaction(transaction_id):
    #Check if request is POST
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float


        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated

        return redirect(url_for("get_transactions"))

    # if the request method is GET, find the transaction with correct id
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)

    # if the transaction id is not found , send a 404 
    return {"message": "Transaction not found"}, 404


# Delete operation
@app.route('/delete/<int:transaction_id>')
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    
    return redirect(url_for("get_transactions"))


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
