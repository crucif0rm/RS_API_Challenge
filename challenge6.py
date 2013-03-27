#!/usr/bin/env python

import os
import sys
import time
import pyrax
import pyrax.exceptions as exc
from time import sleep

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

        cf = pyrax.cloudfiles
        ctnr = cf.list_containers()
        c_ttl = 900
        print "Current Containers:\n"
        for c in ctnr:
            print c
        print '-'*15, '\n', "Please type a container name then press ENTER to CDN enable it\n", '-'*15, '\n'
        ctnrn = raw_input("Container:")

        container = cf.create_container(ctnrn)
        container.make_public(ttl=c_ttl)
        cont = cf.get_container(container)

        print '\n', '-'*15, '\n'
        print "cdn_enabled", cont.cdn_enabled
        print "cdn_ttl", cont.cdn_ttl
        print "cdn_uri", cont.cdn_uri
        print "cdn_ssl_uri", cont.cdn_ssl_uri
        print "cdn_streaming_uri", cont.cdn_streaming_uri
        print '\n', '-'*15


if __name__ == '__main__':
    main()
