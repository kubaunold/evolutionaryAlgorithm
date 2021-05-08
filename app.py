# app.py

import PySimpleGUI as sg
from sympy import symbols   # for symbolic math

# n <= 5
x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')


# first column of a layout
function_definition_column = [
    [
        sg.Text("f(xi)="), 
		sg.In(size=(25, 1), enable_events=True, key="-FUNCTION-")
    ],
    [
        sg.Text("Kostka"), sg.Text("Ograniczenia")
    ],
    [
        sg.Button("Generuj", key="-GENERATE-")
    ],
]

graph_viewer_column = [
	[sg.Text("Write a function and click generate:")],
	[sg.Image(key="-GRAPH-")]
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
        pass

    if event == "-GENERATE-":
        folder = values["-FUNCTION-"]
        print(eval(folder))



window.close()