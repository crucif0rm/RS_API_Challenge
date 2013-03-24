#!/usr/bin/env python

import os
import sys
import time
from time import sleep, strftime, gmtime
import pyrax

def main():

	credz = os.path.expanduser("~/.rackspace_cloud_credentials")

	try:
		pyrax.set_credential_file(credz)
	except exceptions.AuthenticationFailed:
		print '\n\n'
		print "Auth failed, possibly wrong info in .rackspace_cloud_credentials"
	if pyrax.identity.authenticated:
		print '-'*15, '\n', "Auth successful as %s" % pyrax.identity.username, '\n', '-'*15
	else:
		print "Authentication failed."
		sys.exit(1)


	cs = pyrax.cloudservers
	server = cs.servers.get("b04bb6c4-e763-4f31-a3d4-76016903f02e")
	imgn = server.name + strftime("_%m%d-%H%M", gmtime())
	imgnstr = str(imgn)
	server.create_image(imgnstr)
	print "\nImage creation started.. please wait.\n"
	
	server_name = server.name + "-clone"
	
	flavor = server.flavor['id']
	servimage = [img for img in cs.images.list()
		if imgnstr in img.name][0]


	pyrax.utils.wait_until(servimage, "status", ['ACTIVE','ERROR'], interval=20, attempts=40, verbose=True)
	
	new_server = cs.servers.create(server_name, servimage.id, flavor)
	new_serverid = new_server.id
	
	print '-'*15, "\nServer:", new_server.name, '\n', "ID:", new_server.id, '\n', '-'*15, "\nRoot Pass:", new_server.adminPass, '\n'
	while not (new_server.networks):
		time.sleep(10)
		new_server = cs.servers.get(new_serverid)			
	
	print '-'*15, '\n', "Public IP:", new_server.networks["public"][0], '\n', '-'*15	
	

if __name__ == '__main__':
	main()
