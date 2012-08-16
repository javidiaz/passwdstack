.. _sec_fg-client.conf:

``fg-client.conf`` configuration file
-------------------------------------

.. _fg-client_passwdstack:

Section ``[PasswdStack]``
*************************

This section is used to configure FG PasswdStack.

Option ``port``
~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Port where the FG PasswdStack server will be listening.

Option ``serveraddr``
~~~~~~~~~~~~~~~~~~~~~

**Type:** String

**Required:** Yes

Address of the machine where the FG PasswdStack server is running.

Option ``log``
~~~~~~~~~~~~~~

**Type:** log-file

**Required:** Yes

Location of the file where the logs will be stored.

Option ``log_level``
~~~~~~~~~~~~~~~~~~~~

**Valid values:** ``debug``,``error``,``warning``,``info``

**Required:** No

Desired log level. The default option is ``debug``.


Option ``ca_cert``
~~~~~~~~~~~~~~~~~~

**Type:** ca-cert

**Required:** Yes

Location of CA certificate (PEM-encoded) used to generate user and service certificates.

Option ``certfile``
~~~~~~~~~~~~~~~~~~~

**Type:** service-cert

**Required:** Yes

Location of the certificate (PEM-encoded) used by the FG PasswdStack client.

Option ``keyfile``
~~~~~~~~~~~~~~~~~~

**Type:** key-cert

**Required:** Yes

Location of the private key (PEM-encoded) of the certificate specified in ``certfile``.

************
