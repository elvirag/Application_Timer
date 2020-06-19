import configparser

from sqlalchemy import create_engine, Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ApplicationProcesses(Base):
	__tablename__ = 'application_processes'

	pid = Column(Integer, primary_key=True)
	last_update_time = Column('last_update_time', DateTime)
	run_time = Column(Integer)


def connect_db():
	config = configparser.ConfigParser()
	config.read('config.ini')
	engine = create_engine(f"sqlite:///{config['basic']['PROCESS_NAME']}.db", echo=True)
	Base.metadata.create_all(engine, checkfirst=True)

	return engine



