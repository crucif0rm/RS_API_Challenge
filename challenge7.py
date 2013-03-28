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
        clb = pyrax.cloud_loadbalancers

        simg = [image for image in cs.images.list()
            if "Ubuntu 12.04" in image.name][0]
        sflavor = [flavor for flavor in cs.flavors.list()
            if flavor.ram == 512][0]

        srv1 = cs.servers.create("web1", simg, sflavor)
        srv1_id = srv1.id
        srv2 = cs.servers.create("web2", simg, sflavor)
        srv2_id = srv2.id
        print "web1 and web2 build in progress..\n"
        while not (srv1.networks and srv2.networks):
                time.sleep(10)
                srv1 = cs.servers.get(srv1_id)
                srv2 = cs.servers.get(srv2_id)
        print "..build complete.\n", '-'*15, '\n'
        print "IP INFORMATION\n"
        print "WEB1 ", "PUBLIC:", srv1.networks["public"][0], "PRIVATE:", srv1.networks["private"][0],'\n'
        print "WEB2 ", "PUBLIC:", srv2.networks["public"][0], "PRIVATE:", srv2.networks["private"][0],'\n'
        print '-'*15, '\n'

        srv1_pip = srv1.networks["private"][0]
        srv2_pip = srv2.networks["private"][0]

        node1 = clb.Node(address=srv1_pip, port=80, condition="ENABLED")
        node2 = clb.Node(address=srv2_pip, port=80, condition="ENABLED")

        lbn = "web lb"
        vip = clb.VirtualIP(type="PUBLIC")
        lb = clb.create(lbn, port=80, protocol="HTTP", virtual_ips=[vip], nodes=[node1, node2])
        print "Load Balancer:", lb.name
        print "STATUS:", lb.status
        print "ID:", lb.id
        print "Virtual IPs:", lb.virtual_ips
        print '-'*15

if __name__ == '__main__':
    main()
