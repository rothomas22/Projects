import os
import requests

from flask import Flask, session, render_template, request, redirect, url_for , jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

if __name__ =="__main__":
    app.run(Host='0.0.0.0',port=8001)
    books = None

error_message = ""
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/validateUser", methods=["GET", "POST"])
def validateUser():
  
    submitbtn = request.form.get("submit")
    registertbtn = request.form.get("register")
    name = request.form.get("name")
    password = request.form.get("password")

    Enteredisbn = "Enter any ISBN"
    Enteredtitle = "Enter any Title"
    Enteredauthor = "Enter any Author"

    if request.method == "POST":
        if submitbtn == "Submit":
            user = db.execute("SELECT userid, password from users where username =:name and password =:password", {"name":name, "password": password} ).fetchone()
            if user is None :
                error_message = "UserID/Password is invalid.  Please re-enter or register"
                return render_template("index.html", error_message = error_message)
            else :
                session["user_id"] = user.userid
                session["name"] = name
        elif registertbtn == "Register":  
            emailaddress = request.form.get("emailaddress")
            if ( (emailaddress =="") or (name =="") or (password =="") ):
                error_message = "Email address, Name , Password is required.  Please re-enter for register"
                return render_template("index.html", error_message = error_message)
            else:
                db.execute ("INSERT INTO users (username, password, emailaddress) VALUES (:username, :password, :emailaddress)",
                {"username":name, "password": password, "emailaddress":emailaddress })
                db.commit()
                user = db.execute("SELECT userid, password from users where username =:name and password =:password", {"name":name, "password": password} ).fetchone()
                session["user_id"] = user.userid
                session["name"] = name
   
    return render_template("Search.html", name = session["name"], isbn = Enteredisbn , author = Enteredauthor , title = Enteredtitle)
@app.route("/logout")
def logout():
        session["user_id"] = ""
        session["name"] = ""
        session["error_message"]= ""

        return render_template("index.html")

@app.route("/searchBook", methods=["GET", "POST"])
def searchBook():
    session["error_message"]= ""
  
    if request.method == "POST":
        isbn = request.form.get("isbn")
        if isbn is None or isbn =="":
            Enteredisbn = "Enter any ISBN"
            isbn = ""
        else:
            Enteredisbn = isbn
        isbn = "%"+ str(isbn) + "%"
        title = request.form.get("title")
        if title is None or title =="":
            Enteredtitle = "Enter any Title"
            title = ""
        else:
            Enteredtitle = title
        title = "%"+ str(title) + "%"
        author = request.form.get("author")
        if author is None or author =="":
            Enteredauthor = "Enter any Author"
            author = ""
        else:
            Enteredauthor = author
        author = "%"+ str(author) + "%"
       
        books = db.execute("SELECT * from books where isbn like :isbn and title like :title and author like :author", {"title":title, "isbn": isbn, "author": author} ).fetchall()

        return render_template("Search.html",name = session["name"], books=books, isbn = Enteredisbn , author = Enteredauthor , title = Enteredtitle)

@app.route("/bookDetails/<int:bookid>", methods=["GET"])
def bookDetails(bookid):
    #bookid = request.form.get("bookid")
    session["bookid"] = bookid

    bookDetails = db.execute("SELECT b.title, b.author, b.isbn, b.year, u.username, br.reviewtext, br.rating from books b left join bookreviews br on b.bookid = br.bookid " +
    "left join users u on u.userid = br.userid where b.bookid = :bookid", {"bookid":bookid} ).fetchall()

    if bookDetails is None:
        return ("Book not found")
    else:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "nXn9aCuRsnXObj5uGflP3Q", "isbns": {bookDetails[0].isbn}})
        data = res.json()
        return render_template("bookReviews.html",name = session["name"], bookDetails=bookDetails, goodreads=data)

@app.route("/addRating", methods=["POST"])
def addRating():
    submitbtn = request.form.get("Submit")
    session["error_message"]= ""
    if submitbtn == "Submit":
        reviewtext = request.form.get("ReviewText")
        rating =  request.form.get("rating")
        if ( (reviewtext =="") or (rating =="") ):
            session["error_message"]= "Review Text, Rating  is required.  Please re-enter for submission"
            return redirect(url_for('bookDetails', bookid=session["bookid"]))
        else:
            db.execute ("INSERT INTO bookreviews (bookid, userid, reviewtext, rating) VALUES (:bookid, :userid, :reviewtext, :rating)",
            {"userid":session["user_id"], "bookid": session["bookid"], "reviewtext":reviewtext, "rating": rating })
            db.commit()
            # return render_template("bookReviews.html",name = session["name"] , bookid=session["bookid"])
            return redirect(url_for('bookDetails', bookid=session["bookid"]))

@app.route("/api/<string:isbn>", methods=["GET"])
def api(isbn):
    error404 = False
    if isbn is None:
        error404 = True
    else:
        bookDetails = db.execute("SELECT b.title, b.author, b.isbn, b.year, count(br.bookid) as reviewcount, avg(br.rating) as avgrating from books b left join bookreviews br on b.bookid = br.bookid " +
        "where b.isbn = :isbn group by 1,2,3,4", {"isbn":isbn} ).fetchone()
        if bookDetails is None:
            error404 = True
        else:
            avgrating = round(bookDetails.avgrating, 2)

    if error404:
        return jsonify({"error": "ISBN not found"}), 404
    else:
         return jsonify({
            "title": bookDetails.title,
            "author": bookDetails.author,
            "year": bookDetails.year,
            "isbn": bookDetails.isbn,
            "review_count": bookDetails.reviewcount,
            "average_score": str(avgrating)
         }), 200
