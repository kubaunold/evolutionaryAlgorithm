# won't work

import logging

import PySimpleGUI as sg

import crawler as crawler
import iocParser
import mispParser
import postProcessing

# MISP KEY
MISP_URL = ""
MISP_KEY = ""

# logging
print = lambda *args, **kwargs: window['log'].print(*args, **kwargs)


def generate(misp_url: str, misp_key: str, misp_cert: bool, numberOfArticlesPerBlog: int, features: int) -> None:
    [...]    


# GUI
sg.theme('DarkBlue3')  # Add some color to the window

# Very basic window.  Return values using auto numbered keys

layout = [
    [sg.Text('MISP infos')],
    [sg.Text('MISP URL', size=(15, 1)), sg.InputText(default_text=MISP_URL)],
    [sg.Text('MISP KEY', size=(15, 1)), sg.InputText(MISP_KEY)],
    [sg.Checkbox('Verify certificates?', default=False)],
    [sg.Text('Generator info')],
    [sg.Text('Number of articles per source'), sg.Spin([i for i in range(1, 1000)], initial_value=1)],
    [sg.Text('Number of min. features per post'), sg.Spin([i for i in range(1, 15)], initial_value=3)],
    [sg.Text('Log:')],
    [sg.Multiline(size=(100, 10), key='log')],
    [sg.Button('Run'), sg.Button('Exit')]
]

window = sg.Window('IOC Generator', layout)

# Event Loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Run':
        print('Running...')
        generate(values[0], values[1], values[2], values[3], values[4])
        print('Finished...')

window.close()