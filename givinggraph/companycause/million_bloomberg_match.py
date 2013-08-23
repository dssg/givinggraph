#!/usr/bin/env python
#
# Description: This matches the companies on the
#	Bloomberg list and Million-dollar donor list.
# 	The maches are saved to $CSVNAME file.
#

import csv
import re

# Read in these CSV's
COMPANIES = 'bloomberg_companies_list.csv'
DONATIONS = 'million_dollar_list.csv'

# Write to file
CSVNAME = 'million_bloomberg_match.csv'


def main():
    with open(COMPANIES, "rb") as ifile:
        comp_reader = csv.reader(ifile)
        comp_reader.next()  # strip header
        companies_list = []
        for r in comp_reader:
            companies_list.append(r)

    with open(DONATIONS, "rb") as ifile:
        dona_reader = csv.reader(ifile)
        dona_reader.next()  # strip header
        donations_list = []
        for r in dona_reader:
            donations_list.append(r)

    # Initialize .csv file
    myCSVwriter(CSVNAME, ['Company ticker', 'Company name', 'Company industry', 'Company sector', 'Company summary', 'Donor ID', 'Donor name', 'Recipient', 'Recipient subsector'], 1)

    # Get list of company names (Ticker, stripped name, name, industry, sector, summary)
    companies = [(c[0], get_regexed_company_name(c[1].strip()).strip(), c[1], c[4], c[5], c[6]) for c in companies_list]
    # Get list of recipient names, Remove recipients that are academic institutions
    # (Donor ID, stripped name, name, recipient, recipient subsector)
    donations = [(d[0], get_regexed_donor_name(d[1].strip()).strip(), d[1], d[10], d[12]) for d in donations_list if not re.match(r'\b(University|College|School)\b', d[10])]

    for c in companies:
        for d in donations:
            # Condition 1: if the stripped company name is in the donor list
            cond1 = bool(re.match('\\b' + c[1].lower() + '\\b', d[1].lower()))
            # Condition 2: if the company name is larger than "3" characters
            cond2 = bool(len(c[1]) > 3)
            if cond1 & cond2:
                myCSVwriter(CSVNAME, [c[0], c[2], c[3], c[4], c[5], d[0], d[2], d[3], d[4]], 0)


def get_regexed_company_name(company_name):
    #  Strip from companies
    #  20549 Ltd
    #  11780 Inc
    #   8677 Co
    #   7739 Corp
    #   3880 PLC
    #   3764 Group
    #   3492 Holdings
    return re.sub(r'\b(Ltd|Inc|Co|Corp|PLC|Group|Holdings)\b', '', company_name)


def get_regexed_donor_name(donor_name):
    #  Strip from donors
    #  43920 Foundation
    #   3682 Trust(s)
    #   2848 Fund(s)
    return re.sub(r'\b(Foundation|Trust|Trusts|Fund|Funds)\b', '', donor_name)


def myCSVwriter(filname, row, flag):
    # We call this writer when creating a new file
    # Most likely, you'll be writing the header file with flag=1
    if flag == 1:
        with open(filname, 'wb') as csvfhandler:
            csv.register_dialect('excel', delimiter=', ', skipinitialspace=True)
            writer = csv.writer(csvfhandler, dialect='excel')
            writer.writerow(row)

    # We call this writer when appending to existing file
    if flag == 0:
        with open(filname, 'ab') as csvfhandler:
            csv.register_dialect('excel', delimiter=', ', skipinitialspace=True)
            writer = csv.writer(csvfhandler, dialect='excel')
            writer.writerow(row)


if __name__ == '__main__':
    main()
