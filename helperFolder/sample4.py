import PySimpleGUI as sg
import logging

log_file = 'run_log.txt'

# Logging setup to send one format of logs to a log file and one to stdout:
logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s, %(asctime)s, [%(levelname)s], %(message)s',
    filename=log_file,
    filemode='w')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(name)s, [%(levelname)s], %(message)s'))
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