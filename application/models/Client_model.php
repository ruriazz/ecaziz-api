<?php
defined('BASEPATH') or exit('No direct script access allowed');

class Client_model extends CI_Model {
    public int $id;
    public String $alias;
    public String $salt;
    public int $last_transaction;

    function __construct(?Array $data = null)
    {
        if($data) {
            if(array_key_exists('id', $data) && $data['id'] !== null && is_numeric("{$data['id']}"))
                $this->id = (int) $data['id'];

            if(array_key_exists('alias', $data) && $data['alias'] !== null && is_string($data['alias']))
                $this->alias = (String) $data['alias'];

            if(array_key_exists('salt', $data) && $data['salt'] !== null && is_string($data['salt']))
                $this->salt = (String) $data['salt'];

            if(array_key_exists('last_transaction', $data) && $data['last_transaction'] !== null && is_numeric("{$data['last_transaction']}"))
                $this->last_transaction = (int) $data['last_transaction'];
        }
    }

    public function get(?String $string_keys = 'id') : ?Client_model
    {
        $keys = explode(',', $string_keys);
        $this->db->select('*')
                    ->from('client_data');
        foreach($keys as $key) {
            $i = array_search($key, $keys);
            $key = trim($key);
            if(property_exists($this, $key))
                $this->db->where($key, $this->$key);
        }

        $result = $this->db->get()->row_array();
        return $result ? new Client_model($result) : null;
    }

    public function save() : ?Client_model
    {
        $this->last_transaction = militime();
        $insert = $this->db->insert('client_data', $this);
        if(!$insert)
            return null;
        
        $this->id = $this->db->insert_id();
        return $this;
    }

    public function update() : Client_model
    {
        $this->db->where('id', $this->id);
        $this->db->update('client_data', $this);

        return $this;
    }

    public function convert() : Object
    {
        $data = $this;
        return new class($data) {
            function __construct(Object $data)
            {
                $this->data = $data;
            }

            public function fromJson(String $json) : ?Client_model
            {
                $array = json_decode($json, true);

                return $this->fromArray($array);
            }

            public function toJson() : String
            {
                return json_encode($this->toArray());
            }

            public function fromArray(Array $array) : ?Client_model
            {
                if(is_string($array['id'])) {
                    $id = Hashing::Id(HashType::CLIENT_ID)->decode($array['id']);
                    if($id) {
                        $array['id'] = $id;
                        return new Client_model($array);
                    }

                    return null;
                }
            }

            public function toArray() : Array
            {
                $array = (Array) $this->data;
                $array['id'] = Hashing::Id(HashType::CLIENT_ID)->encode($array['id']);

                return $array;
            }
        };
    }

}