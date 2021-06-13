# app.py
from tkinter import Frame, font
from tkinter.constants import DISABLED
from PySimpleGUI.PySimpleGUI import T, theme_text_element_background_color
from sympy import *
# from sympy import symbols   # for symbolic math
# from sympy import Number, NumberSymbol, Symbol
import numpy as np
# import math

import PySimpleGUI as sg
# import PySimpleGUIQt as sg

from matplotlib import use as use_agg
from matplotlib import cm
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

import logging

from functionClass import Function, x1, x2, x3, x4, x5
import draw3d as plot3d

from signal import signal, SIGINT
from sys import exit

import testFunctions as tf

import esPlus as ep


def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully')
    exit(0)

# GLOBAL VARIABLES
keyOfLoggerWindow = '-LOG-'
loggerFileName = "log.txt"

CHAR_LOE = '\u2264'     # Less or equal sign (<=)
CHAR_XVEC = '\u0078'    # x vector sign
CHAR_XVEC = '\u2179'    # x vector sign


# Some helper functions


def enableCubeRow(i, window):
    green_bg = '#68f26d'
    window.Element(f'tXNo{i}').Update(text_color='green')
    window.Element(f'iMin{i}').Update(
        disabled=False, background_color=green_bg)
    # window.Element(f'tCubeRng{i}').Update(disabled=False) ### text can't be disabled!
    window.Element(f'iMax{i}').Update(
        disabled=False, background_color=green_bg)
    # window.Element(f'tCubeRes{i}').Update(disabled=False)
    window.Element(f'sRes{i}').Update(disabled=False)
    window.Refresh()
    return


def disableCubeRow(i, window):
    red_bg = '#d93838'  # won't do - disabled don't have any color
    window.Element(f'iMin{i}').Update(background_color=red_bg)
    window.Element(f'tXNo{i}').Update(text_color='red')
    window.Element(f'iMin{i}').Update(
        disabled=True, background_color=red_bg)    # won't turn red :(
    window.Element(f'iMax{i}').Update(disabled=True, background_color=red_bg)
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
                        sg.Text(f"f({CHAR_XVEC})="),
                        sg.In(size=(30, 1), key="-FUNCTION-"),
                        sg.Checkbox('Zatwierdź funkcję', size=(
                            15, 1), key='-CONFIRM_FUNCTION-', default=False, enable_events=True),
                        sg.B("Test function", key="-TEST_FUNCTION-"),
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
                        sg.T(f'x{i}: ', key=f'tXNo{i}',
                             font=('Arial', 10, 'bold')),
                        sg.Input(key=f'iMin{i}', size=(
                            5, 1), default_text="-10", tooltip=f'Minimalna wartość zmiennej x{i}'),
                        sg.T(f'{CHAR_LOE} x{i} {CHAR_LOE}',
                             key=f'cubeTextRange_{i}'),
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

            sg.Frame(
                layout=[
                    [
                        sg.Checkbox('Zatwierdź ograniczenia', size=(
                            20, 1), key='-CONFIRM_RESTRICTIONS-', default=False, enable_events=True),
                    ],
                    *[[
                        sg.T(f'g{i}({CHAR_XVEC}): '),
                        sg.In(size=(25, 1), key=f"-REST{i}-"),
                        sg.T(f'{CHAR_LOE} 0'),
                        sg.Checkbox(
                            'Zatwierdź', key=f'-CONFIRM_REST{i}-', enable_events=True)
                    ] for i in range(1, 6)],
                ],
                title='Ograniczenia',
                tooltip='Użyj tego pola do wprowadzenia ograniczeń',
                relief=sg.RELIEF_GROOVE
            ),

            # sg.Frame(
            #     layout=[
            #         [
            #             sg.Checkbox('Zatwierdź ograniczenia', size=(
            #                 20, 1), key='-CONFIRM_RESTRICTIONS-', default=False, enable_events=True),
            #         ],
            #         [sg.Listbox(key='lbRest',values=[]),sg.T(f'{CHAR_LOE} 0')],
            #         [sg.In(key='-REST-', size=(30,40)),sg.T(f'{CHAR_LOE} 0')],
            #         [sg.B("Dodaj",key="-addRest-"), sg.B("Usuń",key="-rmRest-")]
            #     ],
            #     title='Ograniczenia',
            #     tooltip='Użyj tego pola do wprowadzenia ograniczeń',
            #     relief=sg.RELIEF_GROOVE
            # ),
        ],

        [sg.Button("Rysuj funkcję", key="-GENERATE-")],
        [sg.Button("GenerujMockData", key="-GENERATE_MOCK-")],
        [sg.Output(size=(120, 15), key=keyOfLoggerWindow)],

        [
            # SIMULATION
            sg.Frame(
                layout=[
                    [
                        sg.In(size=(8, 1),key="mu",default_text="20"),
                        sg.T('<- mu',tooltip='liczba rodziców'),
                    ],
                    [
                        sg.In(size=(8, 1),key="lambda",default_text="100"),
                        sg.T('<- lambda',tooltip='liczba potomstwa'),
                    ],
                    [
                        sg.In(size=(8, 1),key="sigma",default_text="0.15"),
                        sg.T('<- sigma',tooltip='parametr mutowalności'),
                    ],
                    [
                        sg.In(size=(8, 1),key="noEpoch",default_text="500"),
                        sg.T('<- N',tooltip='liczba epok'),
                    ],
                    [
                        sg.B("Rozpocznij symulację", key="-RUN_SIMULATION-"),
                    ],
                ],
                title='Symulacja',
                key='simulation_frame',
                relief=sg.RELIEF_GROOVE,  # GROOVE is normal, nice looking
            )
        ],
    ]

    # second column of layout
    graph_viewer_column = [
        [sg.T(f"f({CHAR_XVEC})="),sg.I("<Wykres funkcji zostanie umieszczony tutaj>",disabled=True,size=(80, 1),key="function_title")],
        [sg.T('Controls1:')],
        [sg.Canvas(key='-FIGURE_CONTROLS1-')],
        [sg.T('Figure1:')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='-FIGURE1-',
                           # it's important that you set this size
                           size=(600, 300)
                           )]
            ],
            background_color='#DAE0E6',
            pad=(0, 0)
        )],

        [sg.T('Controls2:')],
        [sg.Canvas(key='-FIGURE_CONTROLS2-')],
        [sg.T('Figure2:')],
        [sg.Column(
            layout=[
                [sg.Canvas(key='-FIGURE2-',
                           # it's important that you set this size
                           size=(600, 300)
                           )]
            ],
            background_color='#FFFFFF',
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
        finalize=True,
        # no_titlebar=True,
        location=(0, 0),
        # size=(1024, 1080),
        size=(1920, 1080),
        resizable=True,
        # keep_on_top=True,
    )

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
    signal(SIGINT, handler)

    # function object initialization
    fo = Function()

    # Window initialization
    window = windowInit()
    # start window maximized
    window.Maximize()

    # Logger initialization
    logger = loggerInit(window, keyOfLoggerWindow)
    # set up a figure twice as wide as it is tall
    # fig = plt.figure(figsize=plt.figaspect(0.5))

    fig = plt.figure()
    
    while True:
        event, values = window.read(timeout=10)

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        
        if event == '-TEST_FUNCTION-':
            try: window["-FUNCTION-"].update(value=tf.TestFunctions.ackley_function())
            except Exception as e:
                logger.error(f"Nie mogłem wczytać funkcji testowej.")
            else:
                logger.info("Pomyślnie wczytano funkcję testową") 


        # onConfirmFunction enable confirming cube & restrictions
        if event == '-CONFIRM_FUNCTION-':
            if values['-CONFIRM_FUNCTION-'] == True:  # means if it has been checked
                try:    # parse function
                    fo.parseFunction(values["-FUNCTION-"])
                except Exception as e:
                    # uncheck confirmFunction checkbox
                    window['-CONFIRM_FUNCTION-'].Update(value=False)
                    err = f"Błąd podczas rozparsowywania funkcji: {e}. Zmień wzór i zatwierdź."
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

                    window["function_title"].update(value=fo.funToString())

                    logger.info(
                        f"Pomyślnie rozparsowano funkcję: f({CHAR_XVEC}) = {fo.strFunction}")

                    try:    # get and count variables
                        fo.lOccVars = fo.function.atoms(Symbol)
                        fo.n = len(str(fo.lOccVars).split())
                    except Exception as e:
                        logger.info(
                            f"Nie mogłem policzyć zmiennych w równaniu funkcji celu: {e}.")
                    else:
                        logger.info(
                            f"Występujące zmienne: {str(fo.lOccVars)}. N={fo.n}.")

                        # Zmienne muszą być podawane po kolei!
                        # Jeśli n=3, to występują x1, x2 i x3!
                        try:  # enabling cubeRows
                            # now enable corresponding cube
                            for i in range(1, fo.n+1):
                                enableCubeRow(i, window)
                            for i in range(fo.n+1, 6):
                                disableCubeRow(i, window)
                        except Exception as e:
                            logger.error(f"Podczas odblokowywania kostki: {e}")

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
                try:
                    fo.vXMin[0] = eval(values['iMin1'])
                    fo.vXMin[1] = eval(values['iMin2'])
                    fo.vXMin[2] = eval(values['iMin3'])
                    fo.vXMin[3] = eval(values['iMin4'])
                    fo.vXMin[4] = eval(values['iMin5'])

                    fo.vXMax[0] = eval(values['iMax1'])
                    fo.vXMax[1] = eval(values['iMax2'])
                    fo.vXMax[2] = eval(values['iMax3'])
                    fo.vXMax[3] = eval(values['iMax4'])
                    fo.vXMax[4] = eval(values['iMax5'])

                    fo.vXRes[0] = int(values['sRes1'])
                    fo.vXRes[1] = int(values['sRes2'])
                    fo.vXRes[2] = int(values['sRes3'])
                    fo.vXRes[3] = int(values['sRes4'])
                    fo.vXRes[4] = int(values['sRes5'])

                except Exception as e:
                    logger.error(f"Podczas zatwierdzania kostki: {e}.")
                else:
                    logger.info(f"Pomyślnie zatwierdzono kostkę.")

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
            # Zmienne muszą być podawane po kolei!
            # Jeśli n=3, to występują x1, x2 i x3!
            try:    # draw function
                if fo.n == 1:
                    logger.info(
                        "===ROZPOZNANO RÓWNANIE Z 1 ZMIENNĄ===")
                    logger.info("Tylko wykres 2D.")
                    fig.add_subplot(111)
                    # plt.gcf()  # clear figure
                    plt.clf()   # clear figure
                    plt.cla()   # clear axes
                    draw_figure_w_toolbar(
                        window['-FIGURE1-'].TKCanvas, fig, window['-FIGURE_CONTROLS1-'].TKCanvas)
                    # ax = fig.add_subplot(1, 1, 1, projection='2d')

                    X, Y = fo.create2DAxes()

                    plt.plot(X, Y)
                    plt.title(f'f(x1)={fo.strFunction}')
                    plt.xlabel('x1')
                    plt.ylabel('f(x1)')
                    plt.grid()
                    draw_figure_w_toolbar(
                        window['-FIGURE1-'].TKCanvas, fig, window['-FIGURE_CONTROLS1-'].TKCanvas)
                    logger.info("Udało się narysować wykres.")


                        



                elif fo.n == 2:
                    logger.info(
                        "===ROZPOZNANO RÓWNANIE Z 2 ZMIENNYMI===")

                    try:  # wykres 3D
                        logger.info("Rysowanie wykresu 3D.")
                        fig = fo.make3dgraph()
                        draw_figure_w_toolbar(
                            window['-FIGURE1-'].TKCanvas, fig, window['-FIGURE_CONTROLS1-'].TKCanvas)
                    except Exception as e:
                        logger.error(f"Podczas rysowania wykresu 3D: {e}.")
                    else:
                        logger.info("Pomyślnie narysowano wykres 3D.")

                    try:  # wykres 2D - warstwice
                        logger.info("Rysowanie wykresu 2D - warstwice.")
                        fig = fo.make_2d_countour_lines()
                        draw_figure_w_toolbar(
                            window['-FIGURE2-'].TKCanvas, fig, window['-FIGURE_CONTROLS2-'].TKCanvas)
                    except Exception as e:
                        logger.error(f"Podczas rysowania wykresu 2D: {e}.")
                    else:
                        logger.info("Pomyślnie narysowano wykres 2D.")

                else:
                    logger.info(
                        "===ROZPOZNANO RÓWNANIE Z 3 LUB WIĘCEJ ZMIENNYMI===")
                    logger.info("Brak wykresu.")

            except Exception as e:
                logger.info(f"Błąd przy próbie narysowania funkcji: {e}.")


        if event == "-RUN_SIMULATION-":
            try: # get parameters
                lam = int(values['lambda'])
                mu = int(values['mu'])
                sig = float(values['sigma'])
                noEpochs = int(values['noEpoch'])
            except Exception as e:
                logger.error(f"Podczas pozyskiwania parametrów do symulacji: {e}.")
            else:
                try: # run evolution simulation
                    objective, bounds = fo.getSimulationObjectiveAndBounds()
                    n_iter = noEpochs
                    step_size = sig
                    
                    best, score = ep.es_plus(objective, bounds, n_iter, step_size, mu, lam)
                    print(f"Ewolucja zakończona")
                    print('f(%s) = %f' % (best, score))

                except Exception as e:
                    logger.error(f"Podczas przygotowywania parametrów do symulacji: {e}.")



        if event == "-GENERATE_MOCK-":
            try:
                def f(x, y):
                    return np.sin(np.sqrt(x ** 2 + y ** 2))
                x = np.linspace(-6, 6, 30)
                y = np.linspace(-6, 6, 30)
                X, Y = np.meshgrid(x, y)
                Z = f(X, Y)
                fig = plt.figure()
                ax = plt.axes(projection='3d')
                ax.contour3D(X, Y, Z, 50, cmap='binary')
                ax.set_xlabel('x')
                ax.set_ylabel('y')
                ax.set_zlabel('z')
                ax.view_init(60, 35)
                ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                                cmap='viridis', edgecolor='none')
                ax.set_title('surface')
                draw_figure_w_toolbar(
                    window['-FIGURE1-'].TKCanvas, fig, window['-FIGURE_CONTROLS1-'].TKCanvas)
            except Exception as e:
                logger.error(f"Nie mogłem narysować mock data: {e}.")
    window.close()


if __name__ == "__main__":
    runProgram()
