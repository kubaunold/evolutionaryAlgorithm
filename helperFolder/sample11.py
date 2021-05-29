import PySimpleGUI as sg

response_buttons = ['b1', 'b2', 'b3', 'b4', 'b5']
current_event=[]
layout = [[sg.Button('start', key='start')],
            [sg.Button('text5', key='b5')],
            [sg.Button('text4', key='b4')],
            [sg.Button('text3', key='b3')],
            [sg.Button('text2', key='b2')],
            [sg.Button('text1', key='b1')]]
window = sg.Window('GUI test').Layout(layout).Finalize()
for button_label in response_buttons:
    window.FindElement(button_label).Update(disabled=True)
window.Refresh()

while True:
    # Read the Window
    event, values = window.Read()
    if event is None:
        break
    # Take appropriate action based on button
    if event == 'start':
        window.FindElement('start').Update(disabled=True)
        for button_label in response_buttons:
            window.FindElement(button_label).Update(disabled=False)
        window.Refresh()
    if event in response_buttons:
        # collect and store response
        current_event = current_event + [event]
        # disable the buttons during sound presentation
        for button_label in response_buttons:
            window.FindElement(button_label).Update(disabled=True)
        window.Refresh()
        window.FindElement('start').Update(disabled=False)
window.Close()