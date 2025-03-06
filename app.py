from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_blueprint
from routes.candidate_routes import candidate_blueprint
from routes.manager_routes import manager_blueprint
from routes.hr_routes import hr_blueprint
from routes.test_routes import test_blueprint
from routes.email_routes import email_blueprint

app = Flask(__name__)
CORS(app)  


app.register_blueprint(auth_blueprint, url_prefix="/api/auth")
app.register_blueprint(candidate_blueprint, url_prefix="/api/candidates")
app.register_blueprint(manager_blueprint, url_prefix="/api/managers")
app.register_blueprint(hr_blueprint, url_prefix="/api/hr")
app.register_blueprint(test_blueprint, url_prefix="/api/exam")
app.register_blueprint(email_blueprint, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)