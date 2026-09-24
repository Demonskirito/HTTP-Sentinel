from flask import Flask, request


app = Flask(__name__)


@app.route("/search")
def search():

    keyword = request.args.get("q", "")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>XSS Lab</title>
    </head>

    <body>

        <h1>Local XSS Lab</h1>

        <form method="GET">

            <input
                type="text"
                name="q"
                value="{keyword}"
            >

            <button type="submit">
                Search
            </button>

        </form>

        <p>
            Search result: {keyword}
        </p>

    </body>
    </html>
    """


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )