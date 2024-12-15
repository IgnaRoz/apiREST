FROM python:3.10

# Crea un usuario no root
RUN useradd -m appuser

COPY ./tokensrv /tokensrv
COPY pyproject.toml /
COPY requirements.txt /


RUN pip install .
RUN pip install -r requirements.txt

# Cambia los permisos para el usuario
RUN chown -R appuser /tokensrv

# Cambia al usuario creado
USER appuser

EXPOSE 3002

CMD ["python", "/tokensrv/command_handlers.py","-a","http://192.168.1.100:3000/auth/v1"]

