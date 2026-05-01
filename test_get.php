<?php
define('CLI_SCRIPT', true);
$_GET['token'] = '91d0f0ab6abdb68d897bb0f05650dfa8';
$_GET['courseid'] = 2;
$_GET['action'] = 'get';
$_REQUEST = $_GET;

$_SERVER['REQUEST_METHOD'] = 'GET';
$_SERVER['SERVER_PROTOCOL'] = 'HTTP/1.1';
$_SERVER['HTTP_HOST'] = 'localhost';
$_SERVER['SCRIPT_NAME'] = '/proyecto_curso/api_persistente/tesis_course_settings.php';

require('C:\Moodle\server\moodle\proyecto_curso\api_persistente\tesis_course_settings.php');
