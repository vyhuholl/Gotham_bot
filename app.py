from flask import Flask
from flask import request
from flask import render_template
import pickle
import html
import urllib.request
from random import uniform

def unirand(seq):
    sum_, freq_ = 0, 0
    for item, freq in seq:
        sum_ += freq
    rnd = uniform(0, sum_)
    for token, freq in seq:
        freq_ += freq
        if rnd < freq_:
            return token

def generate_sentence(model):
    phrase = ''
    t0, t1 = '$', '$'
    while 1:
        t0, t1 = t1, unirand(model[t0, t1])
        if t1.endswith('$'): break
        if t1.endswith('.') or t1.endswith('?') or t1.endswith('!') or t0.endswith('$'):
            phrase += t1
        else:
            phrase += ' ' + t1
    phrase = phrase.strip(' ')
    return phrase.capitalize()

def unpickle_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

model = unpickle_file('markov_model')

app = Flask(__name__)

@app.route('/127.0.0.1/')

@app.route('/127.0.0.1/<name>')
def main_page(name=None):
    return render_template('main_page.html')

@app.route('/127.0.0.1/reply')
def result_page(name=None):
    if request.args:
        reply = generate_sentence(model)
    return render_template('result_page.html', reply = reply)

if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
