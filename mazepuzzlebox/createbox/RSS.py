import sys
import logging
import shelve
import time
from feedcache import cache
from datetime import date
from django.conf import settings
cacheFile=settings.ROOT_DIR + "mazepuzzlebox/.feedcache"


feed = 'http://www.mattvenn.net/feed/?tag=mazepuzzlebox'
ttl = 60 * 60 #1 hour
def getLatestNews():
    ret = []
    storage = shelve.open(cacheFile)
    url = ''
    summary = ''
    title = ''
    datepub = ''
    try:
        fc = cache.Cache(storage,timeToLiveSeconds=ttl)
        data = fc.fetch(feed)
        for entry in data.entries:
            try:
                url = unicode(entry.link, channels.encoding)
                summary = unicode(entry.description, channels.encoding)
                title = unicode(entry.title, channels.encoding)
            except:
                url = entry.link
                summary = entry.description
                title = entry.title
        
            date = entry.updated_parsed
            datestr = time.strftime('%d/%m/%Y',date)
            ret.append( { 'url' : url, 'summary' : summary, 'title' : title , 'date' : datestr } )
        
    except Exception, e:
        #nothing
        logging.warn( e )
        ret=[]
    finally:
        storage.close()

    return ret 
    return ret[0:4]
