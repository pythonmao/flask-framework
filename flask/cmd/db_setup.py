# -*- coding: utf-8 -*-

from bmc.db import Base, engine


def setup_db():
    """Initialize db tables

    make sure db and user correctly created in mysql
    in case upgrade the table structure, the origin table need be dropped firstly
    """
    Base.metadata.create_all(bind=engine)

def main():
    print 'setup db started...'
    setup_db()
    print 'setup db ok...'