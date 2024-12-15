#!/bin/bash

# Nombre del contenedor
CONTAINER_NAME="tokensrv_container"

# Verificar si el contenedor está corriendo
CONTAINER_RUNNING=$(docker ps --filter "name=$CONTAINER_NAME" --format "{{.Names}}")

if [ "$CONTAINER_RUNNING" == "$CONTAINER_NAME" ]; then
    echo "El contenedor '$CONTAINER_NAME' está en ejecución. Deteniéndolo..."
    docker stop $CONTAINER_NAME
    if [ $? -eq 0 ]; then
        echo "Contenedor '$CONTAINER_NAME' detenido correctamente."
    else
        echo "Error al detener el contenedor '$CONTAINER_NAME'."
        exit 1
    fi
else
    echo "El contenedor '$CONTAINER_NAME' no está en ejecución o no existe."
fi
