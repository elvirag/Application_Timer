from datetime import datetime, date

from sqlalchemy import func
from sqlalchemy.orm import sessionmaker

from db.models import connect_db, ApplicationProcesses


def connect():
	db = connect_db()  # establish connection
	Session = sessionmaker(bind=db)
	session = Session()

	return db, session


def insert_pid_time(pid, time):
	db, session = connect()
	try:
		session.add(ApplicationProcesses(pid=pid, last_update_time=datetime.now(), run_time=time))
		session.commit()
	except Exception as e:
		print(e)


def update_pid_time(pid, time):
	db, session = connect()
	try:
		process = session.query(ApplicationProcesses).get(pid)
		process.run_time = time
		process.last_update_time = datetime.now()
		session.commit()
	except Exception as e:
		print(e)


def is_pid(pid):
	db, session = connect()
	try:
		return session.query(ApplicationProcesses).get(pid)
	except Exception as e:
		print(e)

	return None


def update_entry(pid, time):
	if is_pid(pid):
		update_pid_time(pid, time)
	else:
		insert_pid_time(pid, time)


def get_total_time():
	db, session = connect()
	rows = session.query(ApplicationProcesses).filter(
		func.DATE(ApplicationProcesses.last_update_time) == date.today()).all()
	sum_total_time = 0
	for row in rows:
		sum_total_time += row.run_time

	return sum_total_time
