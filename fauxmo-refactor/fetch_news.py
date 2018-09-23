#!/usr/bin/env python

import urllib2
import smtplib
import json
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# This is a sample script that can be called from a fauxmo file handler.
# When called this script will fetch trending topics on twitter as an
# html page and email them to your specified email address.

print("Lets fetch trending twitter topics...")

# fetch trending topics from twitter
url = 'https://twitter.com/hashtag/trendingnow?lang=en'

try:
	# set generic user agent to masquerade as a regular Firefox browser
	request_headers = {
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
	}

	# send the request with custom headers
	req = urllib2.Request(url, headers=request_headers)

	# read the response
	response = urllib2.urlopen(req)
	page = response.read()
	response.close()

	# get the directory this file is in
	fileDir = os.path.dirname(os.path.realpath('__file__'))

	# join the filename with the directory path for this file, but in the parent dir
	filename = os.path.join(fileDir, '../cred.json')

	# load credential file for our email user
	with open(filename) as f:
	    data = json.load(f)

	# load sender email & password from credential file
	# as well as recipient email
	fromaddr = data['sender']
	frompwd = data['credential']
	toaddr = data['recipient']

	# bail if any parameters are not set
	assert fromaddr and frompwd and toaddr
	
	# setup the email message to send for html type
	msg = MIMEMultipart('alternative')
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = "Trending on Twitter"
	msg.attach(MIMEText(page, 'html'))
	
	# send the email via smtp
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()    
	server.starttls()
	server.login(fromaddr, frompwd)
	server.sendmail(fromaddr, toaddr, msg.as_string())
	server.quit()

# Prints the error HTTP Status code for url errors
except urllib2.HTTPError, e:
    print "HTTPError Error code: %s" % e.code

# Print the error code for sending email if any are raised
except smtplib.SMTPRecipientsRefused, e:
	print "SMTPRecipientsRefused Error code: %s" % e.code
except smtplib.SMTPHeloError, e:
 	print "SMTPHeloError Error code: %s" % e.code
except smtplib.SMTPSenderRefused, e:
 	print "SMTPSenderRefused Error code: %s" % e.code
except smtplib.SMTPDataError, e:
 	print "SMTPDataError Error code: %s" % e.code
 


