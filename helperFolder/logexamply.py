# logexample.py

import PySimpleGUI as sg
from external_file import p, test
import logging

sg.theme('DarkAmber')

layout = [
    [sg.Button("Show Log", key="-show_log-"),
     sg.Output(size=(50, 10), font='Courier 10', key='log')]
]

window = sg.Window('Logging tool', layout, finalize=True)

logger = p
formatter = logging.Formatter("%(levelname)s: %(message)s")

viewHandler = logging.StreamHandler(window["log"].TKOut)
viewHandler.setFormatter(formatter)
logger.addHandler(viewHandler)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "-show_log-":
        logger.info(__name__)
        test()
        logger.info(f"back here: {__name__}")

window.close()