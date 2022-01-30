<?php
defined('BASEPATH') or exit('No direct script access allowed');

use MatthiasMullie\Minify;

if (!function_exists('asset_dir')) {
    function asset_dir($file = '')
    {
        $asset = ROOT . "assets/$file";
        $asset = str_replace(DIRECTORY_SEPARATOR, '/', $asset);

        return $asset;
    }
}

if (!function_exists('public_asset')) {
    function public_asset($file = '')
    {
        $core = ROOT . "public/assets";
        $core = str_replace(DIRECTORY_SEPARATOR, '/', $core);

        return "$core/$file";
    }
}

if (!function_exists('asset_core')) {
    function asset_core($file = '')
    {
        $core = ROOT . "public/assets/core";
        $core = str_replace(DIRECTORY_SEPARATOR, '/', $core);

        if (!is_dir($core)) {
            mkdir($core);
            file_put_contents("$core/index.html", '');
        }

        return "$core/$file";
    }
}

if (!function_exists('push_cdn')) {
    function push_cdn(String $url, String $type)
    {
        if ($type !== 'css' && $type !== 'js')
            throw new Exception("push_cdn() only accepts css and js type, not including .$type");

        get_instance();
        $manifest = public_asset("conf/cdn{$type}Manifest.json");

        if (!is_dir(public_asset('conf'))) {
            mkdir(public_asset('conf'));
            file_put_contents(public_asset('conf/index.php'), file_get_contents(APPPATH.DIRECTORY_SEPARATOR.'views/errors/html/error_404.php'));
        }

        if (!file_exists($manifest))
            file_put_contents($manifest, '[]');

        $cdnUse = public_asset("conf/cdn{$type}Manifest.json");
        $oldCdn = array();
        if (file_exists($cdnUse)) {
            $oldCdn = file_get_contents($cdnUse);
            $oldCdn = json_decode($oldCdn, true);
            unlink($cdnUse);
        }

        $newCdn = ["type" => $type, "src" => $url];
        $exist = false;
        foreach ($oldCdn as $cdn) {
            if ($cdn == $newCdn)
                $exist = true;
        }

        if (!$exist)
            array_push($oldCdn, $newCdn);

        file_put_contents($cdnUse, json_encode($oldCdn));
    }
}

if (!function_exists('create_assets')) {
    function create_assets(array $assets)
    {
        $css = array();
        $js = array();

        $callback = function ($value, $key) use (&$css, &$js) {
            $type = pathinfo($value, PATHINFO_EXTENSION);
            if (is_bool(strpos($value, asset_dir())))
                $value = asset_dir("$type/$value");

            if (!file_exists($value))
                throw new Exception("No file found $value");

            if ($type !== 'css' && $type !== 'js')
                throw new Exception("the create assets() function only accepts css and js files, not including .$type files");

            array_push($$type, $value);
            $$type = array_unique($$type);
        };
        array_walk_recursive($assets, $callback);

        $miniCSS = "";
        $miniJS = "";
        foreach ($css as $mainCSS) {
            $file = file_get_contents($mainCSS);
            $file = (new Minify\CSS($file))->minify();
            $miniCSS .= $file;
        }

        foreach ($js as $mainJS) {
            $file = file_get_contents($mainJS);
            $file = (new Minify\JS($file))->minify();
            $miniJS .= $file;
            $rearJs = substr($miniJS, -1);
            if ($rearJs !== ';')
                $miniJS .= ';';
        }

        $miniJS = trim($miniJS);
        if(strlen($miniJS) > 0) {
            $jsFileName = md5($miniJS) . ".min.js";
            $jsFile = asset_core($jsFileName);
            if (!file_exists($jsFile))
                file_put_contents($jsFile, $miniJS);
        }

        $miniCSS = trim($miniCSS);
        if(strlen($miniCSS) > 0) {
            $cssFileName = md5($miniCSS) . ".min.css";
            $cssFile = asset_core($cssFileName);
            if (!file_exists($cssFile))
                file_put_contents($cssFile, $miniCSS);
        }

        return (object) [
            'css' => isset($cssFileName) ? base_url("assets/core/$cssFileName") : null,
            'js' => isset($jsFileName) ? base_url("assets/core/$jsFileName") : null
        ];
    }
}