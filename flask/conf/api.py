from oslo_config import cfg

api_service_opts = [
    cfg.PortOpt('port',
                default=6868,
                help='The port for the bmc API server.'),
    cfg.IPOpt('host_ip',
              default='0.0.0.0',
              help='The listen IP for the bmc API server.'),
    cfg.BoolOpt('enable_ssl_api',
                default=False,
                help=("Enable the integrated stand-alone API to service "
                       "requests via HTTPS instead of HTTP. If there is a "
                       "front-end service performing HTTPS offloading from "
                       "the service, this option should be False; note, you "
                       "will want to change public API endpoint to represent "
                       "SSL termination URL with 'public_endpoint' option.")),
    cfg.IntOpt('workers',
               help="Number of workers for bmc-api service. "
                      "The default will be the number of CPUs available."),
    cfg.IntOpt('max_limit',
               default=1000,
               help='The maximum number of items returned in a single '
                    'response from a collection resource.'),
]

api_group = cfg.OptGroup(name='api',
                         title='Options for the bmc-api service')


ALL_OPTS = (api_service_opts)


def register_opts(conf):
    conf.register_group(api_group)
    conf.register_opts(ALL_OPTS, api_group)


def list_opts():
    return {
        api_group: ALL_OPTS
    }
