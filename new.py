from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/new")
def new():
  return render_template('new.html', subtitle='Second Page', text = 'This is our second page')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")