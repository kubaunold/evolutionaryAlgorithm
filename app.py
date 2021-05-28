# app.py
from sympy import symbols   # for symbolic math

import math

from matplotlib import use as use_agg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import numpy as np

import PySimpleGUI as sg

from sympy import symbols   # for symbolic math

import logging

### GLOBAL VARIABLES
keyOfLoggerWindow = '-LOG-'
loggerFileName = "log.txt"

def variablesInit():
    # n <= 5
    x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

    return x1, x2, x3, x4, x5


def windowInit():
    sg.theme('LightBrown1')
    # sg.theme('HotDogStand')   # funny theme

    # Use Tkinter Agg
    use_agg('TkAgg')

    ### Layout Definition
    # first column of a layout
    function_definition_column = [
        [sg.Text("f(xi)="), sg.In(size=(25, 1), enable_events=True, key="-FUNCTION-")],
        [sg.Text("Kostka"), sg.Text("Ograniczenia")],
        [sg.Button("Generuj", key="-GENERATE-")],
        [sg.Button("GenerujMockData", key="-GENERATE_MOCK-")],
        [sg.Output(size=(100,10), key=keyOfLoggerWindow)],
    ]

    # second column of layout
    graph_viewer_column = [
        [sg.T('Controls:')],
        [sg.Canvas(key='controls_cv')],
        [sg.T('Figure:')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='fig_cv',
                        # it's important that you set this size
                        size=(400 * 2, 400)
                        )]
            ],
            background_color='#DAE0E6',
            pad=(0, 0)
        )],
    ]

    # Full layout
    layout = [[
            sg.Column(function_definition_column),
            sg.VSeperator(),
            sg.Column(graph_viewer_column),
            ]]

    ### Window definition
    window = sg.Window(
        'Wizualizacja strategii ewolucyjnych',
        layout,
        # default_element_size=(30, 2),
        # font=('Helvetica', ' 10'),
        # default_button_element_size=(8, 2),
        finalize=True)
    return window

def loggerInit(window, keyOfLoggerWindow):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    viewHandler = logging.StreamHandler(window[keyOfLoggerWindow].TKOut)
    viewHandler.setFormatter(formatter)
    logger.addHandler(viewHandler)
    return logger


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)


class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

### Main Porogram that runs forever
def runProgram():
    ### Variables initailization
    x1, x2, x3, x4, x5 = variablesInit()
    ### Window initialization
    window = windowInit()
    ### Logger initialization
    logger = loggerInit(window, keyOfLoggerWindow)
    # set up a figure twice as wide as it is tall
    fig = plt.figure(figsize=plt.figaspect(0.5))
    # ax = fig.add_subplot(2, 2, 1, projection='3d')

    while True:

        event, values = window.read(timeout=10)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        ### Generate function
        if event == "-GENERATE-":
            folder = values["-FUNCTION-"]
            
            try:
                parsedString = str(eval(folder))
            except:
                logger.info("Błąd podczas rozparsowywania funkcji. Zmień wzór i kliknij 'Generuj'.")
            else:   # this block will be executed if no there are no errors
                logger.info(f"Pomyślnie rozparsowano funkcję: f() = {parsedString}")
            
            try:
                 # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
                plt.figure(1)
                fig = plt.gcf()
                DPI = fig.get_dpi()
                # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
                sizeOfFigure = 600
                fig.set_size_inches(sizeOfFigure/DPI, sizeOfFigure/DPI)
                # -------------------------------
                x = np.linspace(0, 2 * np.pi)
                y = np.sin(x)
                plt.plot(x, y)
                plt.title('y=sin(x)')
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.grid()
                # ------------------------------- Instead of plt.show()
                draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
            except:
                logger.info("Błąd przy próbie narysowania funkcji.")

        if event == "-GENERATE_MOCK-":
            pass


    window.close()

if __name__ == "__main__":
    runProgram()