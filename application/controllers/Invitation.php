<?php
defined('BASEPATH') or exit('No direct script access allowed');

require_once APPPATH.DIRECTORY_SEPARATOR.'controllers/_api_/_base_api.php';

use WarkopDeveloper\CustomCI\BaseAPI;

class Invitation extends BaseAPI
{
    function __construct()
    {
        parent::__construct();
    }

	public function index_get()
	{
		$requestData = $this->special_get('key, value');

        $id = Hashing::Id()->encode(26);
        $decoded = Hashing::Id()->decode($id);
		
        $this->response_ok(['content' => ["encode" => $id, "decoded" => $decoded]]);
	}

    public function index_post()
    {

    }

    public function index_put()
    {

    }

    public function index_patch()
    {

    }

    public function index_delete()
    {
        
    }
}
