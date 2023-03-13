import traceback
from time import strftime

from flask import Flask, request, jsonify, make_response, render_template


from summarize import getSummary as sumy


# Initialize the Flask application
app = Flask(__name__)


# REST Service methods


@app.route("/")
def index():
    return {"message": "welcome to webpage summarizer"}


@app.route("/summarize", methods=["POST"])
def summarize():
    content = request.get_json(silent=True, force=True)
    summary = ""

    try:
        web_url = content["url"]

        summary = sumy.getSummary(web_url)

    except Exception as ex:
        app.logger.error(
            "summarize(): error while summarizing: "
            + str(ex)
            + "\n"
            + traceback.format_exc()
        )
        summary = "invalid web page"
        pass

    return make_response(jsonify({"summary": summary}))


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
