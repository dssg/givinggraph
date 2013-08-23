#!/usr/bin/env python
#
# Description: This scrapes company pages
#

import re
import csv
import nltk
import signal
import urllib2
from   collections   import defaultdict
from   BeautifulSoup import BeautifulSoup

# Read search queries
COMPANYNAMES = 'bloomberg_companies_list.csv' # From full Bloomberg finance list
CSVNAME	     = 'company_pages.csv'			  # Store company pages here

def main():

	comp_names = [(c[0],c[1]) for c in  myCSVreader(COMPANYNAMES)] # Get company info (ticker,name)
	d = defaultdict(list)
	for t,c in comp_names:
		d[c].append(t)	 # We will only query unique company names, so group tickers together
	comp_names = d.items() # Results in list of tuples [(name,[ticker1, ticker2]) ...]

	# Initialize collector for (ticker, name, and link_i, text_i, for i=1:6)
	myCSVwriter(CSVNAME,['TICKER','NAME']+[j for i in [('LINK '+str(i) , 'TEXT '+str(i)) for i in range(1,7)] for j in i],1)


	for c,t in comp_names:

		# Query company name with words to get list of search results
		cq = re.compile('[\W_]+').sub('', c) # Remove punctuation from company name for web query
		results1 = get_results(cq,"corporate giving")
		results2 = get_results(cq,"donates supports")

		LINKS  = [j for i in [(results1[i]['href'],results2[i]['href']) for i in range(min(len(results1),len(results2)))] for j in i]
		LINKSU = []
		for i in LINKS:
			if i not in LINKSU:
				LINKSU.append(i) # this gets unique links, preserving Yahoo ranking order

		# Collect text data for these links until we have 6 websites in buffer
		collect_buffer = []
		counter		   = 0
		while (len(collect_buffer) < min(6,len(LINKSU))) & (counter < len(LINKSU)):

			link = LINKSU[counter]
			text = get_text(link)
			if len(text) > 0:
				collect_buffer.append((link,text))

			counter = counter + 1

		# Write websites in buffer for compan "c"
		myCSVwriter(CSVNAME,[t,c]+[j for i in collect_buffer for j in i],0)

		print '\t'.join((c,str(t)))


# Grab list of search results from Yahoo
def get_results(company,keyword):
	try:
		query   = company + ' ' + keyword
		url     = 'http://search.yahoo.com/search?p=' + query.replace(' ','+') # repalce space with +
		soup    = BeautifulSoup(urllib2.urlopen(url))
		results = soup.findAll('a',{'class':'yschttl spt'}) # results top 10 yahoo search results
	except:
		results = []
	return results


# Class to throw timeout exceptions
class TimeoutException(Exception): 
	pass 
 
def timeout(timeout_time, default):
	def timeout_function(f):
		def f2(*args):
			def timeout_handler(signum, frame):
				raise TimeoutException()
 
			old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
			signal.alarm(timeout_time) # triger alarm in timeout_time seconds
			try: 
				retval = f(*args)
			except TimeoutException:
				return default
			finally:
				signal.signal(signal.SIGALRM, old_handler) 
			signal.alarm(0)
			return retval
		return f2
	return timeout_function

@timeout(5, '')
def get_text(link):
	try:
		clean = nltk.clean_html(urllib2.urlopen(link).read())
		text  = ' '.join(clean.split())
	except:
		text  = ''
	return text


def myCSVreader(filename):
	# Read csv file to get data
	with open(filename, 'rb') as ifile:
		my_reader = csv.reader(ifile)
		my_reader.next() # strip header
		csv_data_list = []
		for lin in my_reader:
			csv_data_list.append(lin)
	return csv_data_list


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
