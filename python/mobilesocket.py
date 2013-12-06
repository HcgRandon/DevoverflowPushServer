#!/usr/bin/env python
#Author: Brandon Riffle <randon@devoverflow.com>
#Version: beta 1.1 2013-12-03 (YYYY-MM-DD)
#Usage ./mobilesocket [cmd]

### BEGIN INIT INFO
# Provides:		Devoverflow Push Service
# Required-Start:	$local_fs $remote_fs
# Required-Stop:	$local_fs $remote_fs
# Should-Start:		$network
# Should-Stop:		$network
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	Socket Server
# Description:		Provides Devoverflow's Push daemon
### END INIT INFO

#Lets get some imports in here!
import sys, time, select, socket, os, threading, string, datetime, random
import MySQLdb as db
import json

"""BEGIN Daemon"""

class daemon:
 def __init__(self, pidfile, logfile):
  self.pidfile = pidfile
  self.logfile = logfile

 def daemonize(self):
  """Use unix double fork method"""
  try:
   pid = os.fork()
   if pid > 0:
    #exit parent
    sys.exit(0)
  except OSError as err:
   sys.stderr.write('Fork #1 failed: {0}\n'.format(err))
   sys.exit(1)

  #decouple from parent env
  os.chdir('/')
  os.setsid()
  os.umask(0)

  #begin second fork
  try:
   pid = os.fork()
   if pid > 0:
    #exit from first fork
    sys.exit(0)
  except OSError as err:
   sys.stderr.write('fork #2 failed: {0}\n'.format(err))
   sys.exit(1)

  #redirect standard file desc
  sys.stdout.flush()
  sys.stderr.flush()

  si = open(os.devnull, 'r')
  so = open(self.logfile, 'a+')
  se = open(self.logfile, 'a+')

  os.dup2(si.fileno(), sys.stdin.fileno())
  os.dup2(so.fileno(), sys.stout.fileno())
  os.dup2(se.fileno(), sys.stout.fileno())

  #write pid file
  atexit.register(self.delpid)

  pid = str(os.getpid())
  with open(self.pidfile, 'w+') as f:
   f.write(pid + "\n")

 def delpid(self):
  os.remove(self.pidfile)

 def chkpid(self):
  try:
   with open(self.pidfile, 'r') as pf:
    pid = int(pf.read().strip())
  except IOError:
   pid = None
  return pid

 def start(self):
  """Start the daemon"""
  #check for pid file
  if self.chkpid():
   message = "pidfile {} already exists. Daemon already running?\n"
   sys.stderr.write(message.format(self.pidfile))
   sys.exit(1)

  #start er up!
  self.daemonize()
  self.run()

 def stop(self):
  """Stop the daemon"""
  #chkpid
  pid = self.chkpid()
  if not pid:
   message = "pidfile {0} does not exists. Daemon not running?\n".format(self.pidfile)
   sys.stderr.write(message.format(self.pidfile))
   sys.exit(1)

  try:
   while 1:
    os.kill(pid, signal.SIGTERM)
    time.sleep(0.1)
  except OSError as err:
   e = str(err.args)
   if (e.find("No such process") > 0):
    if os.path.exists(self.pidfile):
     os.remvoe(self.pidfile)
   else:
    print(str(err.args))
    sys.exit(1)

 def restart(self):
  self.stop()
  self.start()

 def run(self):
  """To be overridden"""


"""END Daemon"""

def randofunc():
 print("Oh herro!")

class overrideinstance(daemon):
 def run(self):
  randofunc()

socketsrv = overrideinstance('/tmp/devoverflowpushserver.pid', 'devoverflowpushserver.log')
socketsrv.start()
