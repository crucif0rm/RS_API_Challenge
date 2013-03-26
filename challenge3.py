#!/usr/bin/env python

import os
import sys
import time
import pyrax
import pyrax.exceptions as exc
from time import sleep
import argparse

def main():

	credz = os.path.expanduser("~/.rackspace_cloud_credentials")

	try:
		pyrax.set_credential_file(credz)
	except exceptions.AuthenticationFailed:
		print "\n\nAuth failed, possibly wrong info in .rackspace_cloud_credentials"
	if pyrax.identity.authenticated:
		print '-'*15, '\n', "Auth successful as %s" % pyrax.identity.username, '\n', '-'*15
	else:
		print "Authentication failed."
		sys.exit(1)

	parser = argparse.ArgumentParser(description='cloud files container upload')
	parser.add_argument('--folder', '-f', required=True, help='-f Folder name?')
	parser.add_argument('--name', '-n', required=True, help='-n Local file name to upload?')
	args = parser.parse_args()

	cf = pyrax.cloudfiles
	container = args.folder
	filename = args.name

	try:
		cont = cf.get_container(container)
		print '-'*15, "\nContainer %s exists, attempting upload.." % cont.name, '\n', '-'*15
		time.sleep(2)
	except exc.NoSuchContainer:	
		cont = cf.create_container(container)
		print "Container %s created, attempting upload.." % cont.name

	try:
		with open(filename): pass
	except IOError:
		print "This file %s does not exist on your local system." % cont.name

	print '-'*15, "\nUploading %s from your local system.." % filename, '\n', '-'*15
	time.sleep(2)
	try:
		object = cf.upload_file(cont.name, filename)
		print '-'*15, '\n'
		print "Upload completed."
		print "cdn_enabled", cont.cdn_enabled
		print "cdn_ttl", cont.cdn_ttl
		print '\n', '-'*15
	except exc.UploadFailed:
		print "Upload Failed."

if __name__ == '__main__':
	main() 
