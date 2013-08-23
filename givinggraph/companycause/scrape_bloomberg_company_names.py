#!/usr/bin/env python
#
# Description: This scrapes Bloomberg Companies for all companies
# 	publicly listed on Bloomberg. The output is a .csv file that
#	contains the following company information:
# 	TICKER, NAME, EXCHANGE, WEBSITE, INDUSTRY, SECTOR, SUMMARY
#	Another .csv file is collected with the leadership of all
#	companies.
#

from BeautifulSoup import BeautifulSoup as bs
import urllib2
import unicodedata
import csv

# Write final data to filename CSVNAME
CSVNAME = 'bloomberg_companies_list.csv'
EXECSCSVNAME = 'bloomberg_companies_executives_list.csv'

def main():

	# Bloomberg has these pages on which all company names are listed on
	PAGES = ['0-9','a','b','c','d','e','f','g','h','i','j','k','l', \
		'm','n','o','p','q','r','s','t','u','v','w','x','y','z','other']

	# Initialize collector
	collectorTitle = ['TICKER','NAME','EXCHANGE','WEBSITE','INDUSTRY','SECTOR','SUMMARY']
	execCollectorTitle = ['TICKER','NAME','EXCHANGE',('POSITION TITLE','EXECUTIVE\'S NAME')]

	myCSVwriter(CSVNAME,collectorTitle,1)
	myCSVwriter(EXECSCSVNAME,execCollectorTitle[0:3] + [elt for tup in execCollectorTitle[3] for elt in tup],1)

	for p in PAGES:
		soup = bs(urllib2.urlopen('http://www.bloomberg.com/markets/companies/a-z/'+p+'/'))

		# Get remaining pages in the $p category, then loop over scraping those
		try:
			rem_pages = [str(i['href']) for i in soup.find('div',{'class':'dictionary_pagination'}).findAll('a')]
		except:
			rem_pages = []

		getPageData(soup)
		# print 'Finished 1st page of ' + p

		# Collect data on remaining pages of $p
		for r in rem_pages:
			getPageData(bs(urllib2.urlopen('http://www.bloomberg.com' + r )))
			# print 'Finished ' + r.replace('/markets/companies/a-z/b/','') + ' of page ' + p + '. Collected ' + str(len(collector)) + ' datapoints.'


def getPageData(soup):
	# Grab all companies listed on data table
	table = soup.find('table',{'class':'ticker_data'})

	# The following data (names, tickers, links) are collected in batch from table
	names = [unicodedata.normalize('NFKD',i.find('a').findChild().string).encode('ascii', 'ignore') for i in table.findAll('td',{'class':'name'})]
	tickers = [unicodedata.normalize('NFKD',i.string).encode('ascii', 'ignore') for i in table.findAll('td',{'class':'symbol'})]
	# links = [str(i.find('a')['href']) for i in table.findAll('td',{'class':'name'})] #this links to the Bloomberg page for company

	# Everything else is collected from the company profile page
	for ii in xrange(len(tickers)):
		# Get company TICKER
		ticker = tickers[ii]

		# Get company NAME
		name = names[ii]

		try:
			# Read company profile page and grab additional information
			profile = bs(urllib2.urlopen('http://www.bloomberg.com/quote/'+ticker+'/profile'))

			# Get company EXCHANGE
			exchange = unicodedata.normalize('NFKD',profile.find('div',{'class':'exchange_type'}).findAll('span')[1].string).strip().encode('ascii', 'ignore')

			# Get company WEBSITE
			website = unicodedata.normalize('NFKD',profile.find('a',{'rel':'nofollow','target':'_blank'}).string).encode('ascii', 'ignore')

			# Get company INDUSTRY
			industry = unicodedata.normalize('NFKD',profile.find('div',{'class':'exchange_type'}).findAll('span')[5].string).strip().encode('ascii', 'ignore')

			# Get company SECTOR
			sector = unicodedata.normalize('NFKD',profile.find('div',{'class':'exchange_type'}).findAll('span')[3].string).strip().encode('ascii', 'ignore')

			# Get company SUB-INDUSTRY
			# subindustry = unicodedata.normalize('NFKD',profile.find('div',{'class':'exchange_type'}).findAll('span')[7].string).strip().encode('ascii', 'ignore')

			# Get company SUMMARY
			summary = unicodedata.normalize('NFKD',profile.find('p',{'id':'extended_profile'}).string).strip().encode('ascii', 'ignore')

			# Get company EXECUTIVE (TITLES, and NAMES)
			all_titles = [unicodedata.normalize('NFKD',i.string).strip().replace('&amp;','&').encode('ascii', 'ignore') for i in profile.find('table',{'class':'executives_two_cols'}).findAll('span',{'class':'title'})]
			all_names = [unicodedata.normalize('NFKD',i.string).strip().replace('&quot;','"').encode('ascii', 'ignore') for i in profile.find('table',{'class':'executives_two_cols'}).findAll('span',{'class':'name'})]

			# Append collected data
			pageCollector = [ticker,name,exchange,website,industry,sector,summary]
			pageExecCollector = [ticker,name,exchange,zip(all_titles,all_names)]

			myCSVwriter(CSVNAME,pageCollector,0)
			myCSVwriter(EXECSCSVNAME,pageExecCollector[0:3] + [elt for tup in pageExecCollector[3] for elt in tup],0)


			print '\t'.join((ticker,exchange,name))

		except:
			pass

	return True

def myCSVwriter(filname,row,flag):
	# We call this writer when creating a new file
	# Most likely, you'll be writing the header file with flag=1
	if flag == 1:
		with open(filname, 'wb') as csvfhandler:
			csv.register_dialect('excel', delimiter=',', skipinitialspace=True)
			writer = csv.writer(csvfhandler, dialect='excel')
			writer.writerow(row)

	# We call this writer when appending to existing file
	if flag == 0:
		with open(filname, 'ab') as csvfhandler:
			csv.register_dialect('excel', delimiter=',', skipinitialspace=True)
			writer = csv.writer(csvfhandler, dialect='excel')
			writer.writerow(row)

if __name__ == '__main__':
	main()
