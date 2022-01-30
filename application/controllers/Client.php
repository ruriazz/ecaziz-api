<?php
defined('BASEPATH') or exit('No direct script access allowed');

require_once APPPATH.DIRECTORY_SEPARATOR.'controllers/_api_/_base_api.php';

use WarkopDeveloper\CustomCI\BaseAPI;

class Client extends BaseAPI
{
    function __construct()
    {
        parent::__construct();

        $this->load->model('Client_model', 'client_model');
    }

	public function index_get()
	{
        $client_id = $this->get_header('client');
        if($client_id) {
            $client_data = $this->client_model->convert()->fromArray([
                "id" => $client_id
            ]);
            if($client_data) {
                $client_data = $client_data->get();
                if($client_data) {
                    $client_data->last_transaction = militime();
                    $client_data->update();
                } else {
                    $client_data = $this->_register();
                }
            } else {
                $client_data = $this->_register();
            }
        } else {
            $client_data = $this->_register();
        }

        $password = $client_data->alias;
        $password = password_hash($password, PASSWORD_BCRYPT);
        $password = Hashing::DataEncryption(HashType::PASSWORD)->encrypt($password);

        echo $password;

        die;

        $this->response_ok([
            "content" => $client_data->convert()->toArray()
        ]);
	}
    
    private function _register() : Client_model
    {
        $this->client_model->alias = Generate::client()->alias();
        $this->client_model->salt = Generate::client()->salt();
        return $this->client_model->save();
    }
}
