<?php
defined('BASEPATH') or exit('No direct script access allowed');

class User_model extends CI_Model
{
    public int $id;
    public String $fullname;
    public String $email;
    public String $password;
    public String $token_salt;
    public bool $is_active;

    function __construct(?array $data = null)
    {
        if ($data) {
            if (array_key_exists('id', $data) && $data['id'] !== null && is_numeric("{$data['id']}"))
                $this->id = (int) $data['id'];

            if (array_key_exists('fullname', $data) && $data['fullname'] !== null && is_string($data['fullname']))
                $this->fullname = strtolower($data['fullname']);

            if (array_key_exists('email', $data) && $data['email'] !== null && Validate::email($data['email']))
                $this->email = strtolower($data['email']);

            if (array_key_exists('password', $data) && $data['password'] !== null && is_string($data['password']))
                $this->password = $data['password'];

            if (array_key_exists('token_salt', $data) && $data['token_salt'] !== null && is_string($data['token_salt']))
                $this->token_salt = $data['token_salt'];

            if (array_key_exists('is_active', $data) && $data['is_active'] !== null && (is_numeric("{$data['is_active']}") || is_bool($data['is_active'])))
                $this->is_active = (bool) $data;
        }
    }

    public function save()
    {
        $insert = $this->db->insert('user_data', $this);
        if(!$insert)
            return null;
        
        $this->id = $this->db->insert_id();
        return $this;
    }

    public function get(String $keys = 'id', bool $decrypted_data = false): ?User_model
    {
        $keys = explode(',', $keys);
        $this->db->select('*')
            ->from('user_data');
        foreach ($keys as $key) {
            $key = trim($key);
            if (property_exists($this, $key))
                $this->db->where($key, $this->$key);
        }

        $result = $this->db->get()->row_array();
        if(!$result)
            return null;

        if($decrypted_data) {
            $result['password'] = Hashing::DataEncryption(HashType::PASSWORD)->decrypt($result['password']);
            $result['token_salt'] = Hashing::DataEncryption(HashType::TOKEN_SALT)->decrypt($result['token_salt']);
        }

        return new User_model($result);
    }

    public function update()
    {
    }

    public function delete()
    {
    }

    public function convert(): Object
    {
        $data = $this;
        return new class($data)
        {
            function __construct(Object $data)
            {
                $this->data = $data;
            }

            public function fromJson(): ?User_model
            {
                return new User_model();
            }

            public function toJson()
            {
            }

            public function fromArray(): ?User_model
            {
                return new User_model();
            }

            public function toArray()
            {
            }
        };
    }
}
