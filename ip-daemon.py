#!/usr/bin/python3
#-*- coding=utf-8 -*-

import argparse
import logging
import socket
import re

from http.server import HTTPServer, BaseHTTPRequestHandler


logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")


class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        ip = self.headers["X-Real-IP"]
        log.info(self.headers)
        if ip == None:
            ip = self.client_address[0]
        m = re.search(r"::ffff:(\d+\.\d+\.\d+\.\d+)", ip)
        if m != None: ip = m.group(1)
        response = ip + "\n"
        self.wfile.write(response.encode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug",
                        action="store_true",
                        required=False)
    args = parser.parse_args()

    if args.debug:
        log.setLevel(logging.DEBUG)

    log.debug(args)

    log.info("start")

    httpd = HTTPServerV6(("::", 7777), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
