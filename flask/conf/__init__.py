from oslo_config import cfg
from bmc.conf import api
from bmc.conf import zabbix
from bmc.conf import keystone
from bmc.conf import mysql
from bmc.conf import app

CONF = cfg.CONF

app.register_opts(CONF)
api.register_opts(CONF)
zabbix.register_opts(CONF)
keystone.register_opts(CONF)
mysql.register_opts(CONF)