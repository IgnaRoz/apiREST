#!/bin/bash

# Nombre del contenedor
CONTAINER_NAME="tokensrv_container"
# Nombre de la imagen
IMAGE_NAME="tokensrv"

# Verificar si el contenedor existe (activo o detenido)
CONTAINER_EXISTS=$(docker ps -a --filter "name=$CONTAINER_NAME" --format "{{.Names}}")

if [ "$CONTAINER_EXISTS" == "$CONTAINER_NAME" ]; then
    # El contenedor ya existe, saliendo...
    echo "El contenedor '$CONTAINER_NAME' ya existe. Saliendo..."
    exit 1
else
    echo "El contenedor '$CONTAINER_NAME' no existe. Creándolo e iniciándolo..."
    docker run -d --rm --name $CONTAINER_NAME -p 3002:3002 --cpus="1" --memory="2g" $IMAGE_NAME
    if [ $? -eq 0 ]; then
        echo "Contenedor '$CONTAINER_NAME' creado e iniciado correctamente."
    else
        echo "Error al crear el contenedor '$CONTAINER_NAME'."
        exit 1
    fi
fi