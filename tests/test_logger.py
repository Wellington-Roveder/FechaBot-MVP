import logging
import unittest
from unittest.mock import patch

from utils.logger import configurar_logger


class LoggerTests(unittest.TestCase):
    def test_configurar_logger_cria_diretorio_e_retorna_logger(self):
        logger = logging.getLogger("logger-test")
        logger.handlers.clear()
        with (
            patch("utils.logger.os.path.exists", return_value=False) as exists,
            patch("utils.logger.os.makedirs") as makedirs,
            patch("utils.logger.TimedRotatingFileHandler") as handler,
            patch("utils.logger.logging.getLogger", return_value=logger),
        ):
            resultado = configurar_logger()

            self.assertIs(resultado, logger)
            exists.assert_called_once_with("logs")
            makedirs.assert_called_once_with("logs")
            handler.assert_called_once()
            self.assertEqual(logger.level, logging.INFO)


if __name__ == "__main__":
    unittest.main()
