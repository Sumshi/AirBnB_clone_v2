#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask
from flask import render_template
from models import storage
from models.state import State
from models.city import City

app = Flask(__name__, template_folder='templates')


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """
    display a HTML page: (inside the tag BODY)
    funtcion is executed url:port/cities_by_states is requested
    Returns:
        [str]: HTML page
    """
    states = list(storage.all("State").values())
    # states = sorted(states, key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def teardown_db(self):
    """
    remove the current SQLAlchemy Session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
