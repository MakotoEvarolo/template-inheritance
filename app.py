from flask import Flask, render_template, request, url_for, session, redirect, flash
from flask_bootstrap import Bootstrap5 
import mysql.connector

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "plgfat"

users = {}

conn = mysql.connector.connect(
    host='localhost',
    user='root',  
    password='',
    database='notes_db'
)
cursor = conn.cursor()

@app.route('/')
def home():
    return redirect(url_for('sign_up'))


@app.route("/signup")
def sign_up():
    return render_template("authentication/sign_up.html")

@app.route("/signup", methods=["GET", "POST"])
def sign_up_post():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username and password:
            users[username] = password
            return redirect(url_for("login"))
        return "Please provide a username and password."
    return render_template("authentication/sign_up.html")

@app.route("/login")
def login():
    return render_template("authentication/login.html")

@app.route("/login", methods=["GET", "POST"])
def login_post():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if users.get(username) == password:
            session["user"] = username
            return redirect(url_for("index"))
        return "Invalid credentials. Please try again."
    return render_template("authentication/login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/index")
def index():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("User/index.html", username=session["user"])

@app.route('/profile/<string:username>')
def profile(username):
    if username == 'Admin':
        return redirect(url_for('index'))
    return render_template('User/profile.html', username=username)

@app.route('/User/post.html/<int:post_id>')
def post_detail(post_id):
    return render_template("User/post.html", post_id=post_id)

@app.route('/note', methods=['GET', 'POST'])
def note():
    if request.method == 'POST':
        note_title = request.form.get('note_title')
        note_content = request.form.get('note_content')
        
        if note_title and note_content:
            cursor.execute("INSERT INTO notes (note_title, note_content) VALUES (%s, %s)", (note_title, note_content))
            conn.commit()
            flash("Note added successfully.", "success")
        else:
            flash("Both title and content are required.", "danger")
    
    cursor.execute("SELECT * FROM notes ORDER BY note_created DESC")
    notes = cursor.fetchall()
    
    return render_template('User/note.html', notes=notes)

@app.route('/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    if request.method == 'POST':
        note_title = request.form.get("note_title")
        note_content = request.form.get("note_content")
        
        cursor.execute("UPDATE notes SET note_title=%s, note_content=%s WHERE note_id=%s", (note_title, note_content, note_id))
        conn.commit()
        flash("Note Updated.", "success")
        return redirect(url_for('note'))
    
    cursor.execute("SELECT * FROM notes WHERE note_id=%s", (note_id,))
    note = cursor.fetchone()
    return render_template('User/edit_note.html', note=note)

@app.route('/delete/<int:note_id>', methods=['POST'])
def del_note(note_id):
    cursor.execute("DELETE FROM notes WHERE note_id=%s", (note_id,))
    conn.commit()
    flash("Note deleted successfully!", "success")
    return redirect(url_for('note'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)