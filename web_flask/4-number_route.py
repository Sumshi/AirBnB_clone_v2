#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    display Hello HBNB!
    Returns:
        [str]: Hello HBNB!
    run the script on local server ip address and port 5000
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    display HBNB
    Returns:
        [str]: HBNB
    run the script on local server ip address and port 5000
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_route(text):
    """
    display C followed by the value of the text variable
    Returns:
        [str]: C <text>
    run the script on local server ip address and port 5000
    """
    return "C {}".format(text.replace("_", " "))


@app.route('/python/<text>', strict_slashes=False)
@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
def python_route(text):
    """
    display Python followed by the value of the text variable
    Returns:
        [str]: Python <text>
    run the script on local server ip address and port 5000
    """
    return "Python {}".format(text.replace("_", " "))


@app.route('/number/<int:n>', strict_slashes=False)
def number_route(n):
    """
    display n is a number only if n is an integer
    Returns:
        [str]: n is a number
    run the script on local server ip address and port 5000
    """
    return "{} is a number".format(n)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
