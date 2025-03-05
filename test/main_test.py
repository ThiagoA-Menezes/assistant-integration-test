# syntax: python wrapper.py params.json

# import the Code Engine function: func/__main__.py

import logging
from func.__main__ import main
import sys, json

# NOVO: Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # NOVO: Tratamento de erros ao carregar o arquivo JSON
    try:
        with open(str(sys.argv[1])) as confFile:
            params = json.load(confFile)
        logger.info(f"Loaded params: {params}")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        sys.exit(1)
    except FileNotFoundError:
        logger.error(f"File not found: {sys.argv[1]}")
        sys.exit(1)

    # Invoca a função CE e imprime o resultado
print(main(params))