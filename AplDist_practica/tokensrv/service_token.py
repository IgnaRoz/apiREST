import secrets
import time
import threading
import asyncio
import hashlib
#!/usr/bin/env python3




TIME_LIVE = 6

class Token:
    def __init__(self, username:str):
        self.__token_hex = secrets.token_hex(16)
        self.__time_destroy = time.time() + TIME_LIVE
        self.username = username
        self.task_delete = None

    @property
    def time_live(self):
        return self.__time_destroy - time.time()
    @property
    def token_hex(self):
        return self.__token_hex
    
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
    def make_token(self, username:str):
        
        token = Token(username)
        self.tokens[token.token_hex] = token

        self.logger.info(f'Token {token.token_hex} creado para {username} con tiempo de vida {token.time_live}')

        #Mas tarde crear un unico hilo que se encargue de borrar los tokens y asegurarme de que no haya problemas de concurrencia
        threading.Thread(target=self.Thread_delete_token, args=(token,)).start()

        print("")
        return token.token_hex, token.time_live
    def Thread_delete_token(self,token):
        #print(f'Se va a eleminar el token {token.token_hex}en {token.time_live} segundos')
        time.sleep(token.time_live if token.time_live > 0 else 0) 
        #comprobar si se ha ampliado el tiempo de vida y si no se ha eliminado ya
        if token.time_live < 0.1 :         
            self.delete_token(token.token_hex)
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
        self.logger.info(f'Token {token_hex} eliminado')

    def get_token(self, token_hex:str):
        if token_hex not in self.tokens:
            raise TokenNotFound(token_hex)
        
        #Llamar al servicio de autenticacion para obtener roles
        username, roles =self.tokens[token_hex].username, ['admin']
        self.logger.info(f'Roles {roles} obtenidos para {username}')
        return username, roles




        
