<?php
// tesis_profile.php - Gestion de datos de usuario (GET para leer, POST para actualizar)
require(__DIR__ . '/../../config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/gdlib.php');

header('Content-Type: application/json');

function tesis_profile_original_dir() {
    global $CFG;
    $dir = $CFG->dataroot . '/tesis_profile_originals';
    if (!is_dir($dir)) {
        make_writable_directory($dir);
    }
    return $dir;
}

function tesis_profile_original_path($userid) {
    return tesis_profile_original_dir() . '/user_' . (int)$userid . '.png';
}

function tesis_profile_original_url($userid, $token) {
    global $CFG;
    $path = tesis_profile_original_path($userid);
    if (!is_readable($path)) {
        return '';
    }

    return $CFG->wwwroot . '/proyecto_curso/api_persistente/tesis_profile.php?token=' . rawurlencode($token) . '&action=original&rev=' . filemtime($path);
}

function tesis_profile_save_original($userid, $imageDataUrl) {
    if (empty($imageDataUrl)) {
        return;
    }

    $img_base64 = preg_replace('#^data:image/\w+;base64,#i', '', $imageDataUrl);
    $img_data = base64_decode($img_base64);

    if ($img_data === false) {
        throw new Exception('La imagen original enviada no es base64 valido.');
    }

    if (@getimagesizefromstring($img_data) === false) {
        throw new Exception('La imagen original enviada no es una imagen valida.');
    }

    file_put_contents(tesis_profile_original_path($userid), $img_data);
}

function tesis_profile_get_crop_state($userid) {
    $raw = get_user_preferences('tesis_profile_crop_state', '', $userid);
    if (empty($raw)) {
        return null;
    }

    $decoded = json_decode($raw);
    return $decoded ?: null;
}

function tesis_profile_save_crop_state($userid, $cropState) {
    if (empty($cropState)) {
        return;
    }

    set_user_preference('tesis_profile_crop_state', json_encode($cropState), $userid);
}
$token  = required_param('token', PARAM_ALPHANUM);
$action = optional_param('action', 'get', PARAM_ALPHA);

// 1. Validar Token y Sesion
$token_record = $DB->get_record('external_tokens', array('token' => $token));
if (!$token_record) {
    echo json_encode(['success' => false, 'error' => 'Token invalido']);
    exit;
}
$user = $DB->get_record('user', array('id' => $token_record->userid, 'deleted' => 0), '*', MUST_EXIST);
complete_user_login($user);

// --- ACCION: SERVIR IMAGEN ORIGINAL PARA RECORTE ---
if ($action === 'original') {
    $path = tesis_profile_original_path($user->id);
    if (!is_readable($path)) {
        http_response_code(404);
        echo json_encode(['success' => false, 'error' => 'Imagen original no encontrada']);
        exit;
    }

    $imageinfo = @getimagesize($path);
    $mimetype = !empty($imageinfo['mime']) ? $imageinfo['mime'] : 'image/png';

    header('Content-Type: ' . $mimetype, true);
    header('Access-Control-Allow-Origin: *');
    header('Content-Length: ' . filesize($path));
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    readfile($path);
    exit;
}

// --- ACCION: OBTENER DATOS DEL PERFIL ---
if ($action === 'get') {
    // Generar la URL segura de la foto de perfil para React
    $context = context_user::instance($user->id);
    $pictureurl = '';
    if ($user->picture > 0) {
        $pictureurl = $CFG->wwwroot . '/webservice/pluginfile.php/' . $context->id . '/user/icon/moodle/f1?rev=' . $user->picture;
    } else {
        $pictureurl = $CFG->wwwroot . '/theme/image.php/boost/core/1/u/f1';
    }

    echo json_encode([
        'success' => true,
        'data' => [
            'firstname'          => $user->firstname,
            'lastname'           => $user->lastname,
            'email'              => $user->email,
            'city'               => $user->city,
            'country'            => $user->country,
            'description'        => $user->description,
            'pictureurl'         => $pictureurl,
            'originalpictureurl' => tesis_profile_original_url($user->id, $token),
            'picturecropstate'   => tesis_profile_get_crop_state($user->id)
        ]
    ]);
    exit;
}

// --- ACCION: ACTUALIZAR DATOS ---
if ($action === 'update' && $_SERVER['REQUEST_METHOD'] === 'POST') {
    $json = file_get_contents('php://input');
    $data = json_decode($json);

    if (!$data) {
        echo json_encode(['success' => false, 'error' => 'Datos no recibidos']);
        exit;
    }

    // 1. ACTUALIZAMOS LOS DATOS DE TEXTO
    $user_to_update = new stdClass();
    $user_to_update->id          = $user->id;
    $user_to_update->firstname   = clean_param($data->firstname, PARAM_TEXT);
    $user_to_update->lastname    = clean_param($data->lastname, PARAM_TEXT);
    $user_to_update->email       = clean_param($data->email, PARAM_EMAIL);
    $user_to_update->city        = clean_param($data->city, PARAM_TEXT);
    $user_to_update->country     = strtoupper(clean_param($data->country, PARAM_ALPHA));
    $user_to_update->description = clean_param($data->description, PARAM_RAW);

    try {
        // Guardamos los datos de texto primero
        user_update_user($user_to_update, false, false);

        if (!empty($data->pictureOriginalData)) {
            tesis_profile_save_original($user->id, $data->pictureOriginalData);
        }

        if (!empty($data->pictureCropState)) {
            tesis_profile_save_crop_state($user->id, $data->pictureCropState);
        }
        
        // 2. PROCESAMOS LA IMAGEN (si el usuario selecciono una nueva)
        if (!empty($data->pictureData)) {
            $img_base64 = preg_replace('#^data:image/\w+;base64,#i', '', $data->pictureData);
            $img_data = base64_decode($img_base64);
            
            // Usamos la carpeta temporal de Moodle
            $temp_dir = make_temp_directory('tesis_profile');
            $temp_file = $temp_dir . '/avatar_' . $user->id . '_' . time() . '.png';
            file_put_contents($temp_file, $img_data);
            
            // Moodle recorta la imagen, la vuelve cuadrada (100x100) y la guarda
            $context = context_user::instance($user->id);
            process_new_icon($context, 'user', 'icon', 0, $temp_file);
            
            // Actualizamos la columna 'picture' en la DB para activar la foto y romper la cache
            $DB->set_field('user', 'picture', time(), array('id' => $user->id));
            
            // Borramos el archivo temporal
            @unlink($temp_file);
        }

        // 3. OBTENER LA NUEVA URL SEGURA PARA REACT
        $updated_user = $DB->get_record('user', array('id' => $user->id));
        $context = context_user::instance($user->id);
        
        $new_picture_url = '';
        if ($updated_user->picture > 0) {
            // Utilizamos webservice/pluginfile.php para que soporte el ?token=
            $new_picture_url = $CFG->wwwroot . '/webservice/pluginfile.php/' . $context->id . '/user/icon/moodle/f1?rev=' . $updated_user->picture;
        } else {
            // Foto por defecto si falla
            $new_picture_url = $CFG->wwwroot . '/theme/image.php/boost/core/1/u/f1';
        }

        echo json_encode([
            'success' => true, 
            'message' => 'Perfil actualizado',
            'newfullname' => $user_to_update->firstname . ' ' . $user_to_update->lastname,
            'newpictureurl' => $new_picture_url,
            'originalpictureurl' => tesis_profile_original_url($user->id, $token),
            'picturecropstate'   => tesis_profile_get_crop_state($user->id)
        ]);
    } catch (Exception $e) {
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
    }
    exit;
}




