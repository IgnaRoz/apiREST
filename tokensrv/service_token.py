#!/usr/bin/env python3

"""Token service module."""
import secrets
import time
import threading

import requests




TIME_LIVE = 3

class Token:
    """Class representing a token."""

    def __init__(self, username:str, expiration_cb:str):
        """Create a new token."""
        self.__token_hex = secrets.token_hex(16)
        self.__time_destroy = time.time() + TIME_LIVE
        self.__username = username
        self.__expiration_cb = expiration_cb
        self.task_delete = None #borrar?

    @property
    def time_live(self):
        """Return the time to live of the token."""
        return self.__time_destroy - time.time()
    @property
    def token_hex(self):
        """Return the token hex."""
        return self.__token_hex
    @property
    def username(self):
        """Return the username."""
        return self.__username
    @property
    def expiration_cb(self):
        """Return the expiration callback."""
        return self.__expiration_cb

class TokenNotFound(Exception):
    """Raised if given token does not exists."""

    def __init__(self, token: str) -> None:
        """Store affected token."""
        self._tk_ = token

    def __str__(self) -> str:  # pragma: no cover
        """Error description."""
        return f'Invalid token: {self._tk_}'
class Forbidden(Exception):
    """Raised if the user who isn't owner, try to delete it ."""

    def __init__(self, token: str) -> None:
        """Store affected token."""
        self._tk_ = token

    def __str__(self) -> str:  # pragma: no cover
        """Error description."""
        return f'Invalid token: {self._tk_}'

class ServiceToken:
    """Class representing a service of token."""

    def __init__(self, logger):
        """Create a new service of token."""
        self.tokens = {}
        self.logger = logger
        logger.info('Servicio de token iniciado')

    def status_token(self):
        """Return the status of the service."""
        self.logger.info('Servicio de token activo')
        return 'Servicio de token activo'
    def make_token(self, username:str, expiration_cb:str):
        """Create a new token."""
        token = Token(username, expiration_cb)
        self.tokens[token.token_hex] = token

        self.logger.info(f'Token {token.token_hex} creado para {username} con '
                 f'tiempo de vida {token.time_live}')
        #Mas tarde crear un unico hilo que se encargue de borrar los tokens
        # y asegurarme de que no haya problemas de concurrencia
        timer = threading.Timer(token.time_live, self.thread_delete_token, args=(token,))
        timer.start()

        print("")
        return token.token_hex, token.time_live

    def thread_delete_token(self,token):
        """Delete a token."""
        #print(f'Se va a eleminar el token {token.token_hex}en {token.time_live} segundos')
        #time.sleep(token.time_live if token.time_live > 0 else 0)
        #comprobar si se ha ampliado el tiempo de vida y si no se ha eliminado ya
        if token.time_live < 0.1 :
            if token.token_hex in self.tokens:

                del self.tokens[token.token_hex]
            self.logger.info(f'Token {token.token_hex} eliminado')
            if token.expiration_cb:
                response = requests.put(token.expiration_cb,
                                        json={"token": token.token_hex},timeout=2)
                if response.status_code >= 200 & response.status_code < 300:
                    self.logger.info(f'Callback del Token {token.token_hex} '
                                     f'enviado a la direccion {token.expiration_cb} '
                                     f'con codigo de respuesta {response.status_code}')
                else:
                    self.logger.warning(f'Callback del Token {token.token_hex} '
                                        f'ha fallado con codigo {response.status_code}')

    def delete_token(self, token_hex:str, owner:str):
        """Delete a token."""
        if token_hex not in self.tokens:
            raise TokenNotFound(token_hex)
        token = self.tokens[token_hex]
        if token.username != owner:
            raise Forbidden(token)
        del self.tokens[token_hex]


#FALTA LA LLAMADA A AUTH
    def get_token(self, token_hex:str):
        """Return the token info."""
        if token_hex not in self.tokens:
            raise TokenNotFound(token_hex)

        #Llamar al servicio de autenticacion para obtener roles
        username, roles =self.tokens[token_hex].username, ['admin']
        self.logger.info(f'Roles {roles} obtenidos para {username}')
        return username, roles
