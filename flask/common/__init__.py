from bmc.common.utils import Utils
from bmc.common.http_adapter import HttpMethod
import bmc.conf

CONF = bmc.conf.CONF

utils = Utils()
http = HttpMethod()

from bmc.common.scheduler import Scheduler
bmc_scheduler = Scheduler(CONF.app.debug)