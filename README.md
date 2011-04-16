A simple key-value MySQL store for small chunks of arbitrary data (strings, objects).

Here is an example of usage:

    import sql_cache

    # setup the database
    sql_cache.set_DB(db='imdb', user='ale', passwd='3babes', dbn='mysql') 

    # setup cache size
    sql_cache.MAX_SIZE = 10000

    # make the cache table, drop it if it already exists
    sql_cache.make_sql_table(drop=True)

    # set some key value pairs
    sql_cache.set('query_1', [1,2,3])
    sql_cache.set('query_2', 'a string', sticky=True)
    sql_cache.set('query_3', {'a':1, 'b':2, 'c':3})

    # returns {'a':1, 'b':2, 'c':3}
    print sql_cache.get('query_3')

    # returns 'a string'
    print sql_cache.get('query_2')

    # clears the entire but not the sticky values
    sql_cache.clear(also_sticky=False)

    # returns None
    print sql_cache.get('query_1')

    # returns 'a string'
    print sql_cache.get('query_2')