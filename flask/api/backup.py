# -*- coding: utf-8 -*-

from bmc.server import api
from bmc.db import db_adapter
from bmc.db.models import Server, ServerMonitor
from flask_restful import Resource, reqparse
from flask import request
from time import strptime
from datetime import datetime
from bmc.services import server_manager
from bmc.drivers import xclarity_manager
from bmc.services import monitor_strategy_manager
from bmc.drivers.nova import nova_adapter
from bmc.services import subscription_manager


class TestResource(Resource):
    def get(self):
        return "server started"


class XclarityResource(Resource):
    def post(self):
        xclarity_info = request.get_json(force=True)
        xclarity_db = xclarity_manager.add_xclarity(xclarity_info)
        return {'data': xclarity_db.dic()}

    def put(self):
        xclarity_info = request.get_json(force=True)
        xclarity_db = xclarity_manager.update_xclarity(xclarity_info)
        return {'data': xclarity_db.dic()}

    def delete(self):
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, location='args', required=True)
        args = parse.parse_args()
        xclarity_manager.delete_xclarity(args['id'])


class XclarityListResource(Resource):
    def get(self):
        xclarity_list = map(lambda xclarity: xclarity.dic(),
                            xclarity_manager.get_xclarity_list())
        return {'data': xclarity_list}


class MonitorStrategyResource(Resource):
    def put(self, server_id):
        monitor_strategy_info = request.get_json(
            force=True)  # TODO id or server_id needed?
        strategy_db = monitor_strategy_manager.add_or_update_monitor_strategy(
            monitor_strategy_info, server_id)
        return {'data': strategy_db.dic()}

    def delete(self, server_id):
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, location='args', required=True)
        args = parse.parse_args()
        monitor_strategy_manager.delete_monitor_strategy(args['id'])


class ServerListResource(Resource):
    def get(self):
        # take filters into consideration
        parse = reqparse.RequestParser()
        parse.add_argument('status', type=str, location='args', required=False)
        parse.add_argument('power', type=str, location='args', required=False)
        args = parse.parse_args()
        return server_manager.get_server_list(args)


class ServerResource(Resource):
    def get(self):
        # get details info
        parse = reqparse.RequestParser()
        parse.add_argument('id', type=int, location='args', required=True)
        args = parse.parse_args()
        return server_manager.get_server_details(args['id'])


class ServerSummaryResource(Resource):
    def get(self):
        return server_manager.get_server_summary_resource()


class ServerMonitorResource(Resource):
    def get(self, server_id):
        # get the server's last monitor data record in db
        return {
            'data': monitor_strategy_manager.get_server_lastest_monitor_data(
                server_id)}


class ServerHistoryMonitorResource(Resource):
    def get(self, server_id, begintime):
        begintime = datetime(*strptime(begintime, "%Y-%m-%d %H:%M:%S")[0:6])
        history_monitor_list = db_adapter.find_all_objects(ServerMonitor,
                                                           ServerMonitor.server_id == server_id,
                                                           ServerMonitor.time >= begintime)

        return {
            'data': map(lambda monitor: monitor.dic(), history_monitor_list)}


class ServerPowerAction(Resource):
    def put(self, server_id):
        power_action_args = request.get_json(force=True)
        return server_manager.do_server_power_operation(server_id,
                                                        power_action_args)


class ServerMigrate(Resource):
    def post(self):
        args = request.get_json(force=True)
        nova_adapter.migrate_host_vms(args)
        return {'data': {'status': 'migrating'}}


class ServerMigrateStatus(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('token', type=str, location='args', required=True)
        parse.add_argument('server_id', type=int, location='args',
                           required=True)
        args = parse.parse_args()
        return nova_adapter.get_migration_status(args)


class ServerXclarityDeploy(Resource):
    def post(self):
        """
        Json example:
        {
            'serverId': 2，
            'imageName': 'esxi5.1-x86_64-install-Virtualization'，
            'credentials': {
                    'password': 'xxx'
                    'type': 'Linux/ESXI/WINDOWS'
            },
            'ipAssignment': 'dhcpv4'/'staticv4',
            'networkSettings':{
                     'ipAddress': "9.5.12.121",
                     'prefixLength': 64, #optional
                     'subnetMask': "255.255.255.0",
                     'gateway': "9.5.12.1",
                     'dns1': "9.10.244.100", #optional
                     'dns2': "9.10.244.200", #optional
                     'mtu': 1500, #optional  #optional
        }
        """
        deploy_info_args = request.get_json(force=True)
        return server_manager.do_server_deploy(deploy_info_args)


class XclarityImageSummary(Resource):
    def get(self, xclarity_id):
        """
        get all images of the xclarity
        """
        return server_manager.get_image_list(xclarity_id)


class ServerDeployStatus(Resource):
    def get(self, server_id):
        """
        get deploy status of a server TODO: jobid
        """
        return server_manager.get_deploy_status(server_id)


class ServerVMList(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('token', type=str, location='args', required=True)
        parse.add_argument('server_id', type=str, location='args',
                           required=True)
        args = parse.parse_args()
        return {'data': nova_adapter.get_vm_list(args)}


class ServersPowerAction(Resource):
    def put(self):
        """
        Json example:
        {
        'serverId':[id1,id2,id3],
        'action':'off'
        }
        """
        powers_action_args = request.get_json(force=True)
        return server_manager.do_servers_power_operation(powers_action_args)


class ServerHistoryEvent(Resource):
    def get(self, server_id, begintime):
        begintime = datetime(*strptime(begintime, "%Y-%m-%d %H:%M:%S")[0:6])
        return server_manager.get_server_history_events(server_id, begintime)


class ServerEvent(Resource):
    def get(self, server_id):
        return server_manager.get_server_events(server_id)


class ServerAvailable(Resource):
    def get(self, ):
        parse = reqparse.RequestParser()
        parse.add_argument('username', type=str, location='args',
                           required=True)
        args = parse.parse_args()
        # use request.args.get('username') later
        return subscription_manager.get_available_flavors(args)





def init_routes():
    api.add_resource(TestResource, "/api/test")

    api.add_resource(XclarityResource, "/api/xclarity")
    api.add_resource(XclarityListResource, "/api/xclarity/list")
    api.add_resource(XclarityImageSummary,
                     "/api/<int:xclarity_id>/image/summary")

    api.add_resource(MonitorStrategyResource,
                     "/api/server/<int:server_id>/monitorStrategy")

    api.add_resource(ServerListResource, "/api/server/list")
    api.add_resource(ServerSummaryResource, "/api/server/summary")
    api.add_resource(ServerResource, "/api/server")
    api.add_resource(ServerMonitorResource,
                     "/api/server/<int:server_id>/monitor")
    api.add_resource(ServerHistoryMonitorResource,
                     "/api/server/<int:server_id>/historyMonitor/<string:begintime>")

    api.add_resource(ServerPowerAction, "/api/server/<int:server_id>/power")
    api.add_resource(ServersPowerAction, "/api/servers/power")
    api.add_resource(ServerMigrate, "/api/server/migration")
    api.add_resource(ServerMigrateStatus, "/api/server/migration/status")
    api.add_resource(ServerXclarityDeploy, "/api/server/deploy")
    api.add_resource(ServerDeployStatus, "/api/<int:server_id>/deploy/status")
    api.add_resource(ServerVMList, "/api/server/vmlist")
    api.add_resource(ServerHistoryEvent,
                     "/api/server/<int:server_id>/historyEvent/<string:begintime>")
    api.add_resource(ServerEvent, "/api/server/<int:server_id>/event")

    api.add_resource(ServerAvailable, "/api/physical_server/available")
    api.add_resource(Subscription, "/api/subscription")
    api.add_resource(SubscriptionList, "/api/subscription/list")
    api.add_resource(SubscriptionApprovtion, "/api/subscription/approve")
