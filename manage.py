
'''
telnet 127.0.0.1 9527
set name titto
get name
'''

import argparse
from IOLoop.Reactor import Reactor
from Server.server import server


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-i", help="Server listening host [default: 127.0.0.1]", default="127.0.0.1")
    parser.add_argument("--port", "-p", help="Server listening port [default: 9527]", type=int, default=9527)
    parser.add_argument("--sentinel", "-s", help="Sentinel mode on", type=bool, default=False)
    parser.add_argument("--authpwd", "-a", help="Set server-end auth password", default=None)
    parser.add_argument("--timeout", "-t", help="Set timeout to check client connections", default=10)

    return parser.parse_args()


def main():
    args = parse_args()
    reactor = Reactor(args.host, args.port)
    server.set_loop(reactor)
    if args.sentinel:
        server.on_sentinel_mode()
    server.set_addr(args.host, args.port)
    server.start_watchdog()
    while True:
        reactor.poll()


main()
