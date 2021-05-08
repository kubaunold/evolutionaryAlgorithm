# app.py

import PySimpleGUI as sg
from sympy import symbols   # for symbolic math
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt

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
	[sg.Canvas(key="-CANVAS-")],
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


matplotlib.use("TkAgg")
def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


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

        # fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        # t = np.arange(0, 3, .01)
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        def f(x, y):
            return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

        x_axis = np.linspace(0, 5, 50)
        y_axis = np.linspace(0, 5, 40)

        [X, Y] = np.meshgrid(x_axis, y_axis)

        fig, ax = plt.subplots(1,1)
        Z = f(X, Y)
        ax.contourf(X, Y, Z) 
        ax.set_title('Contour Plot') 
        ax.set_xlabel('x_axis') 
        ax.set_ylabel('y_axis')


        # Add the plot to the window
        draw_figure(window["-CANVAS-"].TKCanvas, fig)




window.close()