from flask import Flask
import pandas as pd
import json
from sqlalchemy import create_engine
import os

from database import close_db

db_file = 'real-estate.db'
echo_logs = not os.path.exists(db_file)

# Load JSON file in pandas dataframe and create SQLite database
with open("data.json", "r") as file:
    data = json.load(file)

df = pd.DataFrame(data["rentals"])
engine = create_engine('sqlite:///real-estate.db', echo=echo_logs)
df.to_sql('rentals', con=engine, if_exists='replace', index=False)

df2 = pd.DataFrame(data["tenants"])
df2.to_sql('tenants', con=engine, if_exists='replace', index=False)


def create_app():
    app = Flask(__name__)

    app.json.sort_keys = False

    from resources import bp_rentals, bp_tenants, bp_root, bp_chat

    app.register_blueprint(bp_root)
    app.register_blueprint(bp_rentals, url_prefix="/rentals")
    app.register_blueprint(bp_tenants, url_prefix="/tenants")
    app.register_blueprint(bp_chat, url_prefix="/chat")

    app.teardown_appcontext(close_db)

    return app


if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=5000, debug=True)
