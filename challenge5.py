#!/usr/bin/env python

import os
import sys
import time
import pyrax
import pyrax.exceptions as exc
from time import sleep
import argparse
import string
import random

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

        parser = argparse.ArgumentParser(description='cloud database creation')
        parser.add_argument('--database', '-d', required=True, help='DB name?')
        parser.add_argument('--name', '-n', required=True, help='user name?')
        args = parser.parse_args()

        def passgen(size=12, chars=string.ascii_uppercase + string.digits + string.lowercase):
            return ''.join(random.choice(chars) for x in range(size))

        cdbn = args.database
        cdbun = args.name
        instname = "challenge 5"
        cdb = pyrax.cloud_databases
        instance = cdb.create(cdbn, flavor=1, volume=1)
        cdbp = passgen()

        print "\nBuilding your database, please wait..\n"
        pyrax.utils.wait_until(instance, "status", ['ACTIVE', 'ERROR'], interval=30, verbose=True)

        db = instance.create_database(instname)
        user = instance.create_user(name=cdbun, password=cdbp, database_names=[db])
        print '-'*15, "\nBuild complete.\n", '-'*15, "\nDB: %s\nUser: %s\nPass: %s\n" % (cdbn, cdbun, cdbp)

if __name__ == '__main__':
    main()
