#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage, State

app = Flask(__name__)


@app.route('/states_list', strict_slashes=False)
def states_list():
    """
    display a HTML page: (inside the tag BODY)
    Returns:
        [str]: HTML page
    """
    states = storage.all(State).values()
    # states = sorted(states, key=lambda state: state.name)
    print(states)  # Add this line for debugging
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def teardown_db(self):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
