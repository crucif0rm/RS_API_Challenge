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

        cs = pyrax.cloudservers
        dns = pyrax.cloud_dns

        #image list
        image_lst = cs.images.list()
        print "\nCurrent Images:\n"
        for i in image_lst:
            print i
        print '-'*15, '\n', "Please type the image name then press ENTER.\n", '-'*15, '\n'
        image_lstn = raw_input("Image:")
        print '\n', '-'*15, '\n'

        #flavor list
        flavor_lst = cs.flavors.list()
        print "\nCurrent Flavors:\n"
        for b in flavor_lst:
            print b
        print '-'*15, '\n', "Please type the flavor size then press ENTER.\n", '-'*15, '\n'
        flavor_lstn = raw_input("Flavor:")
        print '\n', '-'*15, '\n'

        #assign new var names
        flvr = flavor_lstn
        imge = image_lstn

        #setup FQDN
        print "Please enter your FQDN (domain.com) then press ENTER.\n", '-'*15, '\n'
        fque = raw_input("FQDN:")
        fname = fque

        srvb = cs.servers.create(fname, imge, flvr)
        srvb_id = srvb.id
        print '\n', '-'*15, "\nServer build in progress..\n"
        while not (srvb.networks):
            time.sleep(10)
            srvb = cs.servers.get(srvb.id)
        print "..build complete.\n", '-'*15, '\n'

        #IP info
        ip_addr_pub = srvb.networks["public"][0]
        ip_addr_priv = srvb.networks["private"][0]

        #create DNS records
        dom = dns.create(name=fname, emailAddress="admin@rackspace.com", ttl=900, comment="Challenge 9")
        recnfo = {"type": "A", "name": fname, "data": ip_addr_pub, "ttl": 3000}
        recs = dom.add_records([recnfo])
        print "Server:", srvb.name
        print "Domain:", fname
        print "IPs: %s & %s" % (ip_addr_pub, ip_addr_priv)

if __name__ == '__main__':
    main()
