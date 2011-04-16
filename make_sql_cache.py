#! /usr/bin/env python
# Author: Alex Ksikes (alex.ksikes@gmail.com)

import getpass
import web

import sql_cache

def run(db_name, drop=False):
    db = web.database(dbn='mysql', 
        db=db_name, 
        user=raw_input('User: '), 
        passwd=getpass.unix_getpass('Password: ')
    )
    sql_cache.Cache.make_sql_table(db, drop)
    
def usage():
    print 'Usage:' 
    print '    python make_sql_cache.py [options] db_name'
    print 
    print 'Description:' 
    print '    Makes the required sql table.'
    print 
    print 'Options:' 
    print '    -d, --drop              : drop cache sql table if it exists'
    print '    -h, --help              : this help message'
    print
    print 'Email bugs/suggestions to Alex Ksikes (alex.ksikes@gmail.com)' 

import sys, getopt
def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'dh', ['drop', 'help'])
    except getopt.GetoptError:
        usage(); sys.exit(2)
    
    drop = False
    for o, a in opts:
        if o in ('-d', '--drop'):
            drop = True
        elif o in ('-h', '--help'):
            usage(); sys.exit()
    
    if len(args) < 1:
        usage()
    else:
        run(args[0], drop)
        
if __name__ == '__main__':
    main()