<?php
// tesis_lib.php - Utilidades de seguridad para Kenth Courses

// SECRETO — NO versionar el valor real (redactado para el repositorio).
// Clave HMAC que firma/verifica los course_id (kenth_sign_id / kenth_verify_id).
// DEBE coincidir EXACTAMENTE con KENTH_COURSE_ID_SECRET del backend FastAPI
// (services/db_service.py::_load_kenth_secret) o las firmas no validarán.
// En el servidor real, define KENTH_COURSE_ID_SECRET en el entorno de Apache/PHP
// (o mantén el valor local fuera del repo). Ver moodle/api_persistente/README.md.
$KENTH_SECRET = getenv('KENTH_COURSE_ID_SECRET') ?: '__DEFINIR_KENTH_COURSE_ID_SECRET__';

/**
 * Firma un ID para que no pueda ser manipulado ni adivinado.
 * Devuelve un token Base64 que contiene el ID y su firma HMAC.
 */
function kenth_sign_id($id) {
    global $KENTH_SECRET;
    if (empty($id)) return null;
    $hash = hash_hmac('sha256', (string)$id, $KENTH_SECRET);
    // Tomamos los primeros 12 caracteres del hash para no hacer la URL excesivamente larga
    $signature = substr($hash, 0, 12);
    return base64_encode($id . '.' . $signature);
}

/**
 * Verifica la firma de un token y devuelve el ID original si es válido.
 */
function kenth_verify_id($token) {
    global $KENTH_SECRET;
    if (empty($token)) return null;
    
    $decoded = base64_decode($token);
    if (!$decoded) return null;
    
    $parts = explode('.', $decoded);
    if (count($parts) !== 2) return null;
    
    $id = $parts[0];
    $signature = $parts[1];
    
    // Calculamos el hash esperado
    $expected_hash = substr(hash_hmac('sha256', (string)$id, $KENTH_SECRET), 0, 12);
    
    if (hash_equals($expected_hash, $signature)) {
        return (int)$id;
    }
    
    return null;
}
// --- GESTIÓN COMERCIAL (TABLA NATIVA) ---

/**
 * Asegura que la tabla mdl_kenth_commercial exista en la BD.
 */
function kenth_ensure_commercial_table() {
    global $DB, $CFG;
    require_once($CFG->libdir . '/ddllib.php');
    $dbman = $DB->get_manager();
    
    // El prefijo lo maneja Moodle automáticamente en get_records,
    // pero aquí usamos el nombre sin prefijo.
    $tablename = 'kenth_commercial';
    $table = new xmldb_table($tablename);

    if (!$dbman->table_exists($table)) {
        $table->add_field('id', XMLDB_TYPE_INTEGER, '10', null, XMLDB_NOTNULL, XMLDB_SEQUENCE, null);
        $table->add_field('courseid', XMLDB_TYPE_INTEGER, '10', null, XMLDB_NOTNULL, null, null);
        $table->add_field('price', XMLDB_TYPE_NUMBER, '10, 2', null, XMLDB_NOTNULL, null, '0.00');
        $table->add_field('offer_price', XMLDB_TYPE_NUMBER, '10, 2', null, XMLDB_NOTNULL, null, '0.00');
        $table->add_field('is_visible', XMLDB_TYPE_INTEGER, '1', null, XMLDB_NOTNULL, null, '1');
        
        $table->add_key('primary', XMLDB_KEY_PRIMARY, array('id'));
        $table->add_index('courseid_idx', XMLDB_INDEX_UNIQUE, array('courseid'));
        
        $dbman->create_table($table);
    }
}

/**
 * Obtiene los datos comerciales de un curso.
 */
function kenth_get_commercial_data($courseid) {
    global $DB;
    kenth_ensure_commercial_table();
    
    $record = $DB->get_record('kenth_commercial', array('courseid' => $courseid));
    if ($record) {
        return [
            'price' => (float)$record->price,
            'offer_price' => (float)$record->offer_price,
            'is_visible' => (bool)$record->is_visible
        ];
    }
    
    // Valores por defecto
    return [
        'price' => 49.99,
        'offer_price' => 0,
        'is_visible' => false
    ];
}

/**
 * Guarda los datos comerciales de un curso.
 */
function kenth_save_commercial_data($courseid, $data) {
    global $DB;
    kenth_ensure_commercial_table();
    
    $record = $DB->get_record('kenth_commercial', array('courseid' => $courseid));
    
    $newdata = new stdClass();
    $newdata->courseid = $courseid;
    $newdata->price = $data['price'] ?? 49.99;
    $newdata->offer_price = $data['offer_price'] ?? 0;
    $newdata->is_visible = !empty($data['is_visible']) ? 1 : 0;
    
    if ($record) {
        $newdata->id = $record->id;
        return $DB->update_record('kenth_commercial', $newdata);
    } else {
        return $DB->insert_record('kenth_commercial', $newdata);
    }
}
