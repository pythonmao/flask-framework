from flask_restful import Resource, reqparse
from bmc.services import server_manager
import bmc.api.adapter as u

rest = u.Rest('server', __name__)

@rest.get('/server/list')
def server_list():
    parse = reqparse.RequestParser()
    parse.add_argument('status', type=str, location='args', required=False)
    parse.add_argument('power', type=str, location='args', required=False)
    args = parse.parse_args()
    return u.render(server_manager.get_server_list(args))


    # tags = u.get_request_args().getlist('tags')
    # name = u.get_request_args().get('name', None)
    # return u.render(images=[i.dict for i in api.get_images(name, tags)])