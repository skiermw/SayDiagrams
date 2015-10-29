from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from readgraph import get_graph_json, get_domain_json

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/integration')
def integration():
    graph_json = get_graph_json()
    return render_template('integration.html')

@app.route('/domains')
def domains():
    graph_json = get_domain_json()
    return render_template('domains.html')


if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0')
