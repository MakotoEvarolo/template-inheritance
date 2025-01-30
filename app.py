from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5 

app = Flask(__name__)
bootstrap = Bootstrap5(app)

@app.route('/')
def index():
    return render_template('User/index.html')

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