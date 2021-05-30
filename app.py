# app.py
from tkinter import Frame
from tkinter.constants import DISABLED
from PySimpleGUI.PySimpleGUI import theme_text_element_background_color
from sympy import symbols   # for symbolic math
from sympy import Number, NumberSymbol, Symbol
import numpy as np
import math

import PySimpleGUI as sg
# import PySimpleGUIQt as sg

from matplotlib import use as use_agg
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

import logging

# GLOBAL VARIABLES
keyOfLoggerWindow = '-LOG-'
loggerFileName = "log.txt"

loe = '\u2264'  # Less or equal sign (<=)


def variablesInit():
    # n <= 5
    x1, x2, x3, x4, x5 = symbols('x1 x2 x3 x4 x5')

    return x1, x2, x3, x4, x5

### Some helper functions
def enableCubeRow(i, window):
    green_bg = '#68f26d'
    window.Element(f'tXNo{i}').Update(text_color='green')
    window.Element(f'iMin{i}').Update(disabled=False,background_color=green_bg)
    # window.Element(f'tCubeRng{i}').Update(disabled=False) ### text can't be disabled!
    window.Element(f'iMax{i}').Update(disabled=False,background_color=green_bg)
    # window.Element(f'tCubeRes{i}').Update(disabled=False)
    window.Element(f'sRes{i}').Update(disabled=False)
    window.Refresh()
    return


def disableCubeRow(i, window):
    red_bg='#d93838'    ### won't do - disabled don't have any color
    window.Element(f'iMin{i}').Update(background_color=red_bg)
    window.Element(f'tXNo{i}').Update(text_color='red')
    window.Element(f'iMin{i}').Update(disabled=True,background_color=red_bg)    # won't turn red :(
    window.Element(f'iMax{i}').Update(disabled=True,background_color=red_bg)
    window.Element(f'sRes{i}').Update(disabled=True)
    window.Refresh()
    return


def windowInit():

    sg.theme('LightBrown1')
    # sg.theme('HotDogStand')   # funny theme

    # Use Tkinter Agg
    use_agg('TkAgg')

    # Layout Definition
    # cube_layout =
    # allCubeRows = [[sg.Slider((1,10), key=f"slider_x{i}") for i in range(1,6)]]


    # first column of a layout
    function_definition_column = [
        [
            # FUNCTION
            sg.Frame(
                layout=[
                    [sg.T(
                        "Podaj wzór funkcji wykorzystując następujące zmienne w podanej kolejności:\nx1, x2, x3, x4, x5.")],
                    [
                        sg.Text("f(xi)="), sg.In(
                            size=(30, 1), key="-FUNCTION-"),
                        sg.Checkbox('Zatwierdź funkcję', size=(
                            15, 1), key='-CONFIRM_FUNCTION-', default=False, enable_events=True)
                    ],
                ],
                title='Funkcja',
                key='function_frame',
                relief=sg.RELIEF_GROOVE,  # GROOVE is normal, nice looking
            )

        ],
        [
            ### CUBE & RESTRICTIONS
            sg.Frame(
                layout=[
                    [
                        sg.Checkbox('Zatwierdź kostkę', size=(
                            15, 1), key='-CONFIRM_CUBE-', default=False, enable_events=True),
                    ],
                    *[[
                        sg.T(f'x{i}: ', key=f'tXNo{i}', font=('Arial', 10, 'bold')),
                        sg.Input(key=f'iMin{i}', size=(
                            5, 1), default_text="-10", tooltip=f'Minimalna wartość zmiennej x{i}'),
                        sg.T(f'{loe} x{i} {loe}', key=f'cubeTextRange_{i}'),
                        sg.Input(key=f'iMax{i}', size=(
                            5, 1), default_text="10", tooltip=f'Maksymalna wartość zmiennej x{i}'),
                        # sg.VSeperator(key=f'vSep_x{i}'),
                        sg.T(f'rozdzielczość x{i}:', key=f'tCubeRng{i}',
                             tooltip=f'Suwakiem ustal generowaną liczbę punktów dla zmiennej x{i}'),
                        sg.Slider(range=(10, 200), default_value=70, size=(18, 8), orientation='horizontal', font=(
                            'Helvetica', 10), tooltip=f'Suwakiem ustal generowaną liczbę punktów dla zmiennej x{i}', key=f'sRes{i}')
                        # sg.CB(f'Zatwierdź ograniczenie x{i}')
                    ] for i in range(1, 6)],

                ],
                title='Kostka',
                # tooltip = 'Użyj tego pola do ograniczenia zmiennych xi',
                # relief = sg.RELIEF_SUNKEN
            ),
            # sg.VSeperator(),
            sg.Frame(
                layout=[
                    [
                        sg.Checkbox('Zatwierdź ograniczenia', size=(
                            20, 1), key='-CONFIRM_RESTRICTIONS-', default=False, enable_events=True),
                    ],
                ],
                title='Ograniczenia',
                tooltip='Użyj tego pola do wprowadzenia ograniczeń',
                relief=sg.RELIEF_GROOVE
            ),

        ],
        # [sg.Button("Generuj", key="-GENERATE-", button_color=('white', 'green'))],
        [sg.Button("Generuj", key="-GENERATE-")],
        [sg.Button("GenerujMockData", key="-GENERATE_MOCK-")],
        [sg.Output(size=(100, 10), key=keyOfLoggerWindow)],
    ]

    # second column of layout
    graph_viewer_column = [
        [sg.T('Controls:')],
        [sg.Canvas(key='-FIGURE_CONTROLS-')],
        [sg.T('Figure:')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='-FIGURE-',
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

    # Window definition
    window = sg.Window(
        'Wizualizacja strategii ewolucyjnych',
        layout,
        # default_element_size=(30, 2),
        # font=('Helvetica', ' 10'),
        # default_button_element_size=(8, 2),
        finalize=True)

    # Hide some elements @ start
    # disable confirming Cube, Restrictions & Generate
    widgetsToDeactivateAtStart = [
        '-CONFIRM_CUBE-', '-CONFIRM_RESTRICTIONS-', '-GENERATE-']
    for widget_label in widgetsToDeactivateAtStart:
        window.FindElement(widget_label).Update(disabled=True)
    # disable rows of Cube
    for i in range(1, 6):    # 1, 2, 3, 4, 5
        disableCubeRow(i, window)

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

# Main Porogram that runs forever


def runProgram():
    # Variables initailization
    x1, x2, x3, x4, x5 = variablesInit()
    # Window initialization
    window = windowInit()

    # Logger initialization
    logger = loggerInit(window, keyOfLoggerWindow)
    # set up a figure twice as wide as it is tall
    # fig = plt.figure(figsize=plt.figaspect(0.5))

    fig = plt.figure()

    # ax = fig.add_subplot(2, 2, 1, projection='3d')

    while True:
        event, values = window.read(timeout=10)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        # onConfirmFunction enable confirming cube & restrictions
        if event == '-CONFIRM_FUNCTION-':
            if values['-CONFIRM_FUNCTION-'] == True:  # means if it has been checked
                try:    # parse function
                    folder = values["-FUNCTION-"]
                    f = eval(folder)
                    parsedString = str(f)
                except Exception:
                    # uncheck confirmFunction checkbox
                    window['-CONFIRM_FUNCTION-'].Update(value=False)
                    err = "Błąd podczas rozparsowywania funkcji. Zmień wzór i zatwierdź."
                    logger.error(err)
                    # sg.PopupAnnoying(err ,background_color='blue')
                    sg.popup(err, button_color=('#ffffff', '#797979'))
                else:  # if parsed properly
                    # leave checked True
                    # grey out function input
                    window.FindElement('-FUNCTION-').Update(disabled=True)
                    # enable some widgets
                    enableWidgetsOnFuntionConfirm = [
                        '-CONFIRM_CUBE-', '-CONFIRM_RESTRICTIONS-']
                    for w in enableWidgetsOnFuntionConfirm:
                        window.FindElement(w).Update(disabled=False)
                        
                    
                    # show info
                    logger.info(
                        f"Pomyślnie rozparsowano funkcję: f() = {parsedString}")

                    try:    # get and count variables
                        occuringVariables = f.atoms(Symbol)
                        strOccuringVariables = str(occuringVariables)
                        n = len(strOccuringVariables.split())
                    except Exception:
                        logger.info(
                            "Nie mogłem policzyć zmiennych w równaniu funkcji celu.")
                    else:
                        logger.info(
                            f"Występujące zmienne: {strOccuringVariables}. N={n}.")

                        # Zmienne muszą być podawane po kolei!
                        # Jeśli n=3, to występują x1, x2 i x3!
                        try:    ### enabling cubeRows
                            # now enable corresponding cube
                            for i in range(1, n+1):
                                enableCubeRow(i, window)
                            for i in range(n+1, 6):
                                disableCubeRow(i, window)
                        except Exception as e:
                            print(f"Podczas odblokowywania kostki: {e}")

            elif values['-CONFIRM_FUNCTION-'] == False:  # it was unchecked
                # unblock function to edit
                window.FindElement('-FUNCTION-').Update(disabled=False)
                # block Cube and Restruction checkboxes and uncheck them
                window.FindElement(
                    '-CONFIRM_CUBE-').Update(disabled=True, value=False)
                window.FindElement(
                    '-CONFIRM_RESTRICTIONS-').Update(disabled=True, value=False)

        if event == '-CONFIRM_CUBE-':
            if values['-CONFIRM_CUBE-'] == True:
                pass
            elif values['-CONFIRM_CUBE-'] == False:
                pass

        elif event == '-CONFIRM_RESTRICTIONS-':
            if values['-CONFIRM_RESTRICTIONS-'] == True:
                pass
            elif values['-CONFIRM_RESTRICTIONS-'] == False:
                pass

        # when all 3 are True => enable Generate key
        if values['-CONFIRM_FUNCTION-'] == values['-CONFIRM_CUBE-'] == values['-CONFIRM_RESTRICTIONS-'] == True:
            window.FindElement('-GENERATE-').Update(disabled=False)
        else:
            window.FindElement('-GENERATE-').Update(disabled=True)

        # Generate function
        if event == "-GENERATE-":
            folder = values["-FUNCTION-"]

            try:    # parse function
                f = eval(folder)
                parsedString = str(f)
            except Exception:
                logger.info(
                    "Błąd podczas rozparsowywania funkcji. Zmień wzór i kliknij 'Generuj'.")
            else:
                logger.info(
                    f"Pomyślnie rozparsowano funkcję: f() = {parsedString}")
                try:    # get and count variables
                    occuringVariables = f.atoms(Symbol)
                    strOccuringVariables = str(occuringVariables)
                    n = len(strOccuringVariables.split())
                except Exception:
                    logger.info(
                        "Nie mogłem policzyć zmiennych w równaniu funkcji celu.")
                else:
                    logger.info(
                        f"Występujące zmienne: {strOccuringVariables}. N={n}.")

                    # Zmienne muszą być podawane po kolei!
                    # Jeśli n=3, to występują x1, x2 i x3!
                    try:    # draw function
                        if n == 1:
                            logger.info(
                                "===ROZPOZNANO RÓWNANIE Z 1 ZMIENNĄ===")
                            logger.info("Tylko wykres 2D.")
                            fig.add_subplot(111)
                            fig = plt.gcf()  # clear figure
                            # ax = fig.add_subplot(1, 1, 1, projection='2d')
                            X = np.linspace(-5.0, 5.0, num=50)
                            Y = [f.subs(x1, x) for x in X]
                            plt.plot(X, Y)
                            plt.title(f'f(x1)={str(f)}')
                            plt.xlabel('x1')
                            plt.ylabel('f(x1)')
                            plt.grid()
                            draw_figure_w_toolbar(
                                window['-FIGURE-'].TKCanvas, fig, window['-FIGURE_CONTROLS-'].TKCanvas)
                            logger.info("Udało się narysować wykres.")

                        elif n == 2:
                            logger.info(
                                "===ROZPOZNANO RÓWNANIE Z 2 ZMIENNYMI===")
                            logger.info("Wykres 3D + warstwice.")

                        else:
                            logger.info(
                                "===ROZPOZNANO RÓWNANIE Z 3 LUB WIĘCEJ ZMIENNYMI===")
                            logger.info("Brak wykresu. Do nothing.")

                    except Exception:
                        logger.info("Błąd przy próbie narysowania funkcji.")

        if event == "-GENERATE_MOCK-":
            # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
            # plt.figure(1)
            # fig = plt.gcf()
            # DPI = fig.get_dpi()
            # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
            # sizeOfFigure = 600
            # fig.set_size_inches(sizeOfFigure/DPI, sizeOfFigure/DPI)
            # -------------------------------
            # x = np.linspace(0, 2 * np.pi)
            # y = np.sin(x)
            # plt.plot(x, y)
            # plt.title('y=sin(x)')
            # plt.xlabel('X')
            # plt.ylabel('Y')
            # plt.grid()

            # X = np.arange(-5, 5, 0.25)
            # Y = np.arange(-5, 5, 0.25)
            # X, Y = np.meshgrid(X, Y)
            # Z = np.sin(np.sqrt(X**2 + Y**2))
            # plt.plot(X, Y, Z)

            ax = fig.add_subplot(1, 1, 1, projection='3d')

            # plot a 3D surface like in the example mplot3d/surface3d_demo
            X = np.arange(-5, 5, 0.25)
            Y = np.arange(-5, 5, 0.25)
            X, Y = np.meshgrid(X, Y)
            Z = np.sin(np.sqrt(X**2 + Y**2))
            surf = ax.plot_surface(
                X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
            ax.set_zlim(-1.01, 1.01)
            fig.colorbar(surf, shrink=0.5, aspect=10)

            # ------------------------------- Instead of plt.show()
            draw_figure_w_toolbar(
                window['-FIGURE-'].TKCanvas, fig, window['-FIGURE_CONTROLS-'].TKCanvas)

    window.close()


if __name__ == "__main__":
    runProgram()
