.. _sec_fg-server.conf:

``fg-server.conf`` configuration file
-------------------------------------

.. _fg-server_ldap:

Section ``[LDAP]``
******************

This section is used to configure the access to LDAP to verify the user passwords.

*This section is required by all services*

Option ``LDAPHOST``
~~~~~~~~~~~~~~~~~~~

**Type:** String

**Required:** Yes

Hostname or IP address of the LDAP server that manages the user's authentication.

Option ``LDAPUSER``
~~~~~~~~~~~~~~~~~~~

**Type:** user-dn

**Required:** Yes

This is the DN of an user that have read access to the encrypted passwords of every user. This looks 
like ``uid=USER,ou=People,dc=futuregrid,dc=org`` 

Option ``LDAPPASS``
~~~~~~~~~~~~~~~~~~~

**Type:** String

**Required:** Yes

Password of the user specified in the previous section.

Option ``log``
~~~~~~~~~~~~~~

**Type:** log-file

**Required:** Yes

Location of the file where the logs will be stored.

Option ``test``
~~~~~~~~~~~~~~~

**Valid values:** ``True``, ``False``

**Required:** No

This option is for development purposes. For security reasons, the LDAP server cannot be contacted from outside of FutureGrid network.
Therefore, we need this option to go test our services before we deploy them on production.

****************

.. _fg-server_passwdstackserver:

Section ``[PasswdStackServer]``
*******************************

This section is used to configure the FG Move Server. 

Option ``port``
~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Port where the FG PasswdStack server will be listening.

Option ``proc_max``
~~~~~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Maximum number of request that can be processed at the same time.

Option ``refresh``
~~~~~~~~~~~~~~~~~~

**Type:** Integer

**Required:** Yes

Interval to check the status of the running requests when ``proc_max`` is reached and determine if new request can be processed.


Option ``log``
~~~~~~~~~~~~~~

**Type:** log-file

**Required:** Yes

Location of the file where the logs will be stored.

Option ``log_level``
~~~~~~~~~~~~~~~~~~~~

**Valid values:** ``debug``, ``error``, ``warning``, ``info``

**Required:** No

Desired log level. The default option is ``debug``.

Option ``ca_cert``
~~~~~~~~~~~~~~~~~~

**Type:** ca-cert

**Required:** Yes

Location of CA certificate (PEM-encoded) used to generate user and service certificates. Server certificates.

Option ``certfile``
~~~~~~~~~~~~~~~~~~~

**Type:** service-cert

**Required:** Yes

Location of the certificate (PEM-encoded) used by the FG PasswdStack server. Server certificates.

Option ``keyfile``
~~~~~~~~~~~~~~~~~~

**Type:** key-cert

**Required:** Yes

Location of the private key (PEM-encoded) of the certificate specified in ``certfile``. Server certificates.

