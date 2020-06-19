import subprocess

if __name__ == "__main__":
	subprocess.Popen("python app.py", creationflags=subprocess.DETACHED_PROCESS, close_fds=True)
