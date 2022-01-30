<?php

namespace WarkopDeveloper\CustomCI;

use Exception;

defined('BASEPATH') or exit('No direct script access allowed');

class ViewModel
{

    public String $title = "Welcome to CodeIgniter!";
    public String $description = "";
    public ?String $keywords = null;
    public ?String $head = null;
    public ?String $body = null;
    public ?String $foot = null;
    public array $data = [];
    public ?String $css = null;
    public ?String $js = null;
    public array $assets = [];
    public $modules = [];
    public bool $show_ads = false;

    private $ci;

    function __construct(array $data)
    {
        $this->ci = &get_instance();

        $this->_set_data($data);
    }

    private function _set_data($data)
    {
        $data = (object) $data;

        if (property_exists($data, 'title') && is_string($data->title))
            $this->title = (string) $data->title;

        if (property_exists($data, 'description') && is_string($data->description))
            $this->description = (string) $data->description;

        if (property_exists($data, 'keywords') && is_string($data->keywords))
            $this->keywords = (string) $data->keywords;

        if (property_exists($data, 'head') && is_string($data->head))
            $this->head = (string) $data->head;

        if (property_exists($data, 'body') && is_string($data->body)) {
            $this->body = (string) $data->body;
        } else {
            throw new Exception("No body to load. Please specify body to load into ModelView parameter");
        }

        if (property_exists($data, 'content') && is_string($data->content))
            $this->content = (string) $data->content;

        if (property_exists($data, 'foot') && is_string($data->foot))
            $this->foot = (string) $data->foot;

        if (property_exists($data, 'data') && is_array($data->data)) {
            if (is_array($data->data)) {
                $this->data = (array) $data->data;
            } else {
                throw new Exception("the data in the ModelView parameter must be an array");
            }
        }

        if (property_exists($data, 'css') && is_string($data->css))
            $this->css = (string) $data->css;

        if (property_exists($data, 'js') && is_string($data->js))
            $this->js = (string) $data->js;

        if (property_exists($data, 'assets') && is_array($data->assets))
            $this->assets = (array) $data->assets;

        if (property_exists($data, 'modules') && is_array($data->modules))
            $this->modules = (array) $data->modules;

        if (property_exists($data, 'show_ads') && is_bool($data->show_ads))
            $this->show_ads = (bool) $data->show_ads;
    }

    public function load()
    {
        return $this->ci->load->view('_base_view', ['model' => $this]);
    }
}
