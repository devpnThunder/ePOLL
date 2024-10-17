from flask import jsonify
from flask_wtf.csrf import CSRFError

from app.extensions import db


def register_error_handlers(app):
    """
    Register error handlers for the application.
    """

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify(
            {"success": False, "message": "Bad Request", "details": str(error)}
        ), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify(
            {"success": False, "message": "Unauthorized", "details": str(error)}
        ), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify(
            {"success": False, "message": "Forbidden", "details": str(error)}
        ), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify(
            {"success": False, "message": "Not Found", "details": str(error)}
        ), 404

    @app.errorhandler(422)
    def unprocessable_entity_error(error):
        return jsonify(
            {"success": False, "message": "Unprocessable Entity", "details": str(error)}
        ), 422

    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify(
            {
                "success": False,
                "message": "Rate Limit Exceeded",
                "details": error.description,
            }
        ), 429

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error):
        return jsonify(
            {"success": False, "message": "CSRF Error", "details": error.description}
        ), 400

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify(
            {
                "success": False,
                "message": "Internal Server Error",
                "details": str(error),
            }
        ), 500