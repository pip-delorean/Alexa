#!/usr/bin/env python
# https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/

import urllib2

# Explanation for some of the soap xml body below
# 
# <s:Body>
# 	<u:SetBinaryState    						// this is a namespaced method name being requested
# 	xmlns:u="urn:Belkin:service:basicevent:1">  // this defines the service name which serves as the namespace
# 		<BinaryState>1</BinaryState>			// this defines a parameter passed in the request
# 	</u:SetBinaryState>							// closing tag for method
# </s:Body>										// closing tag for body

host = '10.0.0.11'
officePort = '52581'
kitchenPort = '52582'
twitterPort = '52583'

# spin our own soap request body
# s = SOAP-ENV
soap_body = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope 
 s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
 xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
	<s:Body>
		<u:SetBinaryState 
		 xmlns:u="urn:Belkin:service:basicevent:1">
			<BinaryState>1</BinaryState>
		</u:SetBinaryState>
	</s:Body>
</s:Envelope>
	"""

headers = {
	'Host': host,
	'Accept': '*/*',
	'Content-type': 'text/xml; charset="utf-8"',
	'SOAPACTION': '"urn:Belkin:service:basicevent:1#SetBinaryState"',
    'Content-Length': len(soap_body),
}

ctrl_url = "http://%s:%s/upnp/control/basicevent1" % (host, officePort)


# Fetch SCPD
try:
	request = urllib2.Request(ctrl_url, soap_body, headers)
	response = urllib2.urlopen(request)
	info = response.read()
	response.close()
	print '%s' % (info)

except urllib2.HTTPError, e:
    # Prints the HTTP Status code of the response but only if there was a 
    # problem.
    print ("Error code: %s" % e.code)





