from django.shortcuts import render
from .parsir import Parsir
from .models import Junpyth
from datetime import datetime
import sqlite3

def Parsing_result ( row ):
	PROGRESS = ''
	LOGS = row [ 0 ] + ':	' + row [ 1 ]
	parsed_page = Parsir () .return_title_h1 ( row [ 1 ] )
	if datetime.now () >= datetime.strptime ( str ( row [ 0 ] ), "%Y-%m-%d %H:%M:%S" ):	#time check #"%Y-%m-%d %H:%M:%S"
		if parsed_page [ :5 ] == 'Error':												#Error exist check
			LOGS += '\n	' + parsed_page
		else:
			PROGRESS = row [ 1 ] + ':\n' + parsed_page
	LOGS += '\n'
	return [LOGS, PROGRESS]



def main ( request ):
	db_conn = sqlite3.connect ( 'db.sqlite3' )
	cursor_db = db_conn.cursor ()
	cursor_db.execute ( "CREATE TABLE IF NOT EXISTS Parsing_result (  URL varchar(200) primary key not null , Logs_result text not null, Parsing_result text not null );" )
	PROGRESS = ''
	LOGS = ''
#id-url-d/t
	for row in cursor_db.execute ( "select * from Parsing_result" ):

		LOGS += row [ 1 ]
		PROGRESS += row [ 2 ]
#prs-d/t-url		
	for row in cursor_db.execute ( "select testapp_junpyth.time, testapp_junpyth.URL from testapp_junpyth left join Parsing_result on Parsing_result.URL = testapp_junpyth.URL where Parsing_result.URL IS NULL;" ):
			
		result = Parsing_result ( row )
		db_conn.cursor().executescript ( "insert into Parsing_result values (\"" + row [ 1 ] + "\", \"" + result [ 0 ] + "\", \"" + result [ 1 ] + "\");" )
		LOGS += result [ 0 ]
		PROGRESS += result [ 1 ]
		
	db_conn.close()


	try:
		return render ( request, 'testapp/main.html', { 'LOGS': LOGS , 'PROGRESS': PROGRESS, 'for_test':for_test } )
	except:
		return render ( request, 'testapp/main.html', { 'LOGS': LOGS , 'PROGRESS': PROGRESS } )