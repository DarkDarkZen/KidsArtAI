import logging


def setup_logging(level=logging.INFO):
    """Настраивает базовое логирование с указанным уровнем логов."""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )


if __name__ == '__main__':
    setup_logging()
    logging.info('Логирование настроено!') 