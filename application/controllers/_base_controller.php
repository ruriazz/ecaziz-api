<?php

namespace WarkopDeveloper\CustomCI;

defined('BASEPATH') or exit('No direct script access allowed');


class BaseController extends \CI_Controller
{
    
    function __construct()
    {
        parent::__construct();

        $this->load->helper('cookie');
        $this->load->helper('assets');
        $this->load->helper('url');
        // $this->_init_request();
    }

    protected function load_view(ViewModel $viewModel)
    {
        $assets = create_assets($viewModel->assets);

        $viewModel->css = $assets->css;
        $viewModel->js = $assets->js;
        $viewModel->modules = $viewModel->modules ? create_assets($viewModel->modules)->js : null;
        $viewModel->load();
    }

    protected function page_not_found()
    {
        return $this->load->view('errors/html/error_404');
    }
}