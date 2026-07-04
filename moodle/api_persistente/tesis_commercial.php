<?php
/**
 * tesis_commercial.php
 * Gestión de metadatos comerciales de los cursos (Precios, Ofertas, Visibilidad).
 * Almacena los datos en un archivo JSON local para máxima portabilidad.
 */
require(__DIR__ . '/../../config.php');
require_once(__DIR__ . '/tesis_lib.php');

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit;
}

$token    = optional_param('token', '', PARAM_ALPHANUM);
$courseid = optional_param('courseid', '', PARAM_RAW); // Puede ser ID firmado o ID directo (dependiendo del contexto)
$action   = optional_param('action', 'get', PARAM_ALPHA);
$filePath = __DIR__ . '/course_commercial.json';

// --- FUNCIONES DE APOYO ---
function load_catalog($path) {
    if (!file_exists($path)) return [];
    $data = json_decode(file_get_contents($path), true);
    return is_array($data) ? $data : [];
}

function save_catalog($path, $data) {
    return file_put_contents($path, json_encode($data, JSON_PRETTY_PRINT));
}

// --- MIGRACIÓN (Si existe el JSON, lo movemos a la DB) ---
if (file_exists($filePath)) {
    $catalog = load_catalog($filePath);
    foreach ($catalog as $cid => $data) {
        kenth_save_commercial_data($cid, $data);
    }
    rename($filePath, $filePath . '.bak');
}

// --- VALIDACIÓN DE TOKEN (Solo para acciones de admin/escritura) ---
$is_admin = false;
if (!empty($token)) {
    $token_record = $DB->get_record('external_tokens', array('token' => $token));
    if ($token_record) {
        $user = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0));
        if ($user) {
            // Verificamos si tiene capacidad de edición global o en algún curso (simplificado para admin)
            $context = context_system::instance();
            if (is_siteadmin($user->id) || has_capability('moodle/course:update', $context, $user->id)) {
                $is_admin = true;
            }
        }
    }
}

// --- LÓGICA DE LA API ---

// 1. OBTENER INFORMACIÓN (Regla 1: Universal / Pública para GET)
if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    // Si se pide un curso específico
    if (!empty($courseid)) {
        // Intentar verificar si es un ID firmado
        $realId = kenth_verify_id($courseid) ?: (int)$courseid;
        $course = $DB->get_record('course', array('id' => $realId), 'id, fullname, shortname, summary', MUST_EXIST);
        $comm = kenth_get_commercial_data($realId);
        
        // Combinamos la data básica de Moodle con la data comercial de nuestra tabla
        $data = array_merge((array)$course, $comm);
        
        // Aseguramos que el ID devuelto sea el firmado para el frontend
        $data['id'] = kenth_sign_id($realId);
        
        // Limpiamos el resumen de Moodle (opcional, pero recomendado para React)
        $data['summary'] = strip_tags($data['summary']);
        
        echo json_encode(['success' => true, 'data' => $data]);
        exit;
    }

    // Listado completo (Ahora universal para todos los cursos visibles)
    $courses = $DB->get_records('course', [], 'fullname ASC', 'id, fullname, shortname');
    $commercial_records = $DB->get_records('kenth_commercial');
    $catalog_by_id = [];
    foreach($commercial_records as $r) $catalog_by_id[$r->courseid] = $r;

    $fullCatalog = [];
    foreach ($courses as $c) {
        if ($c->id == SITEID) continue; // Saltar página principal
        
        $comm = isset($catalog_by_id[$c->id]) ? [
            'price' => (float)$catalog_by_id[$c->id]->price,
            'offer_price' => (float)$catalog_by_id[$c->id]->offer_price,
            'is_visible' => (bool)$catalog_by_id[$c->id]->is_visible
        ] : [
            'price' => 49.99,
            'offer_price' => 0,
            'is_visible' => false
        ];

        // Solo mostramos si es visible, a menos que sea admin
        if (!$is_admin && !$comm['is_visible']) continue;

        $fullCatalog[] = [
            'id' => kenth_sign_id($c->id), // PROTECCIÓN: Enviamos el ID firmado
            'fullname' => $c->fullname,
            'shortname' => $c->shortname,
            'commercial' => $comm
        ];
    }
    echo json_encode(['success' => true, 'data' => $fullCatalog]);
    exit;
}

// 2. ACTUALIZAR INFORMACIÓN (Solo Admin)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!$is_admin) {
        echo json_encode(['success' => false, 'error' => 'No autorizado']);
        exit;
    }

    $input = json_decode(file_get_contents('php://input'), true);
    if (!$input || !isset($input['courseid'])) {
        echo json_encode(['success' => false, 'error' => 'Datos inválidos']);
        exit;
    }

    // Verificar si el ID enviado es firmado o directo
    $cid = kenth_verify_id($input['courseid']) ?: (int)$input['courseid'];
    
    $data = [
        'price' => (float)($input['price'] ?? 49.99),
        'offer_price' => (float)($input['offer_price'] ?? 0),
        'is_visible' => (bool)($input['is_visible'] ?? true)
    ];

    if (kenth_save_commercial_data($cid, $data)) {
        echo json_encode(['success' => true, 'message' => 'Catálogo actualizado en DB']);
    } else {
        echo json_encode(['success' => false, 'error' => 'Error al guardar en base de datos']);
    }
    exit;
}
