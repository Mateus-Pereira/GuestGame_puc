import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from opentelemetry.instrumentation.flask import FlaskInstrumentor

from .controllers.auth_controller import auth_bp
from .controllers.game_controller import game_bp


def create_app(config=None):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    
    CORS(app)
    app.config.update(config or {})
    
    _configure_jwt(app)
    _configure_telemetry(app)
    _register_blueprints(app)
    _register_health_check(app)
    
    return app


def _configure_jwt(app):
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-super-secret-jwt-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
    
    jwt = JWTManager(app)
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({'error': 'Token expirado'}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({'error': 'Token inválido'}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({'error': 'Token de acesso necessário'}), 401


def _configure_telemetry(app):
    FlaskInstrumentor().instrument_app(app)


def _register_blueprints(app):
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')


def _register_health_check(app):
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})
