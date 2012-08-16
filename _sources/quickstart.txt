.. _quickstart:

FG PasswdStack QuickStart
=========================


At this moment, our software only provides a command line interface. Thus, users need access to the machine where the FG PasswdClient client 
is installed. Currently, this is installed and configured in the FutureGrid India cluster (``india.futuregrid.org``). 
  
Login on India and use the module functionality to load the environment variables:

   ::

      $ ssh <username>@india.futuregrid.org
      $ module load futuregrid



The authentication is done via FutureGrid Ldap server. Thus, in each command we need to specify our FutureGrid username and we 
will be asked for our portal password.   

Using FG PasswdStack
--------------------

   ::

      $ fg-passwdstack -u <username> 

.. note::
   Users need to use their FutureGrid username and portal password.


After typing the command, you will be asked for your portal password. Then, you will be asked for the password that you want to have in 
the OpenStack Dashboard. This password is asked two times to make sure you do not misspell the new password.

  ::
   
     Output: 

         Passwd Stack client...
         Please insert the password for the user jdiaz
         Enter Portal Password:
         
         Please insert the password you want to have in the OpenStack dashboard
         Enter new Dashboard password:
         Retype new Dashboard password:
         The strength of the password is: Weak
         Connecting server: 172.29.200.121:56761
         Your request is in the queue to be processed after authentication
         Authentication OK. Your image request is being processed
         The password was reset: OK
