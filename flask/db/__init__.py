# -*- coding: utf-8 -*-

__author__ = 'hubian'

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bmc.db.db_adapters import SQLAlchemyAdapter
import bmc.conf

CONF = bmc.conf.CONF

# mysql_connection = 'mysql://bmcp:bmcp@localhost/bmcp'
mysql_connection = CONF.mysql.connection
engine = create_engine(mysql_connection,
                       convert_unicode=True,
                       pool_size=50,
                       max_overflow=100,
                       echo=False)

db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()
db_adapter = SQLAlchemyAdapter(db_session)

