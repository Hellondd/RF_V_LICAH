import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    )
    # Подавляем излишние логи от uvicorn при DEBUG=False (по желанию)