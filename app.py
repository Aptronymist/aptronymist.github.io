"""
Python 3 flask app to summarize text with sumy
"""
from flask import Flask, request, render_template
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.kl import KLSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.edmundson import EdmundsonSummarizer
from sumy.utils import get_stop_words

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def summarize():
    if request.method == "POST":
        text = request.form["text"]
        lang = "english"
        parser = PlaintextParser.from_string(text, Tokenizer(lang))

        summarizers = {
            "lexrank": LexRankSummarizer,
            "luhn": LuhnSummarizer,
            "textrank": TextRankSummarizer,
            "sumbasic": SumBasicSummarizer,
            "kls": KLSummarizer,
            "lsa": LsaSummarizer,
            "edmundson": EdmundsonSummarizer,
        }

        summary_options = {}
        for summarizer_name, summarizer_class in summarizers.items():
            summary_options[summarizer_name] = {}
            summarizer = summarizer_class()
            summarizer.stop_words = get_stop_words(lang)
            summary_options[summarizer_name]["summarizer"] = summarizer
            summary_options[summarizer_name]["summary"] = summarizer(
                parser.document, sentences_count=5
            )

        return render_template("index.html", text=text, summary_options=summary_options)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
