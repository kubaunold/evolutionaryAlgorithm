# not working

import PySimpleGUI as sg

with sg.FlexForm('Wszystko razem - ABIX', auto_size_text=True, default_element_size=(40, 1)) as form:
    layout = [
        [sg.Text('Wszystkie grafiki w jednym miejscu!', size=(30, 1), font=("Helvetica", 25), text_color='blue')],
        [sg.Text('Jakiś tekst... a jesli chcesz, wprowadź swój...')],
        [sg.InputText()],
        [sg.Checkbox('Mój checkbox'), sg.Checkbox('Mój kolejny checkbox!', default=True)],
        [sg.Radio('Radio button! ', "RADIO1", default=True), sg.Radio('Inny button !', "RADIO1")],
        [sg.Multiline(default_text='To jest domyślny tekst, jeśli zdecydujesz się nie wpisywać niczego',
        scale=(2, 10))],
        [sg.InputCombo(['Combobox 1', 'Combobox 2'], size=(20, 3)),
        sg.Slider(range=(1, 100), orientation='h', size=(35, 20), default_value=85)],
        [sg.Listbox(values=['Listbox 1', 'Listbox 2', 'Listbox 3'], size=(30, 6)),
        sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=25),
        sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=75),
        sg.Slider(range=(1, 100), orientation='v', size=(10, 20), default_value=10)],
        [sg.Text('_' * 100, size=(70, 1))],
        [sg.Text('Wybierz katalogi: źródłowy i docelowy', size=(35, 1))],
        [sg.Text('Wybierz katalog', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Źródło'),
        sg.FolderBrowse()],
        [sg.Text('Docelowy katalog', size=(15, 1), auto_size_text=False, justification='right'), sg.InputText('Docelowo'),
        sg.FolderBrowse()],
        [sg.Submit(), sg.Cancel(), sg.SimpleButton('Dostosowany', button_color=('white', 'green'))]
    ]

    button, values = form.LayoutAndRead(layout)