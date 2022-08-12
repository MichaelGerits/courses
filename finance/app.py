import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    # TODO: Display the entries in the database on index.html
    stocks = db.execute("SELECT symbol, amount, cash FROM stocks AS 's' JOIN users AS 'u' ON u.id = s.user_id WHERE u.id = ?", user_id)
    if len(stocks) == 0:
        stocks = [{"name": "none", "symbol": "none", "amount": 0, "total_price": usd(0), "price": usd(0)}]
        return render_template("index.html", stocks=stocks, cash=usd(0), total=usd(0))

    cash = stocks[0]["cash"]
    total = cash
    for stock in stocks:
        response = lookup(stock["symbol"])
        #checks if response succeeded
        if response == None:
            return apology("error with API/invalid symbol")
        #sets variables from response and other sources
        price = response["price"]
        stock["total_price"] = price * int(stock["amount"])
        total = total + int(stock["total_price"])
        stock["price"] = usd(price)
        stock["total_price"] = usd(stock["total_price"])
        stock["name"] = response["name"]

    return render_template("index.html", stocks=stocks, cash=usd(cash), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    #checks if its a form sending
    if request.method == "POST":
        #gets the values from the form
        symbol = request.form.get("symbol")
        amount = request.form.get("shares")
        #checks if the inputs are valid
        if not symbol:
            return apology("fill in symbol")
        elif not amount:
            return apology("Invalid amount")
        amount_int = int(amount)
        if amount_int <=0 or (isinstance(amount_int, int) == False):
            return apology("Invalid amount")
        #gets the response using lookup
        response = lookup(symbol)
        #checks if response succeeded
        if response == None:
            return apology("error with API/invalid symbol")
        #sets variables from response and other sources
        price = response["price"]
        dic_symbol = response["symbol"]
        total_price = price * amount_int
        user_id = session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = (?)", user_id)[0]["cash"]
        #checks if the person has enough money
        if total_price > cash:
            return apology("you're poor")
        #checks if the user already owns anny of these stocks
        exists = db.execute("SELECT symbol, user_id, amount FROM stocks WHERE symbol = ? AND user_id= ?", dic_symbol, user_id)
        if len(exists) == 0:
            db.execute("INSERT INTO stocks (user_id, symbol, amount) VALUES (?, ?, ?)", user_id, dic_symbol, amount_int)
        else:
            db.execute("UPDATE stocks SET amount = (?) WHERE user_id = ? AND symbol = ?", (amount_int + exists[0]["amount"]), user_id, dic_symbol)
        #todo: reduce cash and add purchase to table
        db.execute("INSERT INTO transactions (user_id, symbol, amount, price, trans_type) VALUES (?, ?, ?, ?, 'BUY')", user_id, dic_symbol, amount_int, usd(price))
        db.execute("UPDATE users SET cash = (?) WHERE id = (?)" ,(cash - total_price), user_id)
        return redirect("/")
    #else it has to be a visit to the page
    return render_template("buy.html")

@app.route("/transaction", methods=["POST"])
def transaction():
    # Forget birthday
    user_id = session["user_id"]
    symbol = request.form.get("symbol")
    amount = request.form.get("shares")
    trans_type = request.form.get("trans_type")
    cash = db.execute("SELECT cash FROM users WHERE id = (?)", user_id)[0]["cash"]
    if symbol:
        if not amount:
            return apology("Invalid amount")
        amount_int = int(amount)
        if amount_int <=0:
            return apology("Invalid amount")
        #gets the response using lookup
        response = lookup(symbol)
        #checks if response succeeded
        if response == None:
            return apology("error with API/invalid symbol")
        #sets variables from response and other sources
        price = response["price"]
        total_price = price * amount_int

        if trans_type == "BUY":
            exists = db.execute("SELECT user_id, amount FROM stocks WHERE symbol = ? AND user_id= ?", symbol, user_id)
            #checks if the person has enough money
            if total_price > cash:
                return apology("you're poor")
            #checks if the user already owns anny of these stocks
            if len(exists) == 0:
                db.execute("INSERT INTO stocks (user_id, symbol, amount) VALUES (?, ?, ?)", user_id, symbol, amount_int)
            else:
                db.execute("UPDATE stocks SET amount = (?) WHERE user_id = ? AND symbol = ?", (amount_int + exists[0]["amount"]), user_id, symbol)
            #todo: reduce cash and add purchase to table
            db.execute("INSERT INTO transactions (user_id, symbol, amount, price, trans_type) VALUES (?, ?, ?, ?, 'BUY')", user_id, symbol, amount_int, usd(price))
            db.execute("UPDATE users SET cash = (?) WHERE id = (?)" ,(cash - total_price), user_id)

        else:
            available = db.execute("SELECT amount FROM stocks WHERE user_id = (?) AND symbol = (?)", user_id, symbol)[0]["amount"]
            #checks if the person has enough stocks
            if amount_int > available:
                return apology("you don't have that much")
            #checks if the user already owns anny of these stocks
            db.execute("UPDATE stocks SET amount = (?) WHERE user_id = ? AND symbol = ?", (available - amount_int), user_id, symbol)
            #todo: reduce cash and add purchase to table
            db.execute("INSERT INTO transactions (user_id, symbol, amount, price, trans_type) VALUES (?, ?, ?, ?, 'SELL')", user_id, symbol, amount_int, usd(price))
            db.execute("UPDATE users SET cash = (?) WHERE id = (?)" ,(cash + total_price), user_id)
        return redirect("/")

@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    # TODO: Display the entries in the database on index.html
    history = db.execute("SELECT * FROM transactions AS 't' JOIN users AS 'u' ON u.id = t.user_id WHERE u.id = ? ORDER BY timestamp DESC", user_id)
    if len(history) == 0:
            return apology("No transactions made")
    for transaction in history:
        response = lookup(transaction["symbol"])
        #checks if response succeeded
        if response == None:
            return apology("error with API/invalid symbol")
        #sets variables from response and other sources
        transaction["name"] = response["name"]

    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    #checks if its a form sending
    if request.method == "POST":
        #gets the values from the form
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("fill in symbol")
        #gets the response using lookup
        response = lookup(symbol)
        #makes sure the inputs are correct
        if not response:
            return apology("error with API/invalid symbol")
        return render_template("quoted.html", name=response["name"], price=usd(response["price"]), dic_symbol=response["symbol"])
    #else it has to be a visit to the page
    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    #checks if its a form sending
    if request.method == "POST":
        #gets the values from the form
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        registrants = db.execute("SELECT username FROM users WHERE username = ?", username)
        #makes sure the inputs are correct
        for i in registrants:
            if username in i["username"]:
                return apology("username in use.")
        if username == "" or not username:
            return apology("Invalid username.")
        elif password == "" or confirmation == "" or password != confirmation:
            return apology("c'mon man, comfirm password.")
        #adds the valid registration to the sql database (password is hashed)
        db.execute("INSERT INTO users(username, hash) VALUES ((?), (?))", username, generate_password_hash(password))
        return redirect("/")
    #else it has to be a visit to the page
    return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    #checks if its a form sending
    if request.method == "POST":
        #gets the values from the form
        symbol = request.form.get("symbol")
        amount = request.form.get("shares")
        #checks if the inputs are valid
        if not symbol:
            return apology("fill in symbol")
        elif not amount:
            return apology("Invalid amount")
        amount_int = int(amount)
        if amount_int <=0:
            return apology("Invalid amount")
        #gets the response using lookup
        response = lookup(symbol)
        #checks if response succeeded
        if response == None:
            return apology("error with API/invalid symbol")
        #sets variables from response and other sources
        profit = response["price"]
        dic_symbol = response["symbol"]
        total_profit = profit * amount_int
        user_id = session["user_id"]
        available = db.execute("SELECT amount FROM stocks WHERE user_id = (?) AND symbol = (?)", user_id, dic_symbol)[0]["amount"]
        cash = db.execute("SELECT cash FROM users WHERE id = (?)", user_id)[0]["cash"]
        #checks if the person has enough stocks
        if amount_int > available:
            return apology("you don't have that much")
        #checks if the user already owns anny of these stocks
        db.execute("UPDATE stocks SET amount = (?) WHERE user_id = ? AND symbol = ?", (available - amount_int), user_id, dic_symbol)
        #todo: reduce cash and add purchase to table
        db.execute("INSERT INTO transactions (user_id, symbol, amount, price, trans_type) VALUES (?, ?, ?, ?, 'SELL')", user_id, dic_symbol, amount_int, usd(profit))
        db.execute("UPDATE users SET cash = (?) WHERE id = (?)" ,(cash + total_profit), user_id)
        return redirect("/")
    #else it has to be a visit to the page
    else:
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol", session["user_id"])
        return render_template("sell.html", symbols=symbols)
