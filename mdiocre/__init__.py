import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# logging levels for presentation
#logging.addLevelName(logging.INFO, 'INFO')
for i in range(4):
	i += 1
	logging.addLevelName(logging.INFO+i, 'INFO:{}'.format(i))

logging.addLevelName(logging.INFO+5, 'OK')
for i in range(4):
	i += 1
	logging.addLevelName(logging.INFO+5+i, 'OK:{}'.format(i))
	
#logging.addLevelName(logging.WARNING, 'WARNING')
for i in range(4):
	i += 1
	logging.addLevelName(logging.WARNING+i, 'WARNING:{}'.format(i))

logging.addLevelName(logging.WARNING+5, 'SERIOUS')
for i in range(4):
	i += 1
	logging.addLevelName(logging.WARNING+5+i, 'SERIOUS:{}'.format(i))

#logging.addLevelName(logging.ERROR, 'ERROR')
for i in range(4):
	i += 1
	logging.addLevelName(logging.ERROR+i, 'ERROR:{}'.format(i))

# import mdiocre modules
from .core import MDiocre, VariableManager
from .wizard import Wizard
