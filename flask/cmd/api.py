"""The bmc Service API."""

import sys

from bmc.common import service as bmc_service
import bmc.conf

CONF = bmc.conf.CONF


def main():
    # Parse config file and command line options, then start logging
    bmc_service.prepare_service(sys.argv)

    # Build and start the WSGI app
    launcher = bmc_service.process_launcher()
    server = bmc_service.WSGIService(
        'bmc-api',
        CONF.api.enable_ssl_api
    )
    launcher.launch_service(server, workers=server.workers)
    launcher.wait()

if __name__ == '__main__':
    sys.exit(main())