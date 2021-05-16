import logging

loggerFileName  =   'log.txt'
keyOfLoggerWindow   =   '-LOG-'

class Handler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self)
    def emit(self, record):
        global buffer
        record = f'{record.name}, [{record.levelname}], {record.message}'
        buffer = f'{buffer}\n{record}'.strip()
        window[keyOfLoggerWindow].update(value=buffer)

log_file = loggerFileName

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s, %(asctime)s, [%(levelname)s], %(message)s',
    filename=log_file,
    filemode='w')

buffer = ''
ch = Handler()
ch.setLevel(logging.INFO)
logging.getLogger('').addHandler(ch)
