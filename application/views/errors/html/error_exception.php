<?php
defined('BASEPATH') or exit('No direct script access allowed');

$instance =& get_instance();
if (ENVIRONMENT == 'development' && $instance instanceof WarkopDeveloper\CustomCI\BaseController) : ?>

	<div style="border:1px solid #990000;padding-left:20px;margin:0 0 10px 0;">

		<h4>An uncaught Exception was encountered</h4>

		<p>Type: <?php echo get_class($exception); ?></p>
		<p>Message: <?php echo $message; ?></p>
		<p>Filename: <?php echo $exception->getFile(); ?></p>
		<p>Line Number: <?php echo $exception->getLine(); ?></p>

		<?php if (defined('SHOW_DEBUG_BACKTRACE') && SHOW_DEBUG_BACKTRACE === TRUE) : ?>

			<p>Backtrace:</p>
			<?php foreach ($exception->getTrace() as $error) : ?>

				<?php if (isset($error['file']) && strpos($error['file'], realpath(BASEPATH)) !== 0) : ?>

					<p style="margin-left:10px">
						File: <?php echo $error['file']; ?><br />
						Line: <?php echo $error['line']; ?><br />
						Function: <?php echo $error['function']; ?>
					</p>
				<?php endif ?>

			<?php endforeach ?>

		<?php endif ?>

	</div>
<?php
	exit();
elseif(ENVIRONMENT == 'development' && $instance instanceof WarkopDeveloper\CustomCI\BaseAPI) :
	$sapi_type = php_sapi_name();
	if (substr($sapi_type, 0, 3) == 'cgi') {
		header("Status: 500 Internal Server Error");
	} else {
		header("HTTP/1.1 500 Internal Server Error");
	}

	header('Content-Type: application/json; charset=utf-8');

	if (defined('SHOW_DEBUG_BACKTRACE') && SHOW_DEBUG_BACKTRACE === TRUE) {
		foreach ($exception->getTrace() as $error) {
			if (isset($error['file']) && strpos($error['file'], realpath(BASEPATH)) !== 0) {
				if(!isset($errors))
					$errors = array();

				array_push($errors, [
					'file' => $error['file'],
					'line' => $error['line'],
					'function' => $error['function']
				]);
			}
		}
	}

	echo json_encode([
		'type' => $exception,
		'message' => $message,
		'filename' => $exception->getFile(),
		'linenumber' => $exception->getLine(),
		'backtrace' => isset($errors) ? $errors : array()
	]);
	exit();
endif;

require_once __DIR__ . DIRECTORY_SEPARATOR . 'error_404.php'; ?>