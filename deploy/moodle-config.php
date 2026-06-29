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

// wwwroot = origen publico SIN subruta. El SPA reescribe ese origen -> /api/lms.
$CFG->wwwroot   = getenv('MOODLE_WWWROOT') ?: 'http://localhost:8090';
$CFG->dataroot  = '/var/moodledata';
$CFG->admin     = 'admin';

$CFG->directorypermissions = 02777;

// Moodle se accede DIRECTO en su propio wwwroot (:8091); NO hay proxy delante de
// ese puerto. reverseproxy=true rompe todo render de pagina (reverseproxyabused)
// cuando Host==wwwroot. El gateway solo proxya /api/lms a moodle:8080 (WS/pluginfile,
// que no exigen wwwroot), asi que false es lo correcto para esta topologia.
$CFG->reverseproxy = false;
$CFG->sslproxy     = (getenv('PUBLIC_SCHEME') === 'https');

require_once(__DIR__ . '/lib/setup.php');

// No hay cierre de tag a proposito.
