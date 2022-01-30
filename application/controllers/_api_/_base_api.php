<?php

namespace WarkopDeveloper\CustomCI;

defined('BASEPATH') or exit('No direct script access allowed');

use chriskacerguis\RestServer\RestController;
use stdClass;
use Exception;

class BaseAPI extends RestController
{

    protected ?Object $Client;
    protected ?Object $User;

    function __construct()
    {
        parent::__construct();
        $this->Client = client_info();
    }

    protected function bad_response(?array $data = [], ?int $httpCode = null)
    {
        $data['code'] = $httpCode == null ? RestController::HTTP_BAD_REQUEST : $httpCode;
        $data['success'] = false;

        $responseBody = new ResponseBody($data);
        return $this->response($responseBody, $responseBody->code);
    }

    protected function response_ok(array $data = [])
    {
        $data['code'] = 200;
        $data['success'] = true;

        $responseBody = new ResponseBody($data);
        return $this->response($responseBody, $responseBody->code);
    }

    protected function get_header(String $key) : ?String
    {
        $headers = $this->_get_headers();
        $key = strtolower($key);
        if(!array_key_exists($key, $headers))
            return null;

        return $headers[$key];
    }

    protected function special_get($keys, bool $isHTML = false)
    {
        if (is_array($keys)) {
            $results = new stdClass();
            foreach ($keys as $key) {
                $key = trim($key);
                $value = (string) $this->get($key);
                if ($value !== null && $value !== '') {
                    $value = trim($value);
                    if (!$isHTML) {
                        $value = htmlspecialchars($value);
                    }
                } else if ($value == '') {
                    $value = null;
                }

                $results->$key = $value;
            }

            return new RequestBody('GET', $results);
        } else if (is_string($keys)) {
            $keys = explode(',', $keys);

            return $this->special_get($keys, $isHTML);
        }

        throw new Exception("special_get() only allows parameters in strings or arrays");
    }

    protected function special_post($keys, bool $isHTML = false)
    {
        if (is_array($keys)) {
            $results = new stdClass();
            foreach ($keys as $key) {
                $key = trim($key);
                $value = $this->post($key);
                if ($value !== null && $value !== '') {
                    if (is_string($value)) {
                        $value = trim($value);
                        if (!$isHTML) {
                            $value = htmlspecialchars($value);
                        }
                    } else if (is_array($value)) {
                        if (!$isHTML) {
                            array_walk_recursive($value, array($this, '_filter_html_chars'));
                        }
                        $value = json_encode($value);
                        $value = json_decode($value);
                    }
                } else if ($value == '') {
                    $value = null;
                }

                $results->$key = $value;
            }

            return new RequestBody('POST', $results);
        } else if (is_string($keys)) {
            $keys = explode(',', $keys);

            return $this->special_post($keys, $isHTML);
        }

        throw new Exception("special_post() only allows parameters in strings or arrays");
    }

    protected function special_put($keys, bool $isHTML = false)
    {
        if (is_array($keys)) {
            $results = new stdClass();
            foreach ($keys as $key) {
                $key = trim($key);
                $value = $this->put($key);
                if ($value !== null && $value !== '') {
                    if (is_string($value)) {
                        $value = trim($value);
                        $value = htmlspecialchars($value);
                    } else if (is_array($value)) {
                        array_walk_recursive($value, array($this, '_filter_html_chars'));
                        $value = json_encode($value);
                        $value = json_decode($value);
                    }
                } else if ($value == '') {
                    $value = null;
                }

                $results->$key = $value;
            }

            return new RequestBody('PUT', $results);
        } else if (is_string($keys)) {
            $keys = explode(',', $keys);

            return $this->special_put($keys, $isHTML);
        }

        throw new Exception("special_put() only allows parameters in strings or arrays");
    }

    protected function special_patch($keys, bool $isHTML = false)
    {
        if (is_array($keys)) {
            $results = new stdClass();
            foreach ($keys as $key) {
                $key = trim($key);
                $value = $this->patch($key);
                if ($value !== null && $value !== '') {
                    if (is_string($value)) {
                        $value = trim($value);
                        $value = htmlspecialchars($value);
                    } else if (is_array($value)) {
                        array_walk_recursive($value, array($this, '_filter_html_chars'));
                        $value = json_encode($value);
                        $value = json_decode($value);
                    }
                } else if ($value == '') {
                    $value = null;
                }

                $results->$key = $value;
            }

            return new RequestBody('PATCH', $results);
        } else if (is_string($keys)) {
            $keys = explode(',', $keys);

            return $this->special_patch($keys, $isHTML);
        }

        throw new Exception("special_patch() only allows parameters in strings or arrays");
    }

    protected function file_post($keys)
    {
        if (is_array($keys)) {
            $data = array();
            foreach ($keys as $key) {
                $result = array("$key" => null);
                if (isset($_FILES["$key"])) {
                    $result = array(
                        "$key" => (object) $_FILES["$key"]
                    );
                }

                $data = array_merge($data, $result);
            }

            return new RequestBody('FILE_POST', (object) $data);
        } else if (is_string($keys)) {
            $keys = explode(',', $keys);
            $fix = array();
            foreach ($keys as $key) {
                $key = $key !== null || strlen(trim($key)) > 0 ? trim($key) : null;

                if ($key !== null)
                    array_push($fix, $key);
            }

            return $this->file_post($fix);
        }

        return new RequestBody('FILE_POST', new stdClass());
    }

    protected function multipart_post($keys, bool $isHTML = false)
    {
        if (is_array($keys)) {
            $data = array();
            foreach ($keys as $key) {
                $result = array("$key" => null);
                if ($this->input->post("$key") !== null) {
                    $value = $this->input->post("$key");
                    $result = array(
                        "$key" => htmlspecialchars($value)
                    );
                }

                $data = array_merge($data, $result);
            }

            return new RequestBody('MULTIPART_POST', (object) $data);
        } else if (is_string($keys)) {
            $keys = explode(',', $keys);
            $fix = array();
            foreach ($keys as $key) {
                $key = $key !== null || strlen(trim($key)) > 0 ? trim($key) : null;

                if ($key !== null)
                    array_push($fix, $key);
            }

            return $this->multipart_post($fix, $isHTML);
        }

        return new RequestBody('MULTIPART_POST', new stdClass());
    }

    private function _filter_html_chars(&$value)
    {
        $value = htmlspecialchars($value, ENT_QUOTES, 'UTF-8');
    }

    private function _get_headers(): array
    {
        $headers = getallheaders();
        if (is_bool($headers))
            $headers = array();

        foreach ($headers as $key => $value) {
            $newKey = strtolower($key);
            unset($headers[$key]);
            $headers = array_merge($headers, ["$newKey" => $value]);
        }

        return $headers;
    }
}

class RequestBody
{
    public String $method;
    public Object $data;

    function __construct(String $method, Object $data)
    {
        $this->method = $method;
        $this->data = $data;
    }
}

class ResponseBody
{
    public bool $success;
    public int $code;
    public String $message;
    public $content;
    public String $type;
    public int $time;

    function __construct(array $data)
    {
        $data = (object) $data;

        if (property_exists($data, 'success')) {
            $this->success = (bool) $data->success;
        }

        if (property_exists($data, 'code')) {
            $this->code = (int) $data->code;
        }

        if (property_exists($data, 'message')) {
            $this->message = (string) $data->message;
        } else {
            unset($this->message);
        }

        if (property_exists($data, 'content')) {
            $this->content = $data->content;
        } else {
            unset($this->content);
        }

        if (property_exists($data, 'type')) {
            $this->type = $data->type;
        } else {
            unset($this->type);
        }

        $this->time = militime();
    }
}
