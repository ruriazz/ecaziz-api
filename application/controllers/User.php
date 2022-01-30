<?php
defined('BASEPATH') or exit('No direct script access allowed');

require_once APPPATH.DIRECTORY_SEPARATOR.'controllers/_api_/_base_api.php';

use WarkopDeveloper\CustomCI\BaseAPI;

class User extends BaseAPI
{
    function __construct()
    {
        parent::__construct();

        $this->load->model('User_model', 'user_model');
    }

    public function index_get()
    {
        echo collect_ip();
        // $password = "#Suparman42";
        // $password = password_hash($password, PASSWORD_BCRYPT);
        // $password = Hashing::DataEncryption(HashType::PASSWORD)->encrypt($password);
        // $token_salt = Generate::client()->salt();
        // $token_salt = Hashing::DataEncryption(HashType::TOKEN_SALT)->encrypt($token_salt);
        // $model = new User_model([
        //     'fullname' => 'caee',
        //     'email' => 'elsyaarystin26@gmail.com',
        //     'password' => $password,
        //     'token_salt' => $token_salt,
        //     'is_active' => true
        // ]);
        // $model = $model->save();

        // var_dump($model);
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

    public function auth_post()
    {
        if(!$this->Client)
            return $this->bad_response(["message" => "failed to authenticate"]);

        $this->load->model('UAA_model', 'uaa_model');
        $attempt_model = new UAA_model([
            'client' => $this->Client->id,
            'ip' => collect_ip()
        ]);
        $auth_attempt = $attempt_model->get('client, ip');
        if($auth_attempt) {
            // $last_attempt = (int) $auth_attempt->last_attempt / 1000;
            $diff = militime() - $auth_attempt->last_attempt;
            if($diff > 600000) {
                $auth_attempt->delete();
                $auth_attempt = null;
            } else {
                $remain = $auth_attempt->last_attempt + 600000 - militime();
                $remain = round($remain / 60000);

                if($auth_attempt->count >= 3)
                    return $this->bad_response(["message" => "failed to authenticate. please try again in $remain minutes"]);
            }
        }

        $data = $this->special_post('email, password')->data;
        if(!$data->email || !$data->password || !Validate::email($data->email)) {
            return $this->bad_response(["message" => "failed to authenticate"]);
        }

        $data->email = strtolower($data->email);

        $this->user_model->email = $data->email;
        $user_model = $this->user_model->get('email', true);
        if(!$user_model) {
            if($auth_attempt) {
                $auth_attempt->count +=1;
                $auth_attempt->update();
            } else {
                $attempt_model->save();
            }

            return $this->bad_response(["message" => "failed to authenticate"]);
        }

        if(!password_verify($data->password, $user_model->password)) {
            if($auth_attempt) {
                $auth_attempt->count +=1;
                $auth_attempt->update();
            } else {
                $attempt_model->save();
            }

            return $this->bad_response(["message" => "failed to authenticate"]);
        }

        $this->load->model('AuthData_model');
        $auth_data = new AuthData_model([
            "user" => $user_model->id,
            "client" => $this->Client->id,
            "time" => militime()
        ]);

        $jwt_data = $auth_data->convert()->encode();
        $token = Hashing::JWT($user_model->token_salt)->build($jwt_data);
        if($auth_attempt)
            $auth_attempt->delete();

        $this->response_ok([
            "content" => [
                "auth_token" => $token->toString(),
                "exp" => $token->claims()->get('exp')
            ]
        ]);
    }
}