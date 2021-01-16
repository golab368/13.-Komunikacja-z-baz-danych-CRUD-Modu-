from flask import Flask, render_template, request
import sqlite3 as sql
from sqlite3 import Error
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():

    return render_template("home.html")

@app.route("/enternew")
def new_student():
    return render_template("add_new_movie.html")

@app.route("/update/<int:movie_id>", methods=["POST", "GET"])
def update(movie_id):
    
    return render_template("update.html", movie_id=movie_id)

@app.route("/add_new_movie", methods=["POST", "GET"])
def add_new_movie():
    if request.method == "POST":
        try:
            movie_title = request.form["movie_title"]
            genres = request.form["genres"]
            with sql.connect("database.db") as db:
                cur = db.cursor()
                cur.execute(
                    "INSERT INTO movies (movie_title,genres) VALUES (?,?)", (movie_title, genres))
                db.commit()
                msg = "Record successfully added"
        except:
            msg = "error in this operation"
            db.rollback()
        finally:
            return render_template("result.html", msg=msg)
            db.close()

@app.route("/updaterec", methods=["POST", "GET"])
def updaterec():
    if request.method == "POST":
        try:
            movie_id = request.form["movie_id"]
            movie_title = request.form["movie_title"]
            genres = request.form["genres"]
            with sql.connect("database.db") as db:
                cur = db.cursor()
                db.execute(f"UPDATE movies SET movie_title = '{movie_title}', genres = '{genres}' WHERE movie_id = {movie_id};")
                db.commit()
                msg = "Record successfully updated"
        except:
            db.rollback()
            msg = "There was a problem updating"
        
        finally:
            return render_template("result.html", msg=msg)
            db.close()

@app.route("/delete/<int:movie_id>", methods=["POST", "GET"])
def delete(movie_id):
    print(movie_id)
    try:
        db = sql.connect("database.db")
        cur = db.cursor()
        db.execute(f"DELETE FROM movies WHERE movie_id = {movie_id};")
        db.commit()
        msg = "Record successfully deleted"
    except:
        db.rollback()
        msg = "There was a problem with delete this movie"

    finally:
        return render_template("result.html", msg=msg)
        db.close()

@app.route("/list_of_movies")
def list_list_of_movies():
    db = sql.connect("database.db")
    db.row_factory = sql.Row
    cur = db.cursor()
    cur.execute("select * from movies")
    rows = cur.fetchall()
    return render_template("list_of_movies.html", rows=rows)

if __name__ == "main":
    app.run(debug=True)
