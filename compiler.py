#!/usr/bin/env python
from compilationmetrics.collecting import collect
import sys
import sqlite3
import json
import socket
import random

ENDPOINTS_DB='endpoints.db' # TODO Absolute path.

def compactJson(obj):
    return json.dumps(obj, separators=(',',':'))

def handleMetrics(request):
    requestLine = 'push_no_ack {json}\n'.format(json=compactJson(request))
    # endpointsDb = sqlite3.connect(ENDPOINTS_DB)
    # endpoints = list(endpointsDb.execute('select Host, Port from Endpoints;'))
    endpoints = [(socket.gethostname(), 1337)]
    random.shuffle(endpoints)
    for address in endpoints:
        try:
            sock = socket.socket()
            sock.connect(address)
            sock.sendall(requestLine)
            sock.close()
            break # success
        except socket.error:
            continue # try again with next endpoint

sys.exit(collect.collect(sys.argv[1:], callback=handleMetrics, debug=False))
