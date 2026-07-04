<?php
// api_onboarding_process.php
require_once(__DIR__ . '/../../config.php');
require_once($CFG->dirroot . '/user/lib.php');
require_once($CFG->libdir . '/gdlib.php');

header('Content-Type: application/json; charset=utf-8');

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

function tesis_profile_save_crop_state($userid, $cropStateJson) {
    if (empty($cropStateJson)) {
        return;
    }

    $decoded = json_decode($cropStateJson);
    if (!$decoded) {
        return;
    }

    set_user_preference('tesis_profile_crop_state', json_encode($decoded), $userid);
}
$token = required_param('token', PARAM_ALPHANUM);
$firstname = required_param('firstname', PARAM_TEXT);
$lastname = required_param('lastname', PARAM_TEXT);
$password = optional_param('password', '', PARAM_RAW);
$pictureData = optional_param('pictureData', '', PARAM_RAW);
$pictureOriginalData = optional_param('pictureOriginalData', '', PARAM_RAW);
$pictureCropState = optional_param('pictureCropState', '', PARAM_RAW);

global $DB, $CFG;

try {
    $token_record = $DB->get_record('external_tokens', ['token' => $token], '*', MUST_EXIST);
    $user = $DB->get_record('user', ['id' => $token_record->userid, 'deleted' => 0], '*', MUST_EXIST);

    // 1) Actualizar datos basicos
    $user_to_update = new stdClass();
    $user_to_update->id = $user->id;
    $user_to_update->firstname = clean_param($firstname, PARAM_TEXT);
    $user_to_update->lastname = clean_param($lastname, PARAM_TEXT);

    if (!empty($password)) {
        $user_to_update->password = hash_internal_user_password($password);
    }

    user_update_user($user_to_update, false, false);

    if (!empty($pictureOriginalData)) {
        tesis_profile_save_original($user->id, $pictureOriginalData);
    }

    if (!empty($pictureCropState)) {
        tesis_profile_save_crop_state($user->id, $pictureCropState);
    }

    // 2) Procesar foto igual que en tesis_profile.php
    if (!empty($pictureData)) {
        $img_base64 = preg_replace('#^data:image/\w+;base64,#i', '', $pictureData);
        $img_data = base64_decode($img_base64);

        if ($img_data === false) {
            throw new Exception('La imagen enviada no es base64 valido.');
        }

        $temp_dir = make_temp_directory('tesis_profile');
        $temp_file = $temp_dir . '/avatar_' . $user->id . '_' . time() . '.png';
        file_put_contents($temp_file, $img_data);

        $context = context_user::instance($user->id);
        process_new_icon($context, 'user', 'icon', 0, $temp_file);

        // Forzar refresh de cache igual que el endpoint que si funciona
        $DB->set_field('user', 'picture', time(), ['id' => $user->id]);

        @unlink($temp_file);
    }

    // 3) Obtener nueva URL de foto
    $updated_user = $DB->get_record('user', ['id' => $user->id], '*', MUST_EXIST);
    $context = context_user::instance($user->id);

    if ($updated_user->picture > 0) {
        $new_picture_url = $CFG->wwwroot . '/webservice/pluginfile.php/' . $context->id . '/user/icon/moodle/f1?rev=' . $updated_user->picture;
    } else {
        $new_picture_url = $CFG->wwwroot . '/theme/image.php/boost/core/1/u/f1';
    }

    // 4) Limpiar bandera de onboarding
    unset_user_preference('kenth_requires_onboarding', $user->id);

    echo json_encode([
        'success' => true,
        'message' => 'Perfil actualizado correctamente',
        'newfullname' => $updated_user->firstname . ' ' . $updated_user->lastname,
        'newpictureurl' => $new_picture_url,
        'originalpictureurl' => tesis_profile_original_url($user->id, $token),
        'picturecropstate' => tesis_profile_get_crop_state($user->id)
    ], JSON_UNESCAPED_UNICODE);

} catch (Throwable $e) {
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ], JSON_UNESCAPED_UNICODE);
}


