#!/usr/bin/env python

import socket
import email.utils
import urllib
import fmDevice
import fmResponder
import fmPoller
import fmUtilities
import fmXml
import wemos_request


# This subclass does the bulk of the work to mimic a WeMo switch on the network.

class fauxmo(fmDevice.upnp_device):
    @staticmethod
    def make_uuid(name):
        return ''.join(["%x" % sum([ord(c) for c in name])] + ["%x" % ord(c) for c in "%sfauxmo!" % name])[:14]

    def __init__(self, name, listener, poller, ip_address, port, action_handler = None):
        self.serial = self.make_uuid(name)
        self.name = name
        self.ip_address = ip_address
        persistent_uuid = "Socket-1_0-" + self.serial
        other_headers = ['X-User-Agent: redsonic']
        fmDevice.upnp_device.__init__(self, listener, poller, port, "http://%(ip_address)s:%(port)s/setup.xml", "Unspecified, UPnP/1.0, Unspecified", persistent_uuid, other_headers=other_headers, ip_address=ip_address)
        if action_handler:
            self.action_handler = action_handler
        else:
            self.action_handler = self
        fmUtilities.dbg("FauxMo device '%s' ready on %s:%s" % (self.name, self.ip_address, self.port))

    def get_name(self):
        return self.name

    def handle_request(self, data, sender, socket):
        command = wemos_request.wemos_request.from_data(data)
        success = False
        if command.is_requesting_setup():
            fmUtilities.dbg("Responding to setup.xml for %s" % self.name)
            xml = fmXml.SETUP_XML % {'device_name' : self.name, 'device_serial' : self.serial}
            socket.send(self.get_response_message("200 OK", xml))
            return
        elif command.is_wemos_command():
            success = self.handle_wemos_command(command.get_action())
                
        if success:
            # The echo is happy with the 200 status code and doesn't
            # appear to care about the SOAP response body
            socket.send(self.get_response_message("200 OKIE DOKIE", ""))
        else:
            fmUtilities.dbg(data)
            socket.send(self.get_response_message("404 NOT FOUND", ""))

    def get_response_message(self, status, body):
        date_str = email.utils.formatdate(timeval=None, localtime=False, usegmt=True)
        message = ("HTTP/1.1 %s\r\n"
                   "CONTENT-LENGTH: %d\r\n"
                   "CONTENT-TYPE: text/xml\r\n"
                   "DATE: %s\r\n"
                   "LAST-MODIFIED: %s\r\n"
                   "SERVER: Unspecified, UPnP/1.0, Unspecified\r\n"
                   "X-User-Agent: redsonic\r\n"
                   "CONNECTION: close\r\n"
                   "\r\n"
                   "%s" % (status, len(body), date_str, date_str, body))
        return message

    def handle_wemos_command(self, action):
        fmUtilities.dbg("Responding to %s for %s" % (action, self.name))
        if action == '1' or action == 1:
            return self.action_handler.on()
        elif action == '0' or action == 0:
            return self.action_handler.off()
        elif action == 'blue':
            return self.action_handler.on()
        else:
            return False

    def on(self):
        return False

    def off(self):
        return True
