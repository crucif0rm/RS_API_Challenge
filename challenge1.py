#!/usr/bin/env python

import os
import sys
import time
from time import sleep
import pyrax
import argparse


def main():
	parser = argparse.ArgumentParser(description='server build script')
	parser.add_argument('--count', '-c', default=3, type=int, help='how many servers?')
	parser.add_argument('--name', '-n', required=True, help='server name prefix?')
	args = parser.parse_args()

	credz = os.path.expanduser("~/.rackspace_cloud_credentials")

	try:
		pyrax.set_credential_file(credz)
	except exceptions.AuthenticationFailed:
		print "Auth failed, possibly wrong info in .rackspace_cloud_credentials"

		if pyrax.identity.authenticated:
			print "Authentication was successful with user %s" % pyrax.identity.username
		else:
			print "Authentication failed."
		sys.exit(1)

	cs = pyrax.cloudservers	
	simg = [image for image in cs.images.list()
		if "Ubuntu 12.04" in image.name][0]
	sflavor = [flavor for flavor in cs.flavors.list()
		if flavor.ram == 512][0]

	for count in xrange(1, args.count +1):
		sname = args.name + str(count)
		pre_server = cs.servers.create(sname, simg.id, sflavor.id)
		built_server = {'ID' : pre_server.id, 'status' : pre_server.status, 'admin_pass' : pre_server.adminPass}
		print '\n'
		print "Building server %s, if it fails I will let you know." % sname
		
		status_server = cs.servers.get(pre_server.id)	
		while status_server.status != 'ACTIVE':
			sleep(10)
			status_server = cs.servers.get(pre_server.id)
			if status_server.status == "ERROR" or status_server.status == "UNKNOWN":	
				print "Server build failure, current state: %s" % status_server.status
		network = status_server.networks
		os.system("clear")
		print '\n\n'
		print '-'*15
		print "BUILD COMPLETE"
		print '-'*15
		print "Server Name:", status_server.name
		print "Public IP:", status_server.networks['public']
		print "Admin Password: ", built_server['admin_pass']
		print '-'*15

if __name__ == '__main__':
	main()
