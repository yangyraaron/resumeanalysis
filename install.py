#-*- coding: UTF-8 -*-


import subprocess
import logging
import logging.config
import context

logging.config.dictConfig(context.logging)
logger = logging.getLogger('installer')


def main():
	if not checkPip():
		if not installPip():
			logger.error('the pip has not been installed correctly, please install it manually!')
			return

	logger.info('installing required packages')
	installPackages()
	

def checkPip():
	logger.info('checking if the pip has been installed')
	try:
		result = subprocess.check_output('command -v pip',shell=True)
	except subprocess.CalledProcessError:
		logger.error('the pip is not found',exc_info=True)
		return False

	return True

def installPip():
	logger.info('installing pip')
	try:
		subprocess.call('sudo apt-get install python-pip',shell=True)
	except Exception:
		logger.error('installing pip failed!',exc_info=True)
		return False
	else:
		logger.info('the pip has been installed')
		return True

def installPackages():
	try:
		command = 'sudo pip install -r {}/requirements.txt'.format(context.rootPath)
		subprocess.call(command,shell=True)
	except Exception:
		logger.error('install packages failed',exc_info=True)
	else:
		logger.info('packages have been installed!')
	


if __name__ == '__main__':
	main()