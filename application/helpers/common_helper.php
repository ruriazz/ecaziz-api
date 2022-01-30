<?php
defined('BASEPATH') or exit('No direct script access allowed');

if (!function_exists('client_info')) {
    function client_info(): ?Object
    {
        $ci = &get_instance();
        $ci->load->model('Client_model');
        $client_id = collect_header('Client');
        if (!$client_id)
            return null;

        $client_model = new Client_model();
        $client_data = $client_model->convert()->fromArray([
            "id" => $client_id
        ]);
        $client_data = $client_data->get();

        return $client_data;
    }
}

if (!function_exists('collect_header')) {
    function collect_header(?String $header_key = null)
    {
        $headers = getallheaders();
        if (is_bool($headers))
            $headers = array();

        foreach ($headers as $key => $value) {
            $newKey = strtolower($key);
            unset($headers[$key]);
            $headers = array_merge($headers, ["$newKey" => $value]);
        }

        if ($header_key) {
            $header_key = strtolower($header_key);
            if (array_key_exists($header_key, $headers))
                return $headers[$header_key];

            return null;
        }

        return $headers;
    }
}

if (!function_exists('collect_ip')) {
    function collect_ip() : String
    {
        if (isset($_SERVER["HTTP_CF_CONNECTING_IP"])) {
            $_SERVER['REMOTE_ADDR'] = $_SERVER["HTTP_CF_CONNECTING_IP"];
            $_SERVER['HTTP_CLIENT_IP'] = $_SERVER["HTTP_CF_CONNECTING_IP"];
        }
        $client  = @$_SERVER['HTTP_CLIENT_IP'];
        $forward = @$_SERVER['HTTP_X_FORWARDED_FOR'];
        $remote  = $_SERVER['REMOTE_ADDR'];

        if (filter_var($client, FILTER_VALIDATE_IP)) {
            $ip = $client;
        } elseif (filter_var($forward, FILTER_VALIDATE_IP)) {
            $ip = $forward;
        } else {
            $ip = $remote;
        }

        return $ip;
    }
}
