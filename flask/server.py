# -*- coding: utf-8 -*-
import threading
from flask import Flask
from bmc.api import v1 as api_v1
import bmc.conf
from bmc.common import bmc_scheduler
from bmc.services.periodic import sync_servers_info, inventory_servers_resource

CONF = bmc.conf.CONF


def load_app():
    app = Flask(__name__)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'x-requested-with,Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'OPTIONS,GET,PUT,POST,DELETE')
        return response

    app.config['SECRET_KEY'] = CONF.app.secret_key
    app.config['debug'] = CONF.app.debug
    api_v1.register_blueprints(app, url_prefix='/api')
    start_periodic_tasks()
    return app

def start_periodic_tasks():
    def init_monitor_task():
        bmc_scheduler.add_interval(function=sync_servers_info, minutes=1, kwargs={'scheduler_obj': bmc_scheduler})
        bmc_scheduler.add_interval(function=inventory_servers_resource, minutes=5)

    threading.Thread(target=init_monitor_task).start()
