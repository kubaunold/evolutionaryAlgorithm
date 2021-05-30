import PySimpleGUI as sg

layout = [
    [
        sg.Button('Hide'),
        sg.VSeperator(pad=(0,0), color=sg.DEFAULT_BACKGROUND_COLOR, key='V_SEP'),
        sg.Button('Unhide'),
    ]
]
window = sg.Window("Title", layout, finalize=True)
v_sep =  window['V_SEP']
pack_info = None
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Hide':
        if pack_info is None:
            pack_info = v_sep.Widget.pack_info()
            print(f'pack_info: {pack_info}')
            pack_info['before'] = window['Unhide'].Widget
            print(f"pack_info['before']: {pack_info['before']}")
            v_sep.Widget.pack_forget()
    elif event == 'Unhide':
        if pack_info:
            v_sep.Widget.pack(**pack_info)
            pack_info = None
window.close()



# import PySimpleGUI as sg

# def vsep():
#     return sg.Text("")

# layout = [ [sg.Text("Left"), sg.Text("Middle"), sg.Text("Right")],
#            [sg.Text("Left"), sg.VSeperator(), sg.Text("Middle"), sg.VSeparator(), sg.Text("Right")],
#            [sg.Text("Left"), sg.Text(""), sg.Text("Middle"), sg.Text(""), sg.Text("Right")],
#            [sg.Text("Left"), vsep(), sg.Text("Middle"), vsep(), sg.Text("Right")] ]

# window = sg.Window("Vertical test", layout)

# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED:
#         break

# window.close()