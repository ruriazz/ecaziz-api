<?php
defined('BASEPATH') or exit('No direct script access allowed');

use Lcobucci\JWT\Configuration;
use Lcobucci\JWT\Signer;
use Lcobucci\JWT\Signer\Key\InMemory;

if (!class_exists('Hashing')) {
    class Hashing
    {
        public static function Id(?String $hash_type = "default"): Object
        {
            $key = HashKey::$$hash_type;
            return new class($key)
            {
                function __construct(String $key)
                {
                    $this->instance = new Hashids\Hashids($key);
                }

                public function encode(int $id): String
                {
                    $id = sprintf("%05d", $id);
                    $id = bin2hex($id);
                    return $this->instance->encodeHex($id);
                }

                public function decode(String $hash): ?int
                {
                    try {
                        $hex = $this->instance->decodeHex($hash);
                        $bin = hex2bin($hex);
                        return is_numeric($bin) ? (int) $bin : null;
                    } catch (\Throwable $th) {
                        return null;
                    }
                }
            };
        }

        public static function StringId(?String $hash_type = "default"): Object
        {
            $key = HashKey::$$hash_type;
            return new class($key)
            {
                function __construct(String $key)
                {
                    $this->instance = new Hashids\Hashids($key);
                }

                public function encode(String $id): String
                {
                    $id = bin2hex($id);

                    return $this->instance->encodeHex($id);
                }

                public function decode(String $hash): String
                {
                    $hex = $this->instance->decodeHex($hash);
                    return hex2bin($hex);
                }
            };
        }

        public static function DataEncryption(?String $hash_type = "default"): Object
        {
            $ci = &get_instance();
            $key = HashKey::$$hash_type;
            return new class($ci->encryption, $key)
            {
                private object $tool;

                function __construct(object $tool, String $key)
                {
                    $this->tool = $tool->initialize(
                        array(
                            'cipher' => 'aes-256',
                            'mode' => 'cbc',
                            'key' => ctype_xdigit($key) ? hex2bin($key) : $key
                        )
                    );
                }

                public function encrypt(String $plain_text): String
                {
                    return $this->tool->encrypt($plain_text);
                }

                public function decrypt(String $encrypted_text): ?String
                {
                    $decrypted = $this->tool->decrypt($encrypted_text);

                    return $decrypted ? $decrypted : null;
                }
            };
        }

        public static function JWT(String $token_salt): Object
        {
            $token_salt = base64_encode($token_salt);
            $configuration = Configuration::forAsymmetricSigner(
                // You may use RSA or ECDSA and all their variations (256, 384, and 512) and EdDSA over Curve25519
                new Signer\Rsa\Sha256(),
                InMemory::file(APPPATH . 'config/jwtRS256.key'),
                InMemory::base64Encoded($token_salt)
                // You may also override the JOSE encoder/decoder if needed by providing extra arguments here
            );

            return new class($configuration)
            {
                function __construct(Configuration $config)
                {
                    $this->config = $config;
                }

                public function build(Object $claim) : Object
                {
                    assert($this->config);
                    $now   = new DateTimeImmutable();
                    return $this->config->builder()
                        // Configures the issuer (iss claim)
                        ->issuedBy('http://localhost')
                        // Configures the audience (aud claim)
                        ->permittedFor('http://localhost')
                        // Configures the time that the token was issue (iat claim)
                        ->issuedAt($now)
                        // Configures the expiration time of the token (exp claim)
                        ->expiresAt($now->modify('+1 hour'))
                        ->withClaim('user', $claim->user)
                        ->withClaim('client', $claim->client)
                        ->getToken($this->config->signer(), $this->config->signingKey());
                }

                public function parse()
                {
                }

                public function validate()
                {
                }
            };
        }
    }
}

if (!class_exists('HashKey')) {
    class HashKey
    {
        public static String $default = "eLW0sJrohW5kl2lo";
        public static String $clientID = "yJC6xVY1BkAjSQk5";
        public static String $userID = "lwXzXmv8YUJknyba";
        public static String $inviteID = "wRu6jJmrZlfBS3kl";
        public static String $greetingID = "glNAgXjCoP0nfA7v";
        public static String $password = "8e5ffe4d5d155d2a85f4323bf702920ad4eccf8c4f17893cdfb3d9675c83502c";
        public static String $tokenSalt = "1b5d8c05939ac1f53f5926ee550fceaf9ee20bf3dc8d54de5de344a9d431c9bb";
        public static String $authData = "2f75f72350e52c6b171b5557aeedb0c6d6693dff3afdf57977d8572de224ae8e";
    }
}

if (!class_exists('HashType')) {
    abstract class HashType
    {
        const DEFAULT = "default";
        const CLIENT_ID = "clientID";
        const USER_ID = "userID";
        const INVITE_ID = "inviteID";
        const GREETING_ID = "greetingID";
        const PASSWORD = "password";
        const TOKEN_SALT = "tokenSalt";
        const AUTH_DATA = "authData";
    }
}
