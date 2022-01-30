<?php
defined('BASEPATH') or exit('No direct script access allowed');

class AuthData_model extends CI_Model {
    public int $user;
    public int $client;
    public int $time;

    function __construct(Array $data = null)
    {
        if($data) {
            if(array_key_exists('user', $data) && $data['user'] !== null && is_numeric("{$data['user']}"))
                $this->user = (int) $data['user'];

            if(array_key_exists('client', $data) && $data['client'] !== null && is_numeric("{$data['client']}"))
                $this->client = (int) $data['client'];

            if(array_key_exists('time', $data) && $data['time'] !== null && is_numeric("{$data['time']}"))
                $this->time = (int) $data['time'];
        }
    }

    public function convert() : Object
    {
        return new class($this) {
            function __construct(Object $data)
            {
                $this->data = $data;
            }

            public function encode() : Object
            {
                $result = new stdClass();
                $result->user = Hashing::Id(HashType::USER_ID)->encode($this->data->user);
                $result->client = Hashing::Id(HashType::CLIENT_ID)->encode($this->data->client);
                $result->time = $this->data->time;

                return $result;
            }
        };
    }
}