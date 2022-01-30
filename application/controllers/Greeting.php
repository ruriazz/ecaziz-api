<?php
defined('BASEPATH') or exit('No direct script access allowed');

require_once APPPATH.DIRECTORY_SEPARATOR.'controllers/_api_/_base_api.php';

use WarkopDeveloper\CustomCI\BaseAPI;

class Greeting extends BaseAPI
{
    function __construct()
    {
        parent::__construct();
    }

    public function index_get()
    {

    }

    public function index_post()
    {

    }

    public function index_delete()
    {
        
    }
}