import configparser
import logging
import os
import subprocess
import tkinter as tk
from time import sleep

from db import actions


def get_pid_application():
	command = f"Get-Process {config['basic']['PROCESS']}"
	command_format = "Format-Table Id -HideTableHeaders -ErrorAction SilentlyContinue"

	p = subprocess.Popen(["powershell.exe", command, "|", command_format], stdout=subprocess.PIPE)
	application_pid = p.communicate()[0].strip().decode("utf-8")

	return application_pid


def measure_curr_application_time():
	command = f"New-TimeSpan -Start (get-process {config['basic']['PROCESS']}).StartTime"
	command_format = f"Format-Table Hours, Minutes -HideTableHeaders -ErrorAction SilentlyContinue"

	p = subprocess.Popen(["powershell.exe", command, "|", command_format], stdout=subprocess.PIPE)
	time = p.communicate()[0]
	try:
		hours, minutes = [int(item) for item in time.strip().split()]
	except ValueError:
		return 0

	return hours * 60 + minutes


def counter_label(root, label, i):
	if i > 0:
		i -= 1
		label.config(text=f"{config['basic']['PROCESS_NAME']} will close in {i} seconds")
		root.after(config['basic'].getint('MAX_OPERATION_TIME') * 100, lambda: counter_label(root, label, i))
	else:
		root.destroy()


def close_application(time):
	closing_message_start = f"Sorry, you've been using {config['basic']['PROCESS_NAME']} way too much...\n"
	closing_message_end = f"It's been {time}min, your limit is: {config['basic'].getint('MAX_OPERATION_TIME')}min!"
	closing_title = f"{config['basic']['PROCESS_NAME']} will close now."

	root = tk.Tk()
	root.attributes("-topmost", True)
	root.title(closing_title)
	label = tk.Label(root, fg="blue")
	label.pack()
	message = closing_message_start + closing_message_end
	message = tk.Message(root, text=message, width=300, padx=20, pady=15)
	message.pack()
	counter_label(root, label, config['basic'].getint('TIME_TO_DESTROY'))
	button = tk.Button(root, text='Close', width=25, command=root.destroy)
	button.pack()
	root.mainloop()
	os.system(f"taskkill /im {config['basic']['PROCESS']}.exe")


def check_max_time(time):
	if time > config['basic'].getint('MAX_OPERATION_TIME'):
		close_application(time)


def update_app_time():
	pid = get_pid_application()
	time = measure_curr_application_time()
	actions.update_entry(pid, time)


def check_app_status():
	command = f"get-process {config['basic']['PROCESS']} -ErrorAction SilentlyContinue"
	p = subprocess.Popen(["powershell.exe", command], stdout=subprocess.PIPE)
	output = p.communicate()[0]
	return output


def main():
	actions.connect_db()
	while True:
		try:
			is_running = check_app_status()
			if not is_running:
				logging.info(f"sleeping for {config['basic']['SLEEP_TIME']} seconds")
				sleep(config['basic'].getint('SLEEP_TIME'))
				continue
			update_app_time()
			total_time = actions.get_total_time()
			check_max_time(total_time)
			sleep(config['basic'].getint('SLEEP_TIME'))
		except Exception as e:
			print(e)


if __name__ == "__main__":
	config = configparser.ConfigParser()
	config.read('config.ini')
	message_format = '%(asctime)s %(levelname)s %(message)s'
	logging.basicConfig(filename=f"{config['basic']['PROCESS']}_log.log", level=logging.DEBUG, format=message_format)
	main()
