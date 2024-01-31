from flask import Flask

from app.extensions import database, jwt
from app.routes.personal_info_routes import personal_info_bp

app = Flask(__name__)
app.config.from_pyfile('config.py')

database.init_app(app)
jwt.init_app(app)

app.register_blueprint(personal_info_bp, url_prefix='/recruitment/personal_info')

if __name__ == "__main__":
    app.run(debug=True)
