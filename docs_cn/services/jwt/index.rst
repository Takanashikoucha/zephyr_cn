.. _jwt_api:

JSON
Web
Token
（JWT）
####################

Overview
********

JSON Web Tokens（JWT）是一种开放的工业标准（:rfc:`7519`）方法，用于在两个 parties 之间安全地表示 claims。虽然 JWT 相当灵活，但该 API 仅限于创建与 Google Core IoT infrastructure 进行身份验证所需的简单 tokens。

从高层次来看，JWT 只是一个签名的 JSON blob，client 可以将其作为 token 呈现，而不必每次都发送例如 username/password。

Usage
=====

要使用 JWT API，请包含该 header file：

.. code-block:: c

   #include <zephyr/data/jwt.h>

Generating
a
JWT
----------------

JWT subsystem 提供了一个轻量级的、基于 builder 的 API，用于构建 JSON Web Tokens（JWT）。它允许创建 payload（claims）包含以下内容的 tokens：expiration time、issued at time 和 audience。然后该 token 使用提供的 private key 进行签名。

.. code-block:: c

   #include <zephyr/data/jwt.h>

   struct jwt_builder builder;
   char buffer[1024];
   int ret;

   /* Initialize the builder */
   ret = jwt_init_builder(&builder, buffer, sizeof(buffer));
   if (ret < 0) {
       /* Handle error */
   }

   /* Add payload: expiration, issued at, audience */
   ret = jwt_add_payload(&builder, 1767221999, 1764605987, "project-id");
   if (ret < 0) {
       /* Handle error */
   }

   /* Sign the token using a DER-encoded private key */
   ret = jwt_sign(&builder, private_key_der, private_key_der_len);
   if (ret < 0) {
       /* Handle error */
   }

   /*
    * buffer now contains the JWT; it can be passed to a third-party service that will be able
    * to validate it against the public key associated with `private_key_der`.
    */

Configuration
*************

相关的配置选项：

* :kconfig:option:`CONFIG_JWT`
* :kconfig:option-regex:`CONFIG_JWT_.*`


API Reference
*************

.. doxygengroup:: jwt
