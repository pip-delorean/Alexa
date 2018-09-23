#!/usr/bin/env python

from xml.dom import minidom

# This XML is the minimum needed to define one of our virtual switches
# to the Amazon Echo
SETUP_XML = """<?xml version="1.0"?>
<root>
  <device>
    <deviceType>urn:MakerMusings:device:controllee:1</deviceType>
    <friendlyName>%(device_name)s</friendlyName>
    <manufacturer>Belkin International Inc.</manufacturer>
    <modelName>Emulated Socket</modelName>
    <modelNumber>3.1415</modelNumber>
    <UDN>uuid:Socket-1_0-%(device_serial)s</UDN>
  </device>
</root>
"""

def getNodeText(node):
    """
    Return text contents of an XML node.
    """
    text = []
    for childNode in node.childNodes:
        if childNode.nodeType == node.TEXT_NODE:
            text.append(childNode.data)
    return(''.join(text))

def logNode(xml, name):
	element = xml.getElementsByTagName(name)
	if element and len(element) >= 1:
		print '\t%s: %s' % (name, getNodeText(element[0]))

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