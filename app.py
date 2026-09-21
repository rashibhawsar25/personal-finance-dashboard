from flask import Flask, render_template, request, redirect, url_for
from models.transaction import db, Transaction
from datetime import date

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///finance.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def home():
    transactions = Transaction.query.all()

    total_income = sum(
        t.amount for t in transactions if t.type == "income"
    )

    total_expenses = sum(
        t.amount for t in transactions if t.type == "expense"
    )

    total_savings = total_income - total_expenses

    return render_template(
        "index.html",
        total_income=total_income,
        total_expenses=total_expenses,
        total_savings=total_savings,
        transactions=transactions
    )


@app.route("/transactions")
def transactions():
    transactions = Transaction.query.all()

    return render_template(
        "transactions.html",
        transactions=transactions
    )
@app.route("/reports")
def reports():
    transactions = Transaction.query.all()

    total_income = sum(
        t.amount for t in transactions if t.type == "income"
    )

    total_expenses = sum(
        t.amount for t in transactions if t.type == "expense"
    )

    total_savings = total_income - total_expenses

    return render_template(
        "reports.html",
        total_income=total_income,
        total_expenses=total_expenses,
        total_savings=total_savings
    )
@app.route("/settings")
def settings():
    return render_template("settings.html")
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    if request.method == "POST":
        transaction.amount = float(request.form["amount"])
        transaction.type = request.form["type"]
        transaction.category = request.form["category"]
        transaction.description = request.form["description"]

        db.session.commit()

        return redirect(url_for("transactions"))

    return render_template(
        "edit_transaction.html",
        transaction=transaction
    )
@app.route("/delete/<int:id>", methods=["POST"])
def delete_transaction(id):
    transaction = Transaction.query.get_or_404(id)

    db.session.delete(transaction)
    db.session.commit()

    return redirect(url_for("transactions"))
@app.route("/add", methods=["GET", "POST"])
def add_transaction():

    if request.method == "POST":

        amount = float(request.form["amount"])

        transaction_type = request.form["type"]

        category = request.form["category"]

        description = request.form["description"]

        new_transaction = Transaction(
            amount=amount,
            type=transaction_type,
            category=category,
            description=description,
            date=date.today()
        )

        db.session.add(new_transaction)

        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add_transaction.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)