from exceptions import Exception
from oslo_log import log


LOG = log.getLogger(__name__)


class BmcException(Exception):
    message = "An unkonwn message exception occurred."

    def __init__(self, message=None, **kwargs):
        if not message:
            try:
                message = self.message % kwargs
            except Exception as e:
                # kwargs doesn't match a variable in the message
                # log the issue and the kwargs
                for name, value in kwargs.items():
                    LOG.error("%s: %s" % (name, value))

                message = self.message

        super(BmcException, self).__init__(message)

class NotFoundException(BmcException):
    message = "Object %(id)s is not found"

class ConfigInvalid(BmcException):
    message = "Invalid configuration file. %(error_msg)s"

class Forbidden(BmcException):
    message = "You are not authorized to complete this action"

class MalformedRequestBody(BmcException):
    message = "Malformed message body: %(reason)s"

class XClarityConnectionFailed(BmcException):
    message = "Connection to xhmc failed: %(explanation)s"

class XClarityInternalFault(BmcException):
    message = "Internal fault: %(explanation)s %(recovery)s"

class PowerOperationError(BmcException):
    message = "Set power state by Xclarity server error: %(explanation)s"

class MigrationParameterError(BmcException):
    message = "Input parameter error: %(explanation)s"

class MigrationTokenInvalidError(BmcException):
    message = "token invalid: %(explanation)s"

class MigrationFailed(BmcException):
    message = "Migrate failed: %(explanation)s"

class GetDeployStatusFailed(BmcException):
    message = "Get deploy status failed: %(explanation)s"

class ServerDeployFailed(BmcException):
    message = "Server deploy failed: %(explanation)s"

class DeployParameterError(BmcException):
    message = "Parameter Error: %(explanation)s"

class DeployNotReady(BmcException):
    message = "Server is not ready for deploy: %(explanation)s"

class MigrationNotReady(BmcException):
    message = "Server cann't be migrated, host_ip: %(explanation)s"
