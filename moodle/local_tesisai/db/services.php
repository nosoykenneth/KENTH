<?php
$functions = array(
    'local_tesisai_ask_ollama' => array(
        'classname'   => 'local_tesisai_external',
        'methodname'  => 'ask_ollama',
        'classpath'   => 'local/tesisai/externallib.php',
        'description' => 'Recibe prompt de React, consulta a Ollama y devuelve texto.',
        'type'        => 'read',
        'ajax'        => true,
    ),
    'local_tesisai_create_label' => array(
        'classname'   => 'local_tesisai_external',
        'methodname'  => 'create_label',
        'classpath'   => 'local/tesisai/externallib.php',
        'description' => 'Crea un recurso de tipo Etiqueta en un curso especifico',
        'type'        => 'write',
        'ajax'        => true,
    ),
    'local_tesisai_get_permissions' => array(
        'classname'   => 'local_tesisai_external',
        'methodname'  => 'get_permissions',
        'classpath'   => 'local/tesisai/externallib.php',
        'description' => 'Devuelve flags de capabilities (autorizacion) para (usuario, curso)',
        'type'        => 'read',
        'ajax'        => true,
    )
);