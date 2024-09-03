from flask import Flask, jsonify, render_template, Response, abort, make_response
import sqlite3
import pathlib

app = Flask(__name__)

working_directory = pathlib.Path(__file__).parent.absolute()
DATABASE = working_directory / 'CCL_ecommerce.db'

# @app.route("/")
# def hello():
#     return "Hello, World!"

@app.route("/")
def index() -> str:
    return render_template("dashboard.html")

def query_db(query: str, args=()) -> list:
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        result = cursor.execute(query, args).fetchall()
    return result

@app.route("/api/low_stock_levels")
def low_stock_levels() -> Response:
    query = """
    SELECT p.product_name, s.quantity
    FROM stock_level s
    JOIN products p ON s.product_id = p.product_id
    ORDER BY s.quantity ASC;
    """
    result = query_db(query)

    products = [row[0] for row in result]
    quantities = [row[1] for row in result]
    return jsonify({"products": products, "quantities": quantities})


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)