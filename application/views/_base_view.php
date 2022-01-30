<?php
defined('BASEPATH') or exit('No direct script access allowed');

function sanitize_output($buffer)
{
    $search = array('/\>[^\S ]+/s', '/[^\S ]+\</s', '/(\s)+/s', '/<!--(.|\s)*?-->/');
    $replace = array('>', '<', '\\1', '');
    $buffer = preg_replace($search, $replace, $buffer);

    return $buffer;
}

ob_start("sanitize_output");
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- iOS meta tags & icons -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="SISDABIMA">
    <link rel="apple-touch-icon" href="<?php echo base_url('assets/icons/Icon-192.png'); ?>">

    <meta name="author" content="ruriazz | warkopwarawiri.id.id">
    <link rel="icon" href="<?php echo base_url('favicon.ico'); ?>" type="image/x-icon" />
    <meta name="description" content="<?php echo $model->description; ?>">
    <?php if ($model->keywords !== null) echo '<meta name="keywords" content="' . $model->keywords . '">'; ?>
    <?php if ($model->show_ads) echo '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=CLIENT_KEY" crossorigin="anonymous"></script>'; ?>
    <link rel="manifest" href="<?php echo base_url('manifest.json'); ?>">

    <meta name="theme-color" content="HEXCOLOR" />
    <title><?php echo $model->title; ?></title>

    <?php
    $cssManifest = public_asset('conf/cdncssManifest.json');
    $cdnCss = array();
    if (file_exists($cssManifest)) {
        $cdnCss = file_get_contents($cssManifest);
        $cdnCss = json_decode($cdnCss, true);
        unlink($cssManifest);
    }

    foreach ($cdnCss as $cdn) {
        $cdn = (object) $cdn;
        echo '<link rel="stylesheet" href="' . $cdn->src . '"></link>';
    }

    if ($model->css)
        echo '<link rel="stylesheet" href="' . $model->css . '">';
    ?>

</head>

<body <?php

        if ($model->head)
            $this->load->view($model->head, $model->data);

        $this->load->view($model->body, $model->data);

        if ($model->foot)
            $this->load->view($model->foot, $model->data);

        $jsManifest = public_asset('conf/cdnjsManifest.json');
        $cdnJs = array();
        if (file_exists($jsManifest)) {
            $cdnJs = file_get_contents($jsManifest);
            $cdnJs = json_decode($cdnJs, true);
            unlink($jsManifest);
        }

        foreach ($cdnJs as $cdn) {
            $cdn = (object) $cdn;
            echo '<script src="' . $cdn->src . '"></script>';
        }

        if ($model->js)
            echo '<script src="' . $model->js . '"></script>';

        if ($model->modules)
            echo '<script type="module" src="' . $model->modules . '"></script>';
        ?> </body>

</html>

<?php ob_end_flush() ?>