import PySimpleGUI as sg
import logging

# create logger
logger = logging.getLogger('chere')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

'''
    Example of wizard-like PySimpleGUI windows
'''

layout = [[sg.Text('Window 1'), ],
          [sg.Input('')],
          [sg.Text('', size=(20, 1), key='-OUTPUT-')],
          [sg.Button('Next >'), sg.Button('Exit')]]

window1 = sg.Window('Window 1', layout)

window3_active = window2_active = window4_active = False

while True:
    if not window2_active:
        event1, values1 = window1.read()
        if event1 is None or event1 == 'Exit':
            break
        window1['-OUTPUT-'].update(values1[0])

    if not window2_active and event1 == 'Next >':
        window2_active = True
        window1.hide()
        layout2 = [[sg.Text('Window 2')],
                   [sg.Button('< Prev'), sg.Button('Next >')]]

        window2 = sg.Window('Window 2', layout2)

    if window2_active:
        event2 = window2.read()[0]
        if event2 in (None, 'Exit', '< Prev'):
            window2_active = False
            window2.close()
            window1.un_hide()
        elif event2 == 'Next >':
            window3_active = True
            window2_active = False
            window2.hide()
            layout3 = [[sg.Text('Window 3')],
                       [sg.Button('< Prev'), sg.Button('Next >')]]
            window3 = sg.Window('Window 3', layout3)

    if window3_active:
        # TODO: Add complexity
        logger.info('ow3')
        event3, values3 = window3.read()
        logger.info(window3.read())
        if event3 == '< Prev':
            logger.info('ow3: prev')
            window3.close()
            window3_active = False
            window2_active = True
            window2.un_hide()
        elif event3 == 'Next >':
            logger.info('ow3: next')
            window4_active = True
            window3_active = False
            window3.hide()
            layout4 = [[sg.Text('Window 4')],
                       [sg.Button('< Prev'), sg.Button('Exit')]]
            window4 = sg.Window('Window 4', layout4)

    if window4_active:
        logger.info('ow4')
        event4, values4 = window4.read()
        logger.info(window4.read())
        if event4 == '< Prev':
            window4.close()
            window4_active = False
            window3_active = True
            window3.un_hide()
        elif event4 in (None, 'Exit'):
            break

window1.close()
