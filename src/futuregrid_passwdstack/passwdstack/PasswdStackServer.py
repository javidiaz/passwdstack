#!/usr/bin/env python
# -------------------------------------------------------------------------- #
# Copyright 2010-2011, Indiana University                                    #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #
"""
Server to modify the password of OpenStack dashboard
"""
__author__ = 'Javier Diaz'

from types import *
import re
import logging
import logging.handlers
import random
import os
import sys
import socket, ssl
from multiprocessing import Process

from subprocess import *


import time

from futuregrid_passwdstack.passwdstack.PasswdStackServerConf import PasswdStackServerConf
from futuregrid_passwdstack.utils.FGTypes import FGCredential
from futuregrid_passwdstack.utils import FGAuth


class PasswdStackServer(object):

    def __init__(self):
        super(PasswdStackServer, self).__init__()

        self.user=""
        self.numparams =4
        #load configuration
        self._genConf = PasswdStackServerConf()
        self._genConf.load_passwdstackServerConfig()
        self.port = self._genConf.getPort()
        self.proc_max = self._genConf.getProcMax()
        self.refresh_status = self._genConf.getRefreshStatus()
        
        
        self.log_filename = self._genConf.getLog()
        self.logLevel = self._genConf.getLogLevel()    
        self.logger = self.setup_logger()
        
        self._ca_certs = self._genConf.getCaCerts()
        self._certfile = self._genConf.getCertFile()
        self._keyfile = self._genConf.getKeyFile()
        
        print "\nReading Configuration file from " + self._genConf.getConfigFile() + "\n"
        
        
    def setup_logger(self):
        #Setup logging
        logger = logging.getLogger("PasswdStackServer")
        logger.setLevel(self.logLevel)    
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler = logging.FileHandler(self.log_filename)
        handler.setLevel(self.logLevel)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False #Do not propagate to others
        
        return logger    
 
    def start(self):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', self.port))
        sock.listen(1) #Maximum of system unaccepted connections. Maximum value depend of the system (usually 5) 
        self.logger.info('Starting Server on port ' + str(self.port))        
        proc_list = []
        total_count = 0
        while True:        
            if len(proc_list) == self.proc_max:
                full = True
                while full:
                    for i in range(len(proc_list) - 1, -1, -1):
                        #self.logger.debug(str(proc_list[i]))
                        if not proc_list[i].is_alive():
                            #print "dead"                        
                            proc_list.pop(i)
                            full = False
                    if full:
                        time.sleep(self.refresh_status)
            
            total_count += 1
            #channel, details = sock.accept()
            newsocket, fromaddr = sock.accept()
            connstream = 0
            try:
                connstream = ssl.wrap_socket(newsocket,
                              server_side=True,
                              ca_certs=self._ca_certs,
                              cert_reqs=ssl.CERT_REQUIRED,
                              certfile=self._certfile,
                              keyfile=self._keyfile,
                              ssl_version=ssl.PROTOCOL_TLSv1)
                #print connstream                                
                proc_list.append(Process(target=self.passwdreset, args=(connstream,fromaddr[0],)))            
                proc_list[len(proc_list) - 1].start()
            except ssl.SSLError:
                self.logger.error("Unsuccessful connection attempt from: " + repr(fromaddr))
                self.logger.info("Password Stack Request DONE")
            except socket.error:
                self.logger.error("Error with the socket connection")
                self.logger.info("Password Stack Request DONE")
            except:
                self.logger.error("Uncontrolled Error: " + str(sys.exc_info()))
                try: 
                    connstream.shutdown(socket.SHUT_RDWR)
                    connstream.close()
                except:
                    pass 
                self.logger.info("Password Stack Request DONE")
                
                  
    def auth(self, userCred):
        return FGAuth.auth(self.user, userCred)        
      
    def passwdreset(self, channel, fromaddr):
        #this runs in a different proccess
        
        start_all = time.time()
        
        self.logger = logging.getLogger("PasswdStackServer." + str(os.getpid()))
        
        self.logger.info('Starting to process the request')
        
        #receive the message
        data = channel.read(2048)
        
        #self.logger.debug("received data: " + data)
        
        params = data.split('|')

        #params[0] is user
        #params[1] is the user password
        #params[2] is the type of password
        #params[3] is the new password for the dashboard
        
        self.user = params[0].strip()           
        passwd = params[1].strip()
        passwdtype = params[2].strip()
        dashboardpasswd=(params[3])
                
        if len(params) != self.numparams:
            msg = "ERROR: incorrect message"
            self.errormsg(channel, msg)
            #break
            return
        retry = 0
        maxretry = 3
        endloop = False
        while (not endloop):
            userCred = FGCredential(passwdtype, passwd)
            if self.auth(userCred):    
                channel.write("OK")            
                endloop = True                
            else:                
                retry += 1
                if retry < maxretry:
                    channel.write("TryAuthAgain")
                    passwd = channel.read(2048)
                else:
                    msg = "ERROR: authentication failed"
                    endloop = True
                    self.errormsg(channel, msg)
                    return
        
        leave=True
        cmd = "keystone user-list"
        p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
        std = p.communicate()
        if p.returncode != 0:
            status = "ERROR: getting user information. " + std[1]
            self.logger.error(status)
        else:
            status = "ERROR: User not found."
            for i in std[0].split("\n"):
                if not re.search("^\+",i) and i.strip() != "":
                    i="".join(i.split()).strip()
                    parts=i.split("|")
                    if parts[0]=="":
                        add=1
                    else:
                        add=0
                    print parts
                    if re.search("^javi$",parts[3+add].strip()):
                        print parts[0+add] +"-"+ parts[3+add]
                        useridOS = parts[0+add]
                        leave = False
                        status = "OK"
                        break            
            
        if not leave:
            cmd = "keystone user-password-update --pass " + dashboardpasswd + " " + useridOS
            p = Popen(cmd.split(), stdout=PIPE, stderr=PIPE)
            std = p.communicate()
            if p.returncode != 0:
                status = "ERROR: updating user password. " + std[1]
                self.logger.error(status)
            else:
                status = "OK"
        
        if (re.search('^ERROR', status)):
            self.errormsg(channel, status) 
        else: 
            channel.write(str(status))             
            channel.shutdown(socket.SHUT_RDWR)
            channel.close()

        end_all = time.time()
        self.logger.info('TIME walltime image generate:' + str(end_all - start_all))
        self.logger.info("Password Stack DONE")
    
    def errormsg(self, channel, msg):
        self.logger.error(msg)
        try:    
            channel.write(msg)                
            channel.shutdown(socket.SHUT_RDWR)
            channel.close()
        except:
            self.logger.debug("In errormsg: " + str(sys.exc_info()))
        self.logger.info("Password Stack DONE")


def main():
       
    
    passwdstackserver = PasswdStackServer()
    
    passwdstackserver.start()            
        

if __name__ == "__main__":
    main()
#END
