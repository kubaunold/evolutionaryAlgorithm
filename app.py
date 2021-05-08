# app.py

import PySimpleGUI as sg




# first column of a layout
function_definition_column = [
    [
        sg.Text("f(xi)="), 
		sg.In(size=(25, 1), enable_events=True, key="-FUNCTION-"),
    ],
    [
        sg.Text("Kostka"), sg.Text("Ograniczenia"), 
    ],
]

graph_viewer_column = [
	[sg.Text("Write a function and click generate:")],
	[sg.Image(key="-GRAPH-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(function_definition_column),
        sg.VSeperator(),
        sg.Column(graph_viewer_column),
    ]
]

window = sg.Window("Evolutionary Strategy Application", layout)


# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes the window
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FUNCTION-":
        folder = values["-FUNCTION-"]
        print(folder)


window.close()