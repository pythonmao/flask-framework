# -*- coding: utf-8 -*-
from oslo_config import cfg

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PWD = 'root000'
MYSQL_DB = 'bmcp'
MYSQL_PORT = 3306

mysql_service_opts = [
    cfg.StrOpt('connection',
              default='mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB),
              help='Mysql connection url'),
]

mysql_group = cfg.OptGroup(name='mysql',
                         title='Options for the mysql service')


ALL_OPTS = (mysql_service_opts)


def register_opts(conf):
    conf.register_group(mysql_group)
    conf.register_opts(ALL_OPTS, mysql_group)


def list_opts():
    return {
        mysql_group: ALL_OPTS
    }