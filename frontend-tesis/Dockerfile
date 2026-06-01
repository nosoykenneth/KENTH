# Build estatico del SPA.
# El bundle resultante en /app/dist se copia al volumen compartido en el arranque del compose
# para que el gateway nginx lo sirva.
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
# npm install (no npm ci) porque el lockfile suele estar generado en Windows
# y faltan deps opcionales especificas de Linux (ej. @emnapi/runtime).
RUN npm install --no-audit --no-fund

COPY . .
RUN npm run build

FROM alpine:3.20

RUN apk add --no-cache bash

WORKDIR /app
COPY --from=builder /app/dist /app/dist

# El compose monta el volumen 'frontend_build' en /shared y copiamos el bundle ahi.
CMD ["sh", "-c", "rm -rf /shared/* && cp -r /app/dist/. /shared/ && echo 'Frontend build copiado al volumen compartido.' && tail -f /dev/null"]
