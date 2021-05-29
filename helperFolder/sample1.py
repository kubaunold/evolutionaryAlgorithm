import PySimpleGUI as sg
import time
import os
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.ticker import NullFormatter  
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
sg.theme('Dark')

def PyplotSimple():
    import numpy as np
    import matplotlib.pyplot as plt
    t = np.arange(0., 5., 0.2)          

    plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')

    fig = plt.gcf()  # get the figure to show
    return fig

def PyplotSimple2():
    import numpy as np
    import matplotlib.pyplot as plt
    t = np.arange(0., 5., 0.2)        
    plt.plot(t, t, 'r--', t, t ** 2, 'b--', t, t ** 3, 'b--')

    fig = plt.gcf()  # get the figure to show
    return fig

def draw_plot():
    plt.plot([0.1, 0.2, 0.5, 0.7])
    fig = plt.gcf()  # get the figure to show
    return fig



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all')


layout= [
    [sg.Text('my GUI', size=(40,1),justification='c', font=("Arial 10"))],
    [sg.Text('Browse to file:'), sg.Input(size=(40,1), key='input'),sg.FileBrowse (key='filebrowse')],

    [sg.Button('Process' ,bind_return_key=True),
    sg.Radio('1',key= 'RADIO1',group_id='1', enable_events = True,default=False, size=(10,1)),
    sg.Radio('2', key= 'RADIO2',group_id='1',enable_events = True, default=False, size=(10,1)),
    sg.Radio('3', key='RADIO3',group_id='1',enable_events = True, default=False, size=(12,1))],

    [sg.Canvas(size=(200,200), background_color='white',key='-CANVAS-')],
    [sg.Exit()]] 


window = sg.Window('my gui', layout, grab_anywhere=False, finalize=True)
#window.Maximize()
figure_agg = None
# The GUI Event Loop

while True:
    event, values = window.read()
    #print(event, values)                  # helps greatly when debugging
    if event in (sg.WIN_CLOSED, 'Exit'):             # if user closed window or clicked Exit button
        break
          
    if figure_agg:
        delete_figure_agg(figure_agg)
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
    if event == 'Process':
        #my function here 
        #the output of this function will decide the inputs to the graph which is why i need to use radio buttons
        sg.popup('Complete - view graphs',button_color=('#ffffff','#797979'))
    
    if event ==  'RADIO1':
        fig= PyplotSimple()
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

    if event ==  'RADIO2':
        fig= PyplotSimple2()
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
        
    
    if event ==  'RADIO3':
        fig= draw_plot()
        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)
  
    
    elif event == 'Exit':
        break

window.close()