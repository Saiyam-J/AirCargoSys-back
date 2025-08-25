from flask import Flask
from app.config import DevelopmentConfig
from app.extensions import db, ma, migrate, init_redis
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions...
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    init_redis(app)

    # Register blueprints
    from app.routes import flights_bp, bookings_bp, booking_events_bp

    app.register_blueprint(flights_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(booking_events_bp)

    # setup logging
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10 * 1024 * 1024, backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
    )
    file_handler.setLevel(logging.INFO)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Application startup")

    return app
