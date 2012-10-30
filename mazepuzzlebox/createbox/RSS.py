import sys
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
            url = entry.link
            summary = entry.description
            title = entry.title
        
            print summary
            date = entry.updated_parsed
            datestr = time.strftime('%d/%m/%Y',date)
            ret.append( { 'url' : url, 'summary' : summary, 'title' : title , 'date' : datestr } )
        
    finally:
        storage.close()

    return ret[0:4]
