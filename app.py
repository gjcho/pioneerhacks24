import os

from flask import Flask,  render_template, request

app = Flask(__name__)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-started', methods = ['GET', 'POST'])
def func():
    if request.method == "POST":
       name = request.form.get("name")
       print("Your name is ", name)
       return render_template("index3.html")
    return render_template("index2.html")

# @app.route('/invest', methods = ['GET', 'POST'])
# def func1():
#     return render_template("index3.html")

if __name__ == '__main__':
    app.run(debug=True)
