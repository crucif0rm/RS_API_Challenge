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
        print "Usage: -d domain.com -n ip.add.re.ss -c my new site\n"
        print "Usage: domain            ip             comment\n"

        parser = argparse.ArgumentParser(description='cloud files container upload')

        parser.add_argument('--domain', '-d', required=True, help='Domain name?')
        parser.add_argument('--ip', '-n', required=True, help='IP address?')
        parser.add_argument('--comment', '-c', required=True, help='Comment?')
        args = parser.parse_args()

        dns = pyrax.cloud_dns

        domain = args.domain
        ip_addr = args.ip
        comms = args.comment

        try:
            dom = dns.find(name=domain)
        except exc.NotFound:
            answer = raw_input("The domain '%s' was not found. Do you want to create it? [y/n]" % domain)
            if not answer.lower().startswith("y"):
                sys.exit()
            try:
                dom = dns.create(name=domain, emailAddress="admin@rackspace.com", ttl=900, comment=comms)
            except exc.DomainCreationFailed as nope:
                print "Domain creation failed:", nope

        recnfo = {"type": "A", "name": domain, "data": ip_addr, "ttl": 3000}
        recs = dom.add_records([recnfo])
        print "\nSuccessfully added %s with A record pointed to %s\n" % (domain, ip_addr)

if __name__ == '__main__':
    main()
