# -*- coding: utf-8 -*-

import json
from . import Base, db_adapter
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Text, TypeDecorator
from sqlalchemy.orm import relation, backref


def relationship(*arg, **kw):
    ret = relation(*arg, **kw)
    db_adapter.commit()
    return ret


def to_dic(inst, cls):
    # add your coversions for things like datetime's
    # and what-not that aren't serializable.
    convert = dict()
    # convert[TZDateTime] = date_serializer
    convert[DateTime] = str

    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type.__class__ in convert.keys() and v is not None:
            try:
                func = convert[c.type.__class__]
                d[c.name] = func(v)
            except:
                d[c.name] = "Error:  Failed to covert using ", str(convert[c.type.__class__])
        else:
            d[c.name] = v
    return d


def to_json(inst, cls):
    return json.dumps(to_dic(inst, cls))


class DBBase(Base):
    """
    DB model base class, providing basic functions
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        super(DBBase, self).__init__(**kwargs)

    def dic(self):
        return to_dic(self, self.__class__)

    def json(self):
        return to_json(self, self.__class__)

    def __repr__(self):
        return '%s: %s' % (self.__class__.__name__, self.json())


class Server(DBBase):
    __tablename__ = 'physical_server'

    id = Column(Integer, primary_key=True)
    imm_host_name = Column(String(50), unique=True, nullable=False)
    uuid = Column(String(255))
    ip_address = Column(String(255))
    mac_address = Column(String(255))
    cpu_cores = Column(Integer)
    cpu_frequency = Column(Float)
    mem_capacity = Column(Integer)
    deploy_service = Column(String(50))  # constance:SERVER_DEPLOY_SERVICE
    management_ip = Column(String(255))
    xclarity_id = Column(Integer, ForeignKey(Xclarity.id))
    location = Column(String(255))
    position_id = Column(String(255))
    description = Column(String(255))
    serial_number = Column(String(255))
    part_number = Column(String(255))
    manufacturer = Column(String(255))
    machine_type = Column(String(255))
    url = Column(String(255))
    model = Column(String(255))
    inidicator_led = Column(String(16))
    imm_ip = Column(String(16))
    status_power = Column(String(16))

