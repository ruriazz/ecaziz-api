<?php
defined('BASEPATH') or exit('No direct script access allowed');

class UAA_model extends CI_Model
{
    public int $id;
    public int $client;
    public String $ip;
    public int $count;
    public int $last_attempt;

    private static String $table = "authentication_attempt";

    function __construct(Array $data = null)
    {
        if($data) {
            if(array_key_exists('id', $data) && $data['id'] !== null && is_numeric("{$data['id']}"))
                $this->id = (int) $data['id'];

            if(array_key_exists('client', $data) && $data['client'] !== null && is_numeric("{$data['client']}"))
                $this->client = (int) $data['client'];

            if(array_key_exists('ip', $data) && $data['ip'] !== null && is_string($data['ip']) && ip2long($data['ip']) !== false)
                $this->ip = (string) $data['ip'];

            if(array_key_exists('count', $data) && $data['count'] !== null && is_numeric("{$data['count']}"))
                $this->count = (int) $data['count'];

            if(array_key_exists('last_attempt', $data) && $data['last_attempt'] !== null && is_numeric("{$data['last_attempt']}"))
                $this->last_attempt = (int) $data['last_attempt'];
        }
    }

    public function save()
    {
        $this->last_attempt = militime();
        $insert = $this->db->insert(UAA_model::$table, $this);
        if(!$insert)
            return null;
        
        $this->id = $this->db->insert_id();
        return $this;
    }

    public function get(String $keys = 'id')
    {
        $keys = explode(',', $keys);
        $this->db->select('*')
                    ->from(UAA_model::$table);
        foreach($keys as $key) {
            $key = trim($key);
            if(property_exists($this, $key))
                $this->db->where($key, $this->$key);
        }

        $result = $this->db->get()->row_array();
        return $result ? new UAA_model($result) : null;
    }

    public function update() : UAA_model
    {
        $this->db->where('id', $this->id);
        $this->db->update(UAA_model::$table, $this);

        return $this;
    }

    public function delete() : bool
    {
        $this->db->where('id', $this->id);
        return $this->db->delete(UAA_model::$table);
    }
}
