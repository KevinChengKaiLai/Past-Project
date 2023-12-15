import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    user_id = session['user_id']
    stocks = db.execute("SELECT  name, price, SUM(shares) as SUM FROM transactions WHERE user_id = ? GROUP BY name",user_id)
    cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]['cash']
    total = cash
    for stock in stocks:
        total += stock['price'] * stock["SUM"]
    return render_template("index.html", stocks = stocks, cash = cash, usd = usd, total = total)

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        stock = request.form.get("symbol").upper()
        target = lookup(stock)

        if not stock:
            return apology("STOCK Name required!!")
        elif not target:
            return apology("STOCK not found!!")

        try:
            shares =int(request.form.get("shares"))
        except:
            return apology("Shares must be integer!!")
        if shares <= 0:
            return apology("Shares must be positive !!")
        user_id = session['user_id']
        cash = db.execute('SELECT cash FROM users WHERE id = ?', user_id)[0]['cash']
        stock_name = target['name']
        stock_price = target['price']
        total = stock_price * shares
        if cash < total:
            return apology("not enough cash")
        else:
            cash = cash - total
            db.execute("UPDATE users SET cash = ? WHERE id = ?", cash ,user_id)
            db.execute("INSERT INTO transactions (user_id, name, shares, price, type) VALUES(?,?,?,?,?)", user_id, stock_name, shares, stock_price, "buy")
            print(f'\n\n{cash}\n\n')

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session['user_id']
    transactions = db.execute("SELECT type,name, shares, price, time FROM transactions WHERE user_id = ?", user_id)
    print(transactions)

    return render_template("history.html", transactions = transactions, usd = usd)

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
        print(rows)
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
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Please enter a stock you like")

        target = lookup(symbol)
        if not target:
            return apology("Not A Valid Stock")
        return render_template('quoted.html',target = target, usd=usd)

    else:
        return render_template('quote.html')
        # return apology("TODO")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if (request.method =="POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirmation')

        if not username:
            return apology("No Username, Can't Register!!")
        elif not password:
           return apology("No Password, Can't Register!!")
        elif password != confirm_password:
           return apology("Password is different!")
        elif not confirm_password:
          return apology("No Confirm Password, Can't Register!!")

        PW_hash = generate_password_hash(password)
        try:
            db.execute("INSERT INTO users(username,hash) VALUES(?,?)", username,PW_hash)
            return redirect('/')
        except:
            return apology("Usename is existed!")

        return redirect('/')
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        user_id = session['user_id']
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        price = lookup(symbol)['price']
        owned = db.execute("SELECT shares FROM transactions WHERE user_id = ? AND name = ? GROUP BY name", user_id, symbol)[0]['shares']
        if owned < shares:
            return apology("Not enough shares!")

        current_cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
        current_cash += price * shares
        db.execute("UPDATE users SET cash = ? WHERE id = ?",current_cash, user_id)
        db.execute("INSERT INTO transactions (user_id, name, shares, price, type) VALUES(?,?,?,?,?)", user_id, symbol, -shares, price, "sell")
        return redirect('/')

    else:
        user_id = session['user_id']
        symbols = db.execute("SELECT name FROM transactions WHERE user_id = ? GROUP BY name", user_id)
        return render_template("sell.html", symbols = symbols)

