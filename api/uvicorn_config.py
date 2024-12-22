import logging

logger = logging.getLogger(__name__)

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "use_colors": True},
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "format": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {"formatter": "default", "class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
        "access_stream": {"formatter": "access", "class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
        "access_file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/access.log",
            "mode": "a",
        },
        "error_file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/error.log",
            "mode": "a",
        },
        "app_file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "logs/uvicorn.log",
            "mode": "a",
        },
    },
    "loggers": {
        "uvicorn": {"level": "INFO", "handlers": ["default", "app_file"], "propagate": False},
        "uvicorn.error": {"level": "ERROR", "handlers": ["error_file"], "propagate": False},
        "uvicorn.access": {"level": "INFO", "handlers": ["access_stream", "access_file"], "propagate": False},
    },
}


uvicorn_configuration = {
    "host": "0.0.0.0",
    "port": 8000,
    "loop": "uvloop",
    "http": "auto",
    "ws": "websockets",
    "ws_max_size": 4 * 1024 * 1024,
    "ws_max_queue": 32,
    "ws_ping_interval": 20.0,
    "ws_ping_timeout": 20.0,
    "ws_per_message_deflate": True,
    "timeout_graceful_shutdown": 30,
    "lifespan": "auto",
    "timeout_keep_alive": 10,
    "interface": "asgi3",
    "reload": True,
    "reload_delay": 0.25,
    "workers": 1,
    "proxy_headers": True,
    "server_header": True,
    "date_header": True,
    "forwarded_allow_ips": ["*"],
    "log_config": logging_config,
}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="config.asgi:application",
        **uvicorn_configuration,
    )
