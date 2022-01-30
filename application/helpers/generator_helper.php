<?php
defined('BASEPATH') or exit('No direct script access allowed');

use Ramsey\Uuid\Uuid;

if(!class_exists("Generate")) {
    class Generate {
        public static function client() : Object
        {
            return new class {
                public function alias() : String
                {
                    $uuid = uniqid();
                    return sha1($uuid);
                }

                public function salt() : String
                {
                    $ci=& get_instance();
                    $key = $ci->encryption->create_key(8);

                    return bin2hex($key);
                }
            };
        }
    }
}

if(!function_exists('militime')) {
    function militime() : int
    {
        return (int) round(microtime(true) * 1000);
    }
}