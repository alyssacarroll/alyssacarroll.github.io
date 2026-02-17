from flask import Flask, redirect, url_for, render_template, request, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "key"

def check_db_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user="root",
            password="password",
            database='mydb'
        )
        return True
    except mysql.connector.Error as e:
        return False

# <><><> MAIN PAGE <><><>
@app.route("/")
def home():
    return render_template("home.html")

# <><><> QUIZ PAGES <><><>
@app.route("/quiz")
def quiz():
    return render_template("quiz_template.html",
                           usr=session.get("user"))


@app.route("/quiz/name", methods=["GET", "POST"])
def name():
    """ asks user for name and stores in session. redirects to weight question page.

    Returns:
        _type_: render_template or redirect
        renders name question page or redirects to weight question page
    """
    if request.method == "POST": # user submits name
        session["user"] = request.form.get("user", "").strip()  # get name from form and store in session
        return redirect(url_for('weight'))  # redirect to weight question page
    return render_template("qName.html", 
                           usr=session.get("user"))

@app.route("/quiz/weight", methods=["GET", "POST"])
def weight():
    """ asks user for weight and stores in session. redirects to results page.
    """
    if request.method == "POST":
        session["weight"] = request.form.get("weight", "").strip()
        return redirect(url_for('caffeine'))
    return render_template("qWeight.html", 
                           usr=session.get("user"))
    
    
@app.route("/quiz/caffeine", methods=["GET", "POST"])
def caffeine():
    if request.method == "POST":
        session["caffeine"] = request.form.get("caffeine", "").strip()
        return redirect(url_for('results'))
    return render_template("qCaffeine.html",
                           usr=session.get("user"))

# TODO: add goals question (pump/energy/endurance)
    
@app.route("/quiz/results", methods=["GET", "POST"])
def results():
    """ displays quiz results. placeholder for future slider adjustment page.
    """
    return render_template("qResults.html",
                            usr=session.get("user"),
                            weight=session.get("weight"),
                            caffeine=session.get("caffeine"))

# TODO: add slider adjustment page

# TODO: add product match page (database)
@app.route("/products")
def products(): 
    # establish connection w/ database
    conn = mysql.connector.connect(
       host="localhost",
       user="root",
       password="password",
       database="preworkout_products"
    )
    cur = conn.cursor(dictionary=True)  # cursor that collects data

    cur.execute("SELECT * FROM preworkout_data")
    products = cur.fetchall()

    # close database connection
    cur.close()
    conn.close()

    return render_template("products.html",
                            products=products,
                            caffeine=session.get("caffeine")
    )

if __name__ == "__main__":
    app.run(debug=True)