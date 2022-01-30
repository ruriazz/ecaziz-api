<?php
defined('BASEPATH') or exit('No direct script access allowed');

if(!class_exists('Validate')) {
    class Validate {
        public static function email(String $email) : bool
        {
            $find1 = substr_count($email, '@');
            $find2 = substr_count($email, '.');
            return (strlen($email) >= 10 && $find1 == 1 && $find2 > 1);  
        }
    }
}