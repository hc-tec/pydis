
'''
telnet 127.0.0.1 8989
set name titto
get name
'''

import argparse
from IOLoop.Reactor import ReReactor
from Server import server


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", "-i", help="Server listening IP address [default: 127.0.01]", default="127.0.0.1")
    parser.add_argument("--port", "-p", help="Server listening port [default: 9527]", type=int, default=9527)
    parser.add_argument("--enauth", "-e", help="Enable auth password", action="store_true")
    parser.add_argument("--authpwd", "-a", help="Set server-end auth password", default=None)
    parser.add_argument("--timeout", "-t", help="Set timeout to check client connections", default=10)

    return parser.parse_args()


def main():
    reactor = ReReactor('127.0.0.1', 8989)
    server.set_loop(reactor)
    while True:
        reactor.poll()


main()
