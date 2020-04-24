# Arcus Read Only PROXY (API Gateway -> Lambda)

![CI](https://github.com/cuenca-mx/arcus-read-only/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage Status](https://coveralls.io/repos/github/cuenca-mx/arcus-read-only/badge.svg?branch=master)](https://coveralls.io/github/cuenca-mx/arcus-read-only?branch=master)


Para preparar tu ambiente de desarrollo:

```bash
cp .chalice/template.config.json .chalice/config.json
make install-dev
```

Para hacer deploy a stage:
```bash
make deploy
```

Para eliminar stage:
```bash
make destroy
```

Para hacer deploy a prod (si tienes los permisos):
```bash
make deploy-prod
```

Para eliminar producción:
```bash
make destroy-prod
```
