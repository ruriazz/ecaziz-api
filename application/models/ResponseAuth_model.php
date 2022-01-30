<?php
defined('BASEPATH') or exit('No direct script access allowed');

class ResponseAuth_model extends CI_Model {
    public String $id;
    public String $client;
    public String $fullname;
    public String $email;
    public String $auth_token;
    public Object $token_iat;
    public Object $token_exp;

    function __construct(Array $data)
    {

    }
}