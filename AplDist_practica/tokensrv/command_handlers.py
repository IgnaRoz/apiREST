# command_handlers
import argparse

#import service_token as Service_token 
from flask import Flask, request, jsonify

from service_token import  Service_token
import blueprint
from service_token import Token
import logging

def setup_logging(name,file, debug=False):

    logger = logging.getLogger(name)
    # Configurar el nivel y el formato del log
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(file)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if debug:
        handler_debug = logging.StreamHandler()
        handler_debug.setFormatter(formatter)
        logger.addHandler(handler_debug)

    return logger

def run_server(listening, port):
    app = Flask(__name__, instance_relative_config=True)

    logger_service = setup_logging("TokenServer_Service", "TokenServer_Service.log", debug=True)
    logger_blueprint = setup_logging("TokenServer_Blueprint", "TokenServer_Blueprint.log", debug=True)
    app.config['logger'] = logger_blueprint
    app.config['service_token'] = Service_token(logger_service)

    app.register_blueprint(blueprint.token_api)
    app.run(host=listening, port=port, debug=True)

if __name__ == '__main__':
 # Crear el parser para los argumentos
    parser = argparse.ArgumentParser(description="Levanta un servidor de tokens")

    # Agregar los argumentos de puerto y dirección de escucha
    parser.add_argument(
        '-p', '--port', 
        type=int, 
        default=3002, 
        help='Establece el puerto de escucha. Valor por defecto: 3002'
    )
    parser.add_argument(
        '-l', '--listening', 
        type=str, 
        default="0.0.0.0", 
        help='Establece la dirección de escucha. Valor por defecto: 0.0.0.0'
    )

    # Parsear los argumentos
    args = parser.parse_args()

    # Mostrar los valores recibidos
    print(f"Escuchando en {args.listening} en el puerto {args.port}")



    run_server(args.listening, args.port)
