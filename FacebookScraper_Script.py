
# import some Python dependencies
import json
import datetime
import csv
import time
#Since Python3, urllib is divided in 3, therefore, is necessary to import them separately
import urllib.request
import urllib.response
import urllib.error
import pyodbc


#app_id = "272535582777707"
#app_secret = "59e7ab31b01d3a5a90ec15a7a45a5e3b" 

#CHANGE IT. For now use the access_token from facebook graph API (This code chance hourly)
access_token = "EAACEdEose0cBAATDmYxzM2gajgplKbN1rVElc91ZAwiQjZCRuOLsCzLPrOY5r2KQuUBOCikZB8CLtbB04XYt2YYZCEoU8hRHTb5WKvTwYvSHoZAfuvy8jyzKIq6Uz7cCaOdWJEZBWiYwZCov0OSqAPf5LbcKBZB6Bi3o2Lv1wP7JSAZDZD"
page_id = 'crhoy.comnoticias'


def testFacebookPageData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data 
    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req).read().decode('utf8') # le agregué el decode porque json.load() no puede cargar bytes, necesita un string
    data = json.loads(response)
    
    print (json.dumps(data, indent=4, sort_keys=True))
    

testFacebookPageData(page_id, access_token)

# When scraping large amounts of data, here's a high probability to hit an HTTP Error 500 (Internal Error)
# This helper function catch the error and try again after a few seconds.
def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib.request.urlopen(req)
            if response.getcode() == 200: 
                success = True
        except Exception as e:
            print (e)
            time.sleep(5)
            
            print ("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return response.read().decode('utf8')


def testFacebookPageFeedData(page_id, access_token):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id + "/feed" # changed
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    #print (json.dumps(data, indent=4, sort_keys=True))
    

testFacebookPageFeedData(page_id, access_token)


def getFacebookPageFeedData(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com/v2.4"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=message,link,created_time,type,name,id,likes.limit(1).summary(true),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # changed
    #parameters = "/?access_token=%s" % access_token
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data
    #print (json.dumps(data, indent=4, sort_keys=True))
    
test_status = getFacebookPageFeedData(page_id, access_token, 1)["data"][0]
#print (json.dumps(test_status, indent=4, sort_keys=True))    


def processFacebookPageFeedStatus(status):

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else status['message'] 
    link_name = '' if 'name' not in status.keys() else status['name']
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else status['link']
    
    status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) 
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')
    
    # Nested items require chaining dictionary keys.
    num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']
    
    # return a tuple of all processed data
    return (status_id, status_message, link_name, status_type, status_link,
           status_published, num_likes, num_comments, num_shares)

processed_test_status = processFacebookPageFeedStatus(test_status)
print ('Data Set example: {0} \n' .format(processed_test_status))


def scrapeFacebookPageFeedStatus(page_id, access_token):
    # Connection string (CHANGE IT)
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=CHANGEIT;DATABASE=CHANGEIT;UID=CHANGEIT;PWD=CHANGEIT')
    cursor = cnxn.cursor()

    # To write a .csv file in the Python WD
    #with open('%s_facebook_statuses.csv' % page_id, 'w') as file:
    #    w = csv.writer(file)
    #    w.writerow(["status_id", "status_message", "link_name", "status_type", "status_link", 
    #               "status_published", "num_likes", "num_comments", "num_shares"])
        
    has_next_page = True
    num_processed = 0   # keep a count on how many we've processed
    scrape_starttime = datetime.datetime.now()
        
    print ("Scraping %s Facebook Page: %s\n" % (page_id, scrape_starttime))
        
    statuses = getFacebookPageFeedData(page_id, access_token, 100)
        
    while has_next_page:
        for status in statuses['data']:
            # This line write the data to the .csv file
            #w.writerow(processFacebookPageFeedStatus(status))
            processed_status = processFacebookPageFeedStatus(status)

            try:
                cursor.execute("Insert Into DOTAAC_Feeds (PageId, FeedId, FeedMessage, LinkName, FeedType, FeedLink, PublishedDate, LikesCount, CommentsCount, SharesCount, FeedStatus) Values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 265769886798719, processed_status[0], processed_status[1], processed_status[2], processed_status[3], processed_status[4], processed_status[5], processed_status[6], processed_status[7], processed_status[8], 1)
                cnxn.commit()
            except:
                cnxn.rollback()

            # output progress occasionally to make sure code is not stalling
            num_processed += 1
            if num_processed % 1000 == 0:
                print ("%s Statuses Processed: %s" % (num_processed, datetime.datetime.now()))
                    
        # if there is no next page, we're done.
        if 'paging' in statuses.keys():
            statuses = json.loads(request_until_succeed(statuses['paging']['next']))
        else:
            has_next_page = False
        print ("Feeds processed: %s" %( num_processed))

        # If you want to scrape all page feeds, comment this if-else section; scrape only a portion of it set the number in the if condition
        if num_processed == 100:
            has_next_page = False
        else:
            has_next_page = True

    cnxn.close()
        
    print ("\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - scrape_starttime))

scrapeFacebookPageFeedStatus(page_id, access_token)
