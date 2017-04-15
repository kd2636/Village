from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response
    
    
# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///village.db")

@app.route("/")
def index():
    session.clear()
    return render_template("index.html")

@app.route("/landing")
@login_required
def landing():
    return render_template('landing.html')
    
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]
        session["region"] = rows[0]["region"]

        # redirect user to home page
        return redirect(url_for("landing"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method=="POST":
        if not request.form.get("name"):
            return apology("Name cannot be blank")
            
        elif not request.form.get("username"):
            return apology("Username cannot be blank")
            
        elif not request.form.get("passo"):
            return apology("Password cannot be blank")
            
        elif request.form.get("passo") != request.form.get("passv"):
            return apology("Password do not match")
            
        elif not request.form.get("phone"):
            return apology("Enter phone no")
            
        phoneNo = validNumber(request.form.get("phone"))
        if phoneNo == None:
            return apology("Invalid phone no")
        
        region = request.form.get("region")
        print(region)
        if region == '' or None:
            return apology("enter region")
            
        hash = pwd_context.encrypt(request.form.get("passo"))
        userid = db.execute("INSERT INTO users (name, username, hash, region, phone) VALUES(:name, :username, :hash, :region, :phone)",
        name = request.form.get("name"), username = request.form.get("username"), hash = hash, region = region, phone = phoneNo )
        if userid == None:
            return apology("username taken")
        
            
        session["user_id"]=userid
        session["user_name"]=request.form.get("username")
        session["region"]=region
        flash("Registered Successfully")
        return redirect(url_for('landing'))
        
    else:
        return render_template("register.html")
        
        
@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_idsell
    session.clear()

    # redirect user to login form
    return render_template("index.html")
    
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
        if not request.form.get("item"):
            return apology("Select Item")
        elif not request.form.get("qty") or int(request.form.get("qty")) < 1:
            return apology("Invalid qty")
        elif not request.form.get("price"):
            return apology("Enter price")
            
        
        item = request.form.get("item")
        qty = int(request.form.get("qty"))
        try:
            price = float(request.form.get("price"))
        except:
            return apology("Invalid price")
            
        fprice = formatPrice(price)
        
        db.execute("INSERT INTO products (userid, item, qty, price, region) VALUES(:userid, :item, :qty, :price, :region)",
        userid = session.get("user_id"), item = item, qty = qty, price = fprice, region = session.get("region"))
        
        flash("Post Successfull")
        return redirect(url_for('sell'))
    
    else:
        return render_template("sell.html")
        
        
    
    
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    
    if request.method == "POST":
        if not request.form.get("item") or request.form.get("item") == '':
            return apology("Input Item")
            
        rows = db.execute("SELECT * FROM products JOIN users ON products.userid = users.id WHERE item = :item AND products.region = :region AND status = :status ",
        item = request.form.get("item"), region = session.get("region"), status = 'Active')
        
        if len(rows) == 0:
            rows = None
        
        return render_template("list.html", rows = rows, item = request.form.get("item"))
        
    else:
        return render_template("buy.html")


@app.route("/delpost", methods=["GET", "POST"])
@login_required
def delpost():
    if request.method == "POST":
        #if not request.form["del"]
            #turn apology("Select post")
            
        db.execute("DELETE FROM products WHERE id = :id", id = request.form["del"])
        
        flash("Post deleted")
        return redirect(url_for('delpost'))
        
    else:
        rows = db.execute("SELECT * FROM products WHERE userid = :userid AND status = :status",
        userid = session.get("user_id"), status = 'Active')
        if len(rows) == 0:
            rows = None
        return render_template("delpost.html", rows = rows)


        
        
            
            

 