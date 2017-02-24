# -*- coding: utf-8 -*-

__author__ = 'hubian'


class SERVER_STATUS:
    OK = 'ok'
    DEPLOYING = 'deploying'
    SUCCESS = 'success'
    FAILED = 'failed'
    WARNING = 'warning'
    ERROR = 'error'
    UNKNOWN = 'unknown'


class SERVER_MONITOR_LEVEL:
    NORMAL = 'ok'
    WARNING = 'warning'
    UNKNOWN = 'unknown'


class SERVER_POWER:
    ON = 'on'
    POWERING_ON = 'powering on'
    OFF = 'off'
    POWERING_OFF = 'powering off'
    UNKNOWN = 'unknown'
    REBOOT = 'reboot'
    REBOOTING = 'rebooting'


class SERVER_DEPLOY_SERVICE:
    NOVA = 'openstack-nova'
    HORIZON = 'openstack-horizon'
    UBUNTU = 'ubuntu-server'


class IMM_STATUS:
    ONLINE = 'online'
    OFFLINE = 'offline'
    UNKNOWN = 'unknown'
