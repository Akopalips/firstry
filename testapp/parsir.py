from html.parser import HTMLParser
from html.entities import name2codepoint
import urllib.request, sys, os


global total

class MyHTMLParser ( HTMLParser ):
    
    flag = False
    
    def handle_starttag ( self, tag, attrs ):
        if tag == "h1" or tag == "title":
            print  ( tag , ' :')
            self.flag = True   
            
    def handle_data ( self, data ):
        if self.flag == True:
            print  ( data )

    def handle_endtag ( self, tag ):
        self.flag = False
    
class Parsir:
    
    def print_title_h1 ( self,  url ):
        
        try:
            for_pars = urllib.request.urlopen ( url )
            mybytes = for_pars.read ()
            info = str ( for_pars.info () )
            for_pars.close ()
            charset = info [ info.find ( 'charset=' ) + 8 : info.find ( '\n',info.find ( 'charset=' ) ) ]
            del info
            mystr = mybytes.decode ( charset )
            parser = MyHTMLParser ()
            parser.feed ( mystr )
        except Exception as err:
            print ( 'Error: ', err, end='')
    
    def return_title_h1 ( self, url ):

        temp_out = open ( 'temp_out.temp', 'w' )
        old_out = sys.stdout
        sys.stdout = temp_out
        self.print_title_h1 ( url )
        sys.stdout = old_out
        temp_out.close ()

        temp_out = open ( 'temp_out.temp', 'r' )
        total = temp_out.read ()
        temp_out.close ()
        os.remove ( 'temp_out.temp' )
        return ( total )
