from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single')
    data = r.json()
    j = data['joke']
    cat = data['category']
    return render_template('index.html', joke=j, category=cat)

@app.route('/new')
def new_joke():
    r = requests.get('https://v2.jokeapi.dev/joke/Any?type=single')
    data = r.json()
    j = data['joke']
    cat = data['category']
    return render_template('index.html', joke=j, category=cat)

if __name__ == '__main__':
    app.run(debug=True)
