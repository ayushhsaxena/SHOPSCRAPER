from flask import Flask, render_template, request
from scraper import deal_find

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():

    query = request.form["query"]

    products = deal_find(query)

    return render_template(
        "results.html",
        products=products,
        query=query
    )


if __name__ == "__main__":
    app.run(debug=True)     