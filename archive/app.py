"""
Python 3 flask app to summarize text with sumy
"""
from flask import Flask, render_template, request
from sumy.parsers.plaintext import PlaintextParser as pp
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers import *
from sumy.utils import get_stop_words

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def summ():
    text = 'text'
    lang = 'english'
    summary_options = {}

    if request.method == 'POST':
        text = request.form.get('text')
        if text:
            parser = pp.from_string(text, Tokenizer(lang))
            summary_options = {
                n: {'sum': i(), 'summary': i()(parser.document, sentences_count=5)}
                for n, i in {
                    'lex': LexRankSummarizer,
                    'luhn': LuhnSummarizer,
                    'text': TextRankSummarizer,
                    'basic': SumBasicSummarizer,
                    'kls': KLSummarizer,
                    'lsa': LsaSummarizer,
                    'ed': EdmundsonSummarizer
                }.items()
            }
        return render_template('index.html', text=text, summary_options=summary_options)

    return render_template('index.html')
    
if __name__ == '__main__':
    app.run(debug=True)
