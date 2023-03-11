import traceback
from time import strftime

from flask import Flask, request, jsonify, make_response, render_template


from summarize.parser.parser import Parser
from summarize.implementation import word_frequency_summarize_parser

# Initialize the Flask application
app = Flask(__name__)


# REST Service methods


@app.route("/")
def index():
    return {"message": "welcome to webpage summarizer"}


@app.route("/summarize", methods=["POST"])
def test():
    content = request.get_json(silent=True, force=True)

    summary = ""

    try:
        web_text = content["html"]

        # Parse it via parser
        parser = Parser()
        parser.feed(web_text)

        # summary = facebook_parser_word_frequency_summarize.run_summarization(parser.paragraphs)
        summary = word_frequency_summarize_parser.run_summarization(parser.paragraphs)

    except Exception as ex:
        app.logger.error(
            "summarize(): error while summarizing: "
            + str(ex)
            + "\n"
            + traceback.format_exc()
        )
        pass

    return make_response(jsonify({"summary": summary}))


if __name__ == "__main__":
    app.run(host="localhost")
