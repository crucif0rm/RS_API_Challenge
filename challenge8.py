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

        cf = pyrax.cloudfiles
        dns = pyrax.cloud_dns
        indexfile = "index.html"
        index_data = "<html>\n<body>\n<h1>Welcome to the internet</h1>\n"

        cont = cf.create_container("index")
        cont.make_public(ttl=900)
        uppit = cont.store_object(indexfile, index_data)
        print "Uploaded %s" % uppit, '\n', '-'*15
        cont.set_web_index_page(indexfile)
        dom_n = "superc00lwebsite.com"
        dom_e = "matt@crucif0rm.com"
        domain = dns.create(name=dom_n, emailAddress=dom_e)
        name = "cdn." + dom_n
        recadd = {"type": "CNAME", "name": name, "data": cont.cdn_uri, "ttl":900}
        fin = domain.add_records(recadd)
        print fin

if __name__ == '__main__':
    main()
