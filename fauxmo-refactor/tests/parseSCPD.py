#!/usr/bin/env python
# https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/

import urllib2
import urlparse
from xml.dom import minidom

def XMLGetNodeText(node):
    """
    Return text contents of an XML node.
    """
    text = []
    for childNode in node.childNodes:
        if childNode.nodeType == node.TEXT_NODE:
            text.append(childNode.data)
    return(''.join(text))

def logNode(name):
	element = root_xml.getElementsByTagName(name)
	if element and len(element) >= 1:
		print '\t%s: %s' % (name, XMLGetNodeText(element[0]))

def logNodes(nodeArr):
	print 'Nodes: -----'
	for node in nodeArr:
		logNode(node)
	print '------------\n'

def logHeaders(dict):
	print 'Headers: ---'
	for key, value in dict.items():
		print '\t%s: %s' % (key, value)
	print '------------\n'

# location = 'http://192.168.0.1:40833/rootDesc.xml'
request = 'http://10.10.10.2:52581/setup.xml'

# Fetch SCPD
try:
    response = urllib2.urlopen(request)
    response_headers = response.info()
    root_xml = minidom.parseString(response.read())
    response.close()

    # This will just display all the dictionary key-value pairs.  Replace this
    # line with something useful.
    response_headers.dict

except urllib2.HTTPError, e:
    # Prints the HTTP Status code of the response but only if there was a 
    # problem.
    print ("Error code: %s" % e.code)

logHeaders(response_headers.dict)

expectedNodes = ['deviceType', 'friendlyName', 'manufacturer', 'modelName', 'modelNumber', 'UDN']
logNodes(expectedNodes)

# Construct BaseURL
# base_url_elem = root_xml.getElementsByTagName('URLBase')
# if base_url_elem:
#     base_url = XMLGetNodeText(base_url_elem[0]).rstrip('/')
# else:
#     url = urlparse.urlparse(location)
#     base_url = '%s://%s' % (url.scheme, url.netloc)

# # Output Service info
# for node in root_xml.getElementsByTagName('service'):
#     service_type = XMLGetNodeText(node.getElementsByTagName('serviceType')[0])
#     control_url = '%s%s' % (
#         base_url,
#         XMLGetNodeText(node.getElementsByTagName('controlURL')[0])
#     )
#     scpd_url = '%s%s' % (
#         base_url,
#         XMLGetNodeText(node.getElementsByTagName('SCPDURL')[0])
#     )
#     print '%s:\n  SCPD_URL: %s\n  CTRL_URL: %s\n' % (service_type,
#                                                      scpd_url,
#                                                      control_url)

