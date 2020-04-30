import os
import csv
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
#app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

print(os.getcwd())


f = open("D:\\project1\\project1\\books.csv")
reader = csv.reader(f)
next(reader)  # skip header

for isbn, title, author, year in reader:
    print (f"Year is {year}" )
    db.execute("INSERT INTO books (Isbn, Title, Author, Year) VALUES (:Isbn, :Title, :Author, :Year)",
    {"Isbn": isbn, "Title": title, "Year": int(year), "Author": author})
    print (f"Added book isbn {isbn} authored by {author}.")
db.commit()



