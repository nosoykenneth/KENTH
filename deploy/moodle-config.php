<?php  // Moodle config para el contenedor (montado sobre /var/www/html/config.php).
// Reemplaza al config.php de la laptop: apunta a la MariaDB del compose y al
// wwwroot publico (el del gateway). Lee secretos/host por variables de entorno.

unset($CFG);
global $CFG;
$CFG = new stdClass();

$CFG->dbtype    = 'mariadb';
$CFG->dblibrary = 'native';
$CFG->dbhost    = getenv('MOODLE_DB_HOST') ?: 'mariadb';
$CFG->dbname    = getenv('MOODLE_DB_NAME') ?: 'moodle';
$CFG->dbuser    = getenv('MOODLE_DB_USER') ?: 'moodleuser';
$CFG->dbpass    = getenv('MOODLE_DB_PASSWORD') ?: '';
$CFG->prefix    = getenv('MOODLE_DB_PREFIX') ?: 'mdl_';
$CFG->dboptions = array (
  'dbpersist' => 0,
  'dbport'    => (int)(getenv('MOODLE_DB_PORT') ?: 3306),
  'dbsocket'  => '',
  'dbcollation' => 'utf8mb4_unicode_ci',
);

$forwardedhost = $_SERVER['HTTP_X_FORWARDED_HOST'] ?? '';
$forwardedproto = $_SERVER['HTTP_X_FORWARDED_PROTO'] ?? (getenv('PUBLIC_SCHEME') ?: 'http');
$forwardedprefix = rtrim($_SERVER['HTTP_X_FORWARDED_PREFIX'] ?? '', '/');
$directhost = $_SERVER['HTTP_HOST'] ?? '';

$cleanhost = function ($host) {
  $host = trim($host);
  return preg_match('/^[A-Za-z0-9._:-]+$/', $host) ? $host : '';
};

$forwardedhost = $cleanhost($forwardedhost);
$directhost = $cleanhost($directhost);

if ($forwardedhost !== '') {
  $CFG->wwwroot = $forwardedproto . '://' . $forwardedhost . $forwardedprefix;
} else if ($directhost !== '') {
  $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : (getenv('PUBLIC_SCHEME') ?: 'http');
  $CFG->wwwroot = $scheme . '://' . $directhost;
} else {
  $CFG->wwwroot = getenv('MOODLE_WWWROOT') ?: 'http://localhost:8090';
}

$CFG->dataroot  = '/var/moodledata';
$CFG->admin     = 'admin';

$CFG->directorypermissions = 02777;

$CFG->reverseproxy = ($forwardedhost !== '') || filter_var(getenv('MOODLE_REVERSEPROXY'), FILTER_VALIDATE_BOOLEAN);
$CFG->sslproxy     = ($forwardedproto === 'https') || (getenv('PUBLIC_SCHEME') === 'https');

require_once(__DIR__ . '/lib/setup.php');

// No hay cierre de tag a proposito.
