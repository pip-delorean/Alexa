#!/usr/bin/env python

import fmXml
from xml.dom import minidom

# try to import C parser then fallback in pure python parser.
try:
    from http_parser.parser import HttpParser
except ImportError:
    from http_parser.pyparser import HttpParser

# This class encapsulates a request received while polling and manages
# logic to determine if it is targeting a WeMo device.
class wemos_request(object):
    @staticmethod
    def from_data(data):
        p = HttpParser()
        recved = len(data)
        nparsed = p.execute(data, recved)
        name = ''
        action = -1
        if p.is_headers_complete():
            headers = p.get_headers()
            if 'Soapaction' in headers:
                name = headers['Soapaction']
            elif 'SOAPACTION' in headers:
                name = headers['SOAPACTION']

        if p.is_partial_body():
            xml = minidom.parseString(p.recv_body().lstrip())
            print(xml.toprettyxml())
            element = xml.getElementsByTagName('BinaryState')
            if element and len(element) >= 1:
                action = fmXml.getNodeText(element[0])

        print('action: ', action)
        command = wemos_request(name, action)
        command.method = p.get_method()
        command.status_code = p.get_status_code()
        command.path = p.get_path()

        return command

    def is_requesting_setup(self):
        return self.method == "GET" and self.path == "/setup.xml"

    def is_wemos_command(self):
        return self.name.find("urn:Belkin:service:basicevent:1#SetBinaryState")

    def get_action(self):
        return self.action

    def log_values(self):
        print 'Name: ', self.name
        print 'Action: ', self.action
        print 'Method: ', self.method
        print 'Status: ', self.status_code
        print 'Path: ', self.path

    def __init__(self, name, action):
        self.name = name
        self.action = action
