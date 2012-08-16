.. _chap_configure_futuregrid-passwdstack:

Setting up the FutureGrid Software for FG PasswdStack
=====================================================

Configuration Files
-------------------

There are two places where we can locate the configuration files. Our software will look into these places in the following order:   

#. In the directory ``~/.fg/``
#. In the directory ``/etc/futuregrid/`` 

If you have installed FutureGrid PasswdStack using the tarball file (:ref:`Using a source tarball <source_tarball>`) you will find the configuration 
sample files in /etc/futuregrid/. Otherwise, you can download them as a :docs-tar:`tarball <configsamples>` or a :docs-zip:`ZIP file <configsamples>`.

**Server Side**: The configuration file has to be renamed as ``fg-server.conf``.

**Client Side**: The configuration file has to be renamed as ``fg-client.conf``. 

.. note::
   If you configure several clients or servers in the same machine, the ``fg-client.conf`` or ``fg-server.conf`` must be the same file.

.. note::
   In the **Client Side**, the path of the log files must be relative to each users. Using the ``$HOME`` directory is a good idea.

Setting up LDAP
---------------

The authentication of our software is based on LDAP. So, we need to configure some options in the configuration files to make it possible. 

Server Side
***********

We need to configure the ``[LDAP]`` section. This is going to be use by all servers. More information about this section 
of the server configuration file can be found in :ref:`LDAP section <fg-server_ldap>`.

   .. highlight:: bash

   ::
   
      [LDAP]
      LDAPHOST= ldap.futuregrid.org
      LDAPUSER= uid=rainadmin,ou=People,dc=futuregrid,dc=org
      LDAPPASS= passwordrainadmin
      log= ~/fg-auth.log




Setting up FG PasswdStack
-------------------------

In this section we explain how to configure FG PasswdStack. 

.. _passwdstack_config:

Server Side
***********

First, we are going to configure the main server. We need to configure the ``[PasswdStackServer]`` Section 
(see :ref:`PasswdStackServer section <fg-server_passwdstackserver>`). 

   .. highlight:: bash

   ::
   
      [PasswdStackServer]
      port = 56795
      proc_max=5
      refresh=20
      log = passwdstackserver.log
      log_level = debug
      ca_cert=/opt/futuregrid/futuregrid/etc/imdserver/cacert.pem
      certfile=/opt/futuregrid/futuregrid/etc/imdserver/imdscert.pem
      keyfile=/opt/futuregrid/futuregrid/etc/imdserver/privkey.pem

Once everything is set up, you can start the server executing ``PasswdStackServer.py`` as ``imageman`` user.

.. note::
   We recommend to have a system user that run all the servers (i.e. imageman). In this way, it will be easier to manage the sudoers file when necessary. 

.. _passwdstack_client_conf:

Client Side
***********

In the client side, we need to configure the ``[PasswdStack]`` section. More information 
about this section of the client configuration file can be found in :ref:`PasswdStack section <fg-client_passwdstack>`.

   .. highlight:: bash

   ::
     
      [PasswdStack]
      port = 56796
      serveraddr=123.123.123.123
      log = passwdstackclient.log
      log_level = debug
      ca_cert=/etc/futuregrid/imdserver/cacert.pem
      certfile=/etc/futuregrid/imdserver/imdscert.pem
      keyfile=/etc/futuregrid/imdserver/privkey.pem
     

The executable file of this client is ``fg-paswdstack``. More information about how to use FG PasswdStack can be found 
in the :ref:`FG PasswdStack Manual <man-passwdstack>`.


FG PasswdStack Check List
*************************

+-----------------+-----------------------------------------+----------------------------------+
|                 | Server Side (``fg-server.conf``)        | Client Side (``fg-client.conf``) |
+=================+=========================================+==================================+
| **Requirement** | - LDAP client configured in the machine |                                  |
+-----------------+-----------------------------------------+----------------------------------+
| **Configure**   | - ``[PasswdStackServer]`` section       | - ``[PasswdStack]`` section      |
|                 | - ``[LDAP]`` section                    |                                  |
+-----------------+-----------------------------------------+----------------------------------+
| **Executables** | - ``PasswdStackServer.py``              | - ``fg-paswdstack``              |
+-----------------+-----------------------------------------+----------------------------------+


