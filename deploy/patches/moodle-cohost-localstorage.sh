#!/usr/bin/env bash
#
# Parche: core/storagewrapper de Moodle hace localStorage.clear() cuando el
# jsrev/cache no coincide (validateCache) o cuando se valida la cache
# (storage_validation -> clean()). Este Moodle esta CO-ALOJADO en el MISMO
# ORIGEN que la SPA (el gateway enruta por path: /api/lms), asi que ese
# clear() borra TODO el localStorage del origen, incluidas las claves de
# sesion de la SPA (moodle_token, moodle_userid, ...). Sintoma: al abrir un
# recurso H5P / Moodle Studio el usuario "pierde la sesion" ("Acceso denegado:
# Token invalido o expirado" / "Sesion expirada") aunque acababa de loguearse.
#
# Fix: hacer el limpiador de cache "namespace-aware" -> que borre SOLO las
# claves propias de Moodle (prefijadas "<hash>/..."), que SIEMPRE contienen
# "/". Las claves de la SPA (moodle_token, etc.) no contienen "/", asi que
# sobreviven.
#
# runtime/moodle esta en .gitignore (codigo real montado, no versionado), por
# eso este parche vive aqui y debe RE-APLICARSE tras cualquier re-provision o
# upgrade de Moodle. Es idempotente. Tras aplicarlo, purgar caches para
# bumpear el jsrev:
#   docker exec -u www-data tic-moodle php /var/www/html/admin/cli/purge_caches.php
#
# Uso: deploy/patches/moodle-cohost-localstorage.sh [RUTA_MOODLE]
set -euo pipefail

ROOT="${1:-/srv/kenneth/tic-kenth/runtime/moodle}"
SRC="$ROOT/lib/amd/src/storagewrapper.js"
MIN="$ROOT/lib/amd/build/storagewrapper.min.js"

CLEAROWN_MIN='Wrapper.prototype.clearOwn=function(){for(var i=this.storage.length-1;i>=0;i--){var k=this.storage.key(i);k&&-1!==k.indexOf("/")&&this.storage.removeItem(k)}}'

patch_min() {
  if grep -q "clearOwn" "$MIN"; then echo "[min] ya parcheado"; return; fi
  # validateCache: clear() -> clearOwn() y agregar el metodo clearOwn
  perl -0pi -e 's/config\.jsrev!=cacheVersion&&\(this\.storage\.clear\(\),this\.storage\.setItem\(this\.jsrevPrefix,config\.jsrev\)\);else this\.storage\.setItem\(this\.jsrevPrefix,config\.jsrev\)\}\}/config.jsrev!=cacheVersion&&(this.clearOwn(),this.storage.setItem(this.jsrevPrefix,config.jsrev));else this.storage.setItem(this.jsrevPrefix,config.jsrev)}},'"$CLEAROWN_MIN"'/' "$MIN"
  # clean(): clear() -> clearOwn()
  perl -0pi -e 's/Wrapper\.prototype\.clean=function\(\)\{this\.storage\.clear\(\)\}/Wrapper.prototype.clean=function(){this.clearOwn()}/' "$MIN"
  echo "[min] parcheado"
}

patch_src() {
  [ -f "$SRC" ] || { echo "[src] no existe, omito"; return; }
  if grep -q "clearOwn" "$SRC"; then echo "[src] ya parcheado"; return; fi
  perl -0pi -e 's/(if \(moodleVersion != cacheVersion\) \{\n\s*)this\.storage\.clear\(\);/$1this.clearOwn();/' "$SRC"
  perl -0pi -e 's/    Wrapper\.prototype\.clean = function\(\) \{\n        this\.storage\.clear\(\);\n    \};/    Wrapper.prototype.clearOwn = function() {\n        for (var i = this.storage.length - 1; i >= 0; i--) {\n            var k = this.storage.key(i);\n            if (k \&\& k.indexOf(String.fromCharCode(47)) !== -1) {\n                this.storage.removeItem(k);\n            }\n        }\n    };\n\n    Wrapper.prototype.clean = function() {\n        this.clearOwn();\n    };/' "$SRC"
  echo "[src] parcheado"
}

patch_min
patch_src
echo "Listo. Recuerda purgar caches para bumpear jsrev."
