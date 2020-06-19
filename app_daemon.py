import logging


def main():
	pass


if __name__ == "__main__":
	# subprocess.Popen(executable, creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
	logging.basicConfig(filename='arena_log.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
	main()
