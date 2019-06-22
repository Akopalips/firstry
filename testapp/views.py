from django.shortcuts import render
from .parsir import Parsir
from .models import Site2pars
from datetime import datetime
import sqlite3


def Parsing_result(row):
	parsed = ''
	logs = row[0] + ':	' + row[1]
	parsed_page = Parsir() .return_title_h1(row[1])

	# time check #"%Y-%m-%d %H:%M:%S"
	if datetime.now() >= datetime.strptime(str(row[0]), "%Y-%m-%d %H:%M:%S"):
		if parsed_page[:5] == 'Error':
			logs += '\n	' + parsed_page
		else:
			parsed = row[1] + ':\n' + parsed_page
	logs += '\n'
	return [logs, parsed]


class Parsed_and_Logs:


	def __init__(self, db_file):

		# connect to db to create table with parsed results
		self.db_conn = sqlite3.connect(db_file)
		self.cursor_db = self.db_conn.cursor()
		self.cursor_db.execute("""	CREATE TABLE IF NOT EXISTS Parsing_result 
								(  
									URL varchar(200) primary key not null , 
									Logs_result text not null, 
									Parsing_result text not null 
								);""")
		self.parsed = ''
		self.logs = ''


	def return_Parsed_h1_title_and_Logs(self):

		# take already parsed urls
		# columns: 'id'-'url'-'date/time'
		for row in self.cursor_db.execute("	select * from Parsing_result"):
			self.parsed += row[2]
			self.logs += row[1]

		# parsing new urls
		# columns: 'parsed_date'-'date/time'-'url'
		for row in self.cursor_db.execute("""select testapp_site2pars.time, testapp_site2pars.URL 
										from testapp_site2pars 
										left join Parsing_result on Parsing_result.URL = testapp_site2pars.URL 
										where Parsing_result.URL IS NULL;"""):
			result = Parsing_result(row)
			self.cursor_db.executescript(
									f'	insert into Parsing_result values ("{row[1]}","{result[0]}","{result[1]}");')
			self.parsed += result[1]
			self.logs += result[0]

		return [self.parsed,self.logs]


	def __del__(self):

		del self.cursor_db
		self.db_conn.close()


def main(request):

	parsed_logs = Parsed_and_Logs('db.sqlite3')
	result = parsed_logs.return_Parsed_h1_title_and_Logs()

	try:
		return render(request, 'testapp/main.html', { 'PARSED': result[0], 'LOGS': result[1],'for_test': for_test})
	except:
		return render(request, 'testapp/main.html', { 'PARSED': result[0], 'LOGS': result[1]})
