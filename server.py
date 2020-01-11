from flask import Flask, render_template, request, redirect, session, flash
import re
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "keep it secret"
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route("/")
def index():
    return render_template("/index.html")


@app.route("/create_user", methods=["POST"])
def create_user_in_db():
    is_valid = True
    if len(request.form['fname']) < 2:
    	is_valid = False
    	flash("Enter a first name")

    if len(request.form['lname']) < 2:
    	is_valid = False
    	flash("Enter a last name")

    if len(request.form['email']) < 1:
        is_valid = False
        flash("Enter an email address")

    if len(request.form['password']) < 8:
    	is_valid = False
    	flash("Enter a password of at least 5 characters")

    if request.form['password'] != request.form['confirm_pw']:
    	is_valid = False
    	flash("Password must match confirmation")

    if not EMAIL_REGEX.match(request.form["email"]):
        is_valid = False
        flash("Email format incorrect")

    if is_valid:
        fn = request.form["fname"]
        ln = request.form["lname"]
        em = request.form["email"]
        pw = request.form["password"]
        cpw = request.form["confirm_pw"]
        pw_hash = bcrypt.generate_password_hash(request.form['password'])   
        mysql = connectToMySQL("pyexam")
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(fn)s, %(ln)s, %(em)s, %(password_hash)s, NOW(), NOW())"
        data = {
            "fn": fn,
            "ln": ln,
            "em": em,
            "password_hash": pw_hash
        }
        mysql.query_db(query,data)
        flash("User entry successful!")
    return redirect("/")


@app.route("/login", methods=["POST"])
def user_login():
    mysql = connectToMySQL("pyexam")
    query = "SELECT * FROM users WHERE email = %(em)s;"
    data = { 
        "em" : request.form["email"]
        }
    result = mysql.query_db(query,data)
    if result:
        if bcrypt.check_password_hash(result[0]["password"], request.form["password"]):
            session["user_id"] = result[0]["id"]
            return redirect("thoughts_wall")
    flash("You could not be logged in")
    return redirect("/")


@app.route("/logout")
def log_user_out():
    session.clear()
    return redirect("/")


@app.route("/thought_create", methods=["POST"])
def create_a_thought():
    is_valid = True
    if len(request.form['thought']) > 256:
        is_valid = False
        flash("Thoughts cannot be longer than 255 characters.")
    if len(request.form['thought']) < 1:
        is_valid = False
        flash("Thoughts cannot be shorter than 5 character.")
    if is_valid:
        mysql = connectToMySQL("pyexam")
        query = "INSERT INTO thoughts (author, message, created_at, updated_at) VALUES (%(au)s, %(me)s, NOW(), NOW())"
        data = {
            'au': session["user_id"], 
            'me': request.form["thought"]
        }
        user = mysql.query_db(query, data)
    return redirect("/thoughts_wall")


@app.route("/thoughts_wall")
def successful_login():

    mysql = connectToMySQL("pyexam")
    query = "SELECT * FROM users WHERE id = %(id)s"
    data = {
        "id": session['user_id']
    }
    result = mysql.query_db(query, data)


    mysql = connectToMySQL("pyexam")
    query = "SELECT users.id AS user_id, thoughts.message, thoughts.id AS thought_id, users.first_name, users.last_name FROM thoughts LEFT JOIN users ON thoughts.author = users.id ORDER BY thoughts.created_at DESC;"
    thoughts = mysql.query_db(query)


    mysql = connectToMySQL("pyexam")
    query = "SELECT thought_id, COUNT(thought_id) AS liked FROM users_has_thoughts GROUP BY thought_id;"
    like_count = mysql.query_db(query)


    mysql = connectToMySQL("pyexam")
    query = "SELECT * FROM users_has_thoughts WHERE user_id = %(id)s;"
    data = {
        "id": session["user_id"]
    }
    is_liked = mysql.query_db(query, data)
    liked_messages = []
    for liked in is_liked:
        liked_messages.append(liked["thought_id"])
    return render_template("/thoughts_wall.html", user_info=result[0], thoughts=thoughts, like_count=like_count, liked_messages=liked_messages)


@app.route("/like/<th_id>/")
def like_a_message(th_id):
    mysql = connectToMySQL("pyexam")
    query = "INSERT INTO users_has_thoughts(user_id, thought_id, created_at, updated_at) VALUES (%(uid)s, %(thid)s, NOW(), NOW())"
    data = {
        "uid": session["user_id"],
        "thid": th_id
    }
    mysql.query_db(query, data)
    return redirect("/thoughts_wall")


@app.route("/details/<th_id>/")
def message_details(th_id):

    mysql = connectToMySQL("pyexam")
    query = "SELECT users_has_thoughts.user_id, users.first_name, users.last_name, users_has_thoughts.thought_id FROM users_has_thoughts JOIN users ON users_has_thoughts.user_id = users.id WHERE users_has_thoughts.thought_id = %(thid)s;"
    data = {
        "thid": th_id
    }
    users_who_liked = mysql.query_db(query, data)


    mysql = connectToMySQL("pyexam")
    query = "SELECT users.id AS user_id, thoughts.message, thoughts.created_at, thoughts.id AS thought_id, users.first_name, users.last_name FROM thoughts LEFT JOIN users ON thoughts.author = users.id WHERE thoughts.id = %(thid)s;"
    data = {
        "thid": th_id
    }
    message = mysql.query_db(query, data)
    return render_template("/details.html", users_who_liked=users_who_liked, message=message[0])


@app.route("/unlike/<th_id>/")
def unlike_message(th_id):
    mysql = connectToMySQL("pyexam")
    query = "DELETE FROM users_has_thoughts WHERE user_id = %(uid)s AND thought_id = %(thid)s"
    data = {
        "uid": session["user_id"],
        "thid": th_id
    }
    mysql.query_db(query, data)
    return redirect("/thoughts_wall")

@app.route("/dashboard")
def return_to_dashboard():
    return redirect("/thoughts_wall")

@app.route("/delete_thought/<th_id>/")
def delete_a_thought(th_id):
    query = "DELETE FROM users_has_thoughts WHERE thought_id = %(thid)s"
    data = {
        'thid': th_id
    }
    mysql = connectToMySQL('pyexam')
    mysql.query_db(query, data)

    query = "DELETE FROM thoughts WHERE id = %(thid)s"
    mysql = connectToMySQL('pyexam')
    mysql.query_db(query, data)
    return redirect("/thoughts_wall")

if __name__ == "__main__":
    app.run(debug=True)