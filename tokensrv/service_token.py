import secrets
import time
import threading
import asyncio
import hashlib
import requests
import threading
#!/usr/bin/env python3




TIME_LIVE = 6

class Token:
    def __init__(self, username:str, expiration_cb:str):
        self.__token_hex = secrets.token_hex(16)
        self.__time_destroy = time.time() + TIME_LIVE
        self.__username = username
        self.__expiration_cb = expiration_cb
        self.task_delete = None #borrar?

    @property
    def time_live(self):
        return self.__time_destroy - time.time()
    @property
    def token_hex(self):
        return self.__token_hex
    @property
    def username(self):
        return self.__username
    @property
    def expiration_cb(self):
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

class Service_token:
    def __init__(self, logger):
        
        self.tokens = {}
        self.logger = logger
        logger.info('Servicio de token iniciado')

    def status_token(self):
        self.logger.info('Servicio de token activo')
        return 'Servicio de token activo'
    def make_token(self, username:str, expiration_cb:str):
        
        token = Token(username, expiration_cb)
        self.tokens[token.token_hex] = token

        self.logger.info(f'Token {token.token_hex} creado para {username} con tiempo de vida {token.time_live}')

        #Mas tarde crear un unico hilo que se encargue de borrar los tokens y asegurarme de que no haya problemas de concurrencia
        timer = threading.Timer(token.time_live, self.Thread_delete_token, args=(token,))
        timer.start()

        print("")
        return token.token_hex, token.time_live
    def Thread_delete_token(self,token):
        #print(f'Se va a eleminar el token {token.token_hex}en {token.time_live} segundos')
        #time.sleep(token.time_live if token.time_live > 0 else 0) 
        #comprobar si se ha ampliado el tiempo de vida y si no se ha eliminado ya
        if token.time_live < 0.1 :         
            if token.expiration_cb:
                response = requests.put(token.expiration_cb, json={"token": token.token_hex})
                if response.status_code >= 200 & response.status_code < 300:
                    self.logger.info(f'Callback del Token {token.token_hex} enviado a la direccion {token.expiration_cb} con codigo de respuesta {response.status_code}')
                else:                    
                    self.logger.warning(f'Callback del Token {token.token_hex} ha fallado con codigo {response.status_code}')
            self.delete_token(token.token_hex, token.username)
            self.logger.info(f'Token {token.token_hex} eliminado')
            
        else:
            #print(f'Token {token.token_hex} no eliminado')
            #self.logger.info(f'Token {token.token_hex} no eliminado')
            pass
            
            
    def delete_token(self, token_hex:str, owner:str):
        if token_hex not in self.tokens:
            raise TokenNotFound(token_hex)
        token = self.tokens[token_hex]
        if token.username != owner:
            raise Forbidden(token)
        del self.tokens[token_hex]

    def get_token(self, token_hex:str):
        if token_hex not in self.tokens:
            raise TokenNotFound(token_hex)
        
        #Llamar al servicio de autenticacion para obtener roles
        username, roles =self.tokens[token_hex].username, ['admin']
        self.logger.info(f'Roles {roles} obtenidos para {username}')
        return username, roles




        
