"""Módulo principal de la aplicación."""
# command_handlers
import argparse
import logging
#import service_token as Service_token
from flask import Flask

from tokensrv.service_token import  ServiceToken
from tokensrv import blueprint
from tokensrv.clientAuth import ClientAuth

def setup_logging(name,file, debug=False):
    """Configura el sistema de log."""
    logger = logging.getLogger(name)
    # Configurar el nivel y el formato del log
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(file)
    handler.setFormatter(formatter)
    logger.handlers.clear()
    logger.addHandler(handler)
    if debug:
        handler_debug = logging.StreamHandler()
        handler_debug.setFormatter(formatter)
        logger.addHandler(handler_debug)

    return logger

def make_server(auth):
    """Create the server."""
    app = Flask(__name__, instance_relative_config=True)

    #config = read_config(config_path)
    client_auth = ClientAuth(auth)
    if not client_auth.status():
        print (f'WARNING: No se ha podido conectar con \
               el servicio de autenticación en {auth}')
    app.config["service_auth"] = client_auth

    logger_service = setup_logging("TokenServer_Service",
                                   "tokensrv/logs/TokenServer_Service.log", debug=True)
    logger_blueprint = setup_logging("TokenServer_Blueprint",
                                     "tokensrv/logs/TokenServer_Blueprint.log", debug=True)
    app.config['logger'] = logger_blueprint
    app.config['service_token'] = ServiceToken(logger_service)

    app.register_blueprint(blueprint.token_api)
    #app.run(host=listening, port=port, debug=True)
    return app

def main():
    """Define the main function."""
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
    parser.add_argument(
        '-a', '--auth',
        type=str,
        default="http://127.0.0.1:3000/auth/v1",
        help='Establece la dirección de servicio auth. '
        'Valor por defecto: http://127.0.0.1:3000/auth/v1'
    )


    # Parsear los argumentos
    args = parser.parse_args()

    # Mostrar los valores recibidos
    print(f"Escuchando en {args.listening} en el puerto {args.port}")



    app = make_server(args.auth)
    app.run(host=args.listening, port=args.port, debug=True)
if __name__ == '__main__':
    main()
