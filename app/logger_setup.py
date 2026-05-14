import logging


def setup_logging():
    # Simple local logging that won't crash your app
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    return logging.getLogger("app_logger")
