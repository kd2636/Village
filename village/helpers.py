import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
    
def validNumber(phoneNo):
    if phoneNo.isdigit():
        if len(phoneNo) == 10:
            return "+91-{}-{}-{}".format(phoneNo[0:3],phoneNo[3:6],phoneNo[6:10])
        elif len(phoneNo) == 11 and phoneNo[0] == 0:
            return "+91-{}-{}-{}".format(phoneNo[1:4],phoneNo[4:7],phoneNo[7:11])
        else:
            return None
    
    else:
        return None
        

def formatPrice(value):
    """Formats value as Rs"""
    return "Rs{:,.2f}/unit".format(value)
        