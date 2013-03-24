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
	server = cs.servers.get("9e6796cd-983d-4101-9cc2-6a464804fbb5")
	
	imgn = server.name + strftime("_%m%d-%H%M", gmtime())
	server.create_image(imgn)
	print '\n', "Image creation started.. please wait.", '\n'
	server_name = server.name + "-clone"
	
	flavor = server.flavor['id']
	image = [img for img in cs.images.list()
		if imgn in img.name][0]

	pyrax.utils.wait_until(image, "status", ['ACTIVE','ERROR'], interval=60, attempts=40, verbose=True)
	
	new_server = cs.servers.create(server_name, image.id, flavor)
	status_server = cs.servers.get(new_server.id)
	network = status_server.networks
	
	ip4 = network["public"][0] if ":" in network["public"][1] else network["public"][1]

	print '-'*15, "Image creation successful", '\n', '-'*15, '\n', "Image:", new_server.name, '\n', "ID:", new_server.id, '\n', '-'*15, "Build from image started.. please wait.", '\n'
	
	pyrax.utils.wait_until(new_server, "status", ['ACTIVE','ERROR'], interval=30, attempts=40, verbose=False)
	
	print '-'*15, '\n', "Root Pass:", new_server.adminPass, '\n', "Public IP:", ip4, '\n', '-'*15



#	flavor = [flavor for flavor in cs.flavors.list()
#		if flavor.ram == 512][0]
#	server = cs.servers.list()[0]
#	imgn = server.name + strftime("_%Y%m%d-%H%M%S", gmtime())
#	imgd = cs.servers.create_image(server.id, imgn)
#	network = server.networks
#	ip4 = network['public'][0] if ":" in network['public'][1] else network['public'][1]
#	
#	active = False
#
#	while not active:
#		sleep(30)
#		imgl = cs.images.list()
#		for image in imgl:
#			if image.id == imgd:
#				if image.status == 'ACTIVE':
#					server = cs.servers.create(image.name, image.id, flavor.id)
#					print "Name:", server.name
#					print "ID:", server.id
#					print "Status:", server.status
#					print "Root Pass:", server.adminPass
#					print "Networks:", ip4
#					active = True
if __name__ == '__main__':
	main()
