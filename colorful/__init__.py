from flask import Flask, render_template

app = Flask(__name__)

app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.get('/')
def index():
    return render_template("index.html")

@app.get('/register/')
def get_register():
    return render_template("register.html")

@app.get('/login/')
def get_login():
    return render_template("login.html")

@app.get('/about/')
def get_about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)