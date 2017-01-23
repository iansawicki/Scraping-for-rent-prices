from bs4 import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime
import csv
import sys
import os
import smtplib
import config
import re
import requests as reqq


def parse_res(page):
	print page
	res = []
	#page = page.strip().replace(' ','+')
	#page_url = BURL.format(page)
	soup = BeautifulSoup(urlopen(page).read())
	#This is the equivalent of xpath searching through Doc Elements. 
	"""Important NOTE: This is culling through all of the results of the query. Not a single info page"""
	rows = soup.find('div','content').find_all('p','row')
	# Now we're batch applying a search inside the elements above
	for row in rows:
		print row
		url = 'http://chicago.craigslist.org' + row.a['href']
		create_date = row.find('time').get('datetime')
		title = row.find_all('a')[1].get_text().encode('utf-8').strip()
		try:
			hood = row.find_all('small')[0].get_text()
		except: 
			hood = 'na'
		try:
			price = row.find_all("span", { "class" : "price" })[0].get_text()#.encode('utf-8').strip()
		except:
			price = 'na'
		try:
			bed_count = row.find_all("span", { "class" : "housing" })[0].get_text()#.encode('utf-8').strip()
			bed_count = re.findall("([0-9].[Bb][A-Za-z]+|[0-9][Bb][A-Za-z])",bed_count)[0]
			bed_count = re.findall("[0-9]",bed_count)[0]
		except:
			bed_count = 'na'
		res.append({'url':url,'create_date':create_date,'title':title,'price':price,'bed_count':bed_count,'hood':hood})
	return res

def write_res(res):
	"""Write dictionaries to file"""
	with open(targ,'ab') as f:
		dw = csv.DictWriter(f,fieldnames=['url','create_date','title','price','bed_count','hood'],delimiter =',')
		dw.writerows(res)
	

if __name__ == '__main__':
	term = raw_input("What Chicago neighborhood do you want to collect rental price data on from Craiglist?\n")
	search_key = re.sub("\s","+",term)

	targ = re.sub("\s","_",term) 
	targ = term + '.csv'
	
	with open(targ,'w') as f:
		dw = csv.DictWriter(f,fieldnames=['url','create_date','title','price','bed_count','hood'],delimiter =',')
		dw.writer.writerow(dw.fieldnames)
		f.close()


	URL = 'http://chicago.craigslist.org/search/apa?query=%s' % search_key
	results = parse_res(URL)
	write_res(results)


		

