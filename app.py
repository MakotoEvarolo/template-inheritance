from flask import Flask, render_template, request, url_for, session, redirect
from flask_bootstrap import Bootstrap5 

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.secret_key = "plgfat"

users = {}

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)