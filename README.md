[![Tests](https://github.com/IgnaRoz/apiREST/actions/workflows/tests.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/tests.yml)
[![Tests integracion](https://github.com/IgnaRoz/apiREST/actions/workflows/testsIntegracion.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/testsIntegracion.yml)
[![Linters](https://github.com/IgnaRoz/apiREST/actions/workflows/linters.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/linters.yml)
[![Type checking](https://github.com/IgnaRoz/apiREST/actions/workflows/typechecking.yml/badge.svg)](https://github.com/IgnaRoz/apiREST/actions/workflows/typechecking.yml)

# Token Service for ADI 2024-2025

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```

## Execution

To run the server, just install the package and run

```
token_service
```

## Running tests and linters locally

If you want to run the tests and/or linters, you need to install the dependencies for them:

- To install test dependencies: `pip install .[tests]`
- To install linters dependencies: `pip install .[linters]`

All the tests runners and linters are configured in the `pyproject.toml`.

## Kubernetes

### Requisitos

- Tener instalado Kubernetes.
- Tener las imágenes de los servicios `tokensrv` y `authsrv` construidas usando el script `build`.
- El servicio authsrv se puede obtener del repositorio: https://github.com/luisbl03/Authentication.git (probado con el tag "entregable2")

Para desplegar los servicios `tokensrv` y `authsrv` en Kubernetes, sigue estos pasos:

1. **Aplicar los archivos YAML** para `tokensrv` y `authsrv` que se encuentran en la carpeta `kubernetes`.

    ```sh
    kubectl apply -f .\\kubernetes\\srv-tokensrv.yaml
    kubectl apply -f .\\kubernetes\\srv-authsrv.yaml
    ```

2. **Verificar los despliegues y servicios**:
    ```sh
    kubectl get deployments
    kubectl get services
    ```

3. **Ver logs de los servicios**:
    ```sh
    kubectl logs --follow deployment/tokensrv-deployment
    kubectl logs --follow deployment/authsrv-deployment
    ```

4. **Configurar port-forwarding** para acceder a los servicios localmente:
    ```sh
    kubectl port-forward service/tokensrv-service 3002:3002
    kubectl port-forward service/authsrv-service 3001:3001
    ```
