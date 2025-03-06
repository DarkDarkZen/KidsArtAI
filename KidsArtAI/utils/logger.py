import logging

def setup_logging():
    """Настройка логирования. В production логи можно отключать или перенаправлять."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    ) 