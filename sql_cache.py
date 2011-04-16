'''A simple key-value MySQL store for small chunks of arbitrary data.

You need a table of the following schema:

create table cache (
    _key                    varchar(32) primary key,
    query                   varchar(250),
    value                   text,
    sticky                  boolean,
    datetime                timestamp default current_timestamp,
    index (sticky),
    index (datetime)
) charset utf8 engine MyISAM;
'''

__author__ = 'Alex Ksikes (alex.ksikes@gmail.com)'

import base64
import md5
import cPickle as pickle
import web

DB = None
MAX_SIZE = 10000 # maximum allowed size including the sticky values

class Cache(object):
    def __init__(self, **db_params):
        if not db_params:
            db = DB
        elif len(db_params) == 1 and db_params.get('db'):
            db = db_params.pop('db')
        else:
            db = web.database(**db_params)
        self.db = db
        
    def get(self, query):
        key = self._make_key(query)
        r = self.db.select('cache', vars=dict(key=key), where='_key = $key', limit=1)
        r = web.listget(r, 0)
        
        value = None
        if r:
            if not r.sticky:
                self.db.query('update cache set datetime=now() where _key = $key', vars=dict(key=key))
            value = pickle.loads(base64.b64decode(r.value))
        return value
        
    def set(self, query, value, replace=False, sticky=False):
        key = self._make_key(query)
        value = base64.b64encode(pickle.dumps(value))
        
        sql = ('insert cache (_key, query, value, sticky) values ($key, $query, $value, $sticky) '
               'on duplicate key update datetime=now()')
        
        if replace:
            sql += ', query=$query, value=$value, sticky=$sticky'
        
        self.db.query(sql, vars=dict(key=key, query=query, value=value, sticky=sticky))
        self._delete_lru()
        
    def get_ifnot_set(self, query, value, replace=False, sticky=False):
        value = self.get(query)
        if not value:
            self.set(query, value, replace, sticky)
        return value
    
    def _delete_lru(self):
        r = self.db.query('select count(*) as size from cache')
        r = web.listget(r, 0)
        n = r.size - MAX_SIZE 
        if n > 0:
            self.db.query('delete from cache where sticky !=1 order by datetime limit %s' % n)
            
    def _make_key(self, query):
        return md5.new(_utf8(query)).hexdigest()

    @classmethod
    def clear(cls, db, also_sticky=False):
        if not also_sticky:
            where = 'sticky != 1'
        else:
            where = ''
        db.delete('cache', where=where)
        
    @classmethod
    def make_sql_table(cls, db, drop=False):
        if drop:
            db.query('drop table if exists cache')
        db.query(
        'create table cache ('
        '    _key            varchar(32) primary key,'
        '    query           varchar(250),'
        '    value           text,'
        '    sticky          boolean,'
        '    datetime        timestamp default current_timestamp,'
        '    index (sticky),'
        '    index (datetime)'
        ') charset utf8 engine MyISAM;'
        )

def set_DB(**db_params):
    global DB
    DB = web.database(**db_params)
    DB.printing = False

def get(query):
    return Cache(db=DB).get(query)
    
def set(query, value, replace=False, sticky=False):
    return Cache(db=DB).set(query, value, replace, sticky)

def clear(db=None, also_sticky=False):
    db = db or DB
    Cache.clear(db, also_sticky)

def make_sql_table(db=None, drop=False):
    db = db or DB
    Cache.make_sql_table(db, drop)

def _utf8(s):
    if isinstance(s, unicode):
        return s.encode("utf-8")
    assert isinstance(s, str)
    return s