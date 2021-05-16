# sample3.py
# Shows logging into widget window in pysimplegui

import logging
import PySimpleGUI as sg
class Handler(logging.StreamHandler):

    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer
        record = f'{record.name}, [{record.levelname}], {record.message}'
        buffer = f'{buffer}\n{record}'.strip()
        window['log'].update(value=buffer)

log_file = 'run_log.txt'

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s, %(asctime)s, [%(levelname)s], %(message)s',
    filename=log_file,
    filemode='w')

buffer = ''
ch = Handler()
ch.setLevel(logging.INFO)
logging.getLogger('').addHandler(ch)

layout = [
    [sg.Text('Number:'), sg.Input(key='input')],
    [sg.Button('Run')],
    [sg.Output(size=(100,10), key='log')],
    [sg.Button('Exit')],
]

window = sg.Window('Window Title', layout)

while True:  # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Run':
        logging.info('Running...')

window.close()