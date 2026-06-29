# ============================================================================
#  Moodle 5.0.x corriendo el CODIGO REAL de la laptop (paridad de version).
#  No usamos bitnami: el codigo (incluye local/tesisai y proyecto_curso/
#  api_persistente) se monta como volumen desde ./runtime/moodle.
#  Esta imagen solo aporta PHP 8.3 + Apache + extensiones que Moodle exige.
#  Apache escucha en 8080 para coincidir con el upstream nginx (moodle:8080).
# ============================================================================
FROM php:8.3-apache

# Librerias de sistema para las extensiones PHP que pide Moodle.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpng-dev libjpeg62-turbo-dev libfreetype6-dev \
        libicu-dev \
        libzip-dev \
        libxml2-dev \
        libonig-dev \
        libcurl4-openssl-dev \
        ghostscript \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# Extensiones PHP requeridas/recomendadas por Moodle.
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j"$(nproc)" \
        gd intl zip soap exif opcache mysqli \
    && docker-php-ext-enable opcache

# Apache: rewrite + headers; servir en 8080 (no 80, que lo ocupa el gateway).
RUN a2enmod rewrite headers \
    && sed -ri 's/Listen 80$/Listen 8080/' /etc/apache2/ports.conf \
    && sed -ri 's/:80>/:8080>/' /etc/apache2/sites-available/000-default.conf

COPY deploy/moodle-apache.conf /etc/apache2/conf-available/zzz-moodle.conf
RUN a2enconf zzz-moodle

COPY deploy/moodle-php.ini /usr/local/etc/php/conf.d/zz-moodle.ini

COPY deploy/moodle-entrypoint.sh /usr/local/bin/moodle-entrypoint.sh
RUN chmod +x /usr/local/bin/moodle-entrypoint.sh

EXPOSE 8080
ENTRYPOINT ["/usr/local/bin/moodle-entrypoint.sh"]
