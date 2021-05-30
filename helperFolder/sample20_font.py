import PySimpleGUI as sg

layout = [[sg.Text('Date to Start Summing', key='-CALOUTPUT-', font=('Arial', 10, 'bold')), sg.Text(key='-CAL-', size=(10, None), font=('Arial', 10, 'bold'))],
          [sg.CalendarButton('Calendar', target='-CAL-', pad=None, font=('Arial', 10, 'bold'), format='%m/%d/%Y')],
          [sg.Text('Filename', key='-FOUTPUT-', font=('Arial', 10, 'bold'))],
          [sg.In( visible=False),
           sg.Input(key='-DIR-', size=(20, None), font=('Arial', 10, 'bold')), sg.FileBrowse('Browse', target='-DIR-', font=('Arial', 10, 'bold'))],
          [sg.OK(), sg.Cancel()]]


window = sg.Window('Data Collector', layout, grab_anywhere=False, size=(400, 280), return_keyboard_events=True,
                   finalize=True)

event, values = window.read()

while True:             # Event Loop
    event, values = window.Read()
    print(event, values, window.Size)
    if event is None or event == 'Exit':
        break