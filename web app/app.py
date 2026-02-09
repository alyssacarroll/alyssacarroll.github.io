from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# <><><> MAIN PAGE <><><>
@app.route("/")
def home():
    return render_template("home.html", content="testing")


@app.route("/quiz")
def test():
    return render_template("quiz_template.html")

@app.route("/quiz/name")
def quiz_name():
    return render_template("quiz_name.html")

if __name__ == "__main__":
    app.run(debug=True)