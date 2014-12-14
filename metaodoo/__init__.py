from optparse import OptionParser
import psycopg2
import json
from os import path, mkdir
from psycopg2 import OperationalError

def get_connection(user, db):
    try:
        connection = "dbname=%s user=%s" % (db, user)
        conn = psycopg2.connect(connection)
    except OperationalError as exc:
        raise Exception("Authentication failed")

    return conn

def get_modules(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM ir_module_module where state = 'installed';")

    ret = []
    for record in cur:
        ret.append(record[0])

    cur.close()

    return ret

def make_module(directory, modules):
    outDirectory = path.join(directory, "meta_package")
    outInit = path.join(outDirectory, "__init__.py")
    outManifest = path.join(outDirectory, "__openerp__.py")

    module = {
        "name": "MetaPackage",
        "version": "1.0",
        "category": "dev",
        "description": "Extract modules",
        "author": 'Savoir-faire Linux',
        "website": 'http://www.savoirfairelinux.com',
        "depends": modules,
        "installable": True,
        "auto_install": False,
    }

    if not path.exists(outDirectory):
        mkdir(outDirectory)

    if not path.exists(outInit):
        with open(outInit, "w") as init:
            init.write("")

    with open(outManifest, "w") as out:
        json.dump(module, out, indent=4)

    return module


def main():
    parser = OptionParser()
    parser.add_option("-o", "--addons", dest="addons", default=".",
            help="Directory where to save the module")
    parser.add_option("-u", "--user", dest="user", type="string",
            help="Username")
    parser.add_option("-d", "--db", dest="db", type="string",
            help="Database name")
    parser.add_option("-i", "--interactive", dest="interactive",
            action="store_true", default=False,
            help="Prompt variables interactively")

    (options, args) = parser.parse_args()

    user = options.user
    db = options.db
    addons_folder = options.addons

    if (not user or not db) and not options.interactive:
        parser.print_help()
    else:
        if options.interactive:
            user = raw_input("User > ").replace("\n", "")
            db = raw_input("DBName > ").replace("\n", "")

        conn = get_connection(user, db)
        modules = get_modules(conn)

        print("Modules extracted")
        
        if options.interactive:
            addons_folder = raw_input("Addons directory > ")

        make_module(addons_folder, modules)

if __name__ == '__main__':
    main()
