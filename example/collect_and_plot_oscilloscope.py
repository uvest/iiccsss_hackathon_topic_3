# imports
import json

import requests
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# constants
# enter the devices' IP addresses as defined by phyphox here
DEVICE_IPS = [
    ## for example
    # "192.168.0.111",
    # "192.168.0.158",
]
PORT=8080
GET_PARAMS = "?subdata=full&subtime0=full&length"

# functions
def get_data(devices:list, port:int, params:str) -> tuple:

    ### Sensor specific
    # prepare lists for amplitude and time of data
    amps = []
    times = []
    ###
    for i in range(len(devices)):
        # GET data from each phone
        response = requests.get(f"http://{devices[i]}:{port}/get{params}")

        # parse response to dictionary
        response = json.loads(response.content)

        # access data
        data = response["buffer"]

        ### Sensor specific
        # extract amplitude and time from data
        _amp = data["subdata"]["buffer"]
        _time = data["subtime0"]["buffer"]
        amps.append(_amp)
        times.append(_time)
        ###
    return times, amps

# define update function
def update(frame):
    global lines
    global axs

    # updating the data
    times, amps = get_data(DEVICE_IPS, PORT, params=GET_PARAMS)

    # udpate the graph
    for i in range(len(DEVICE_IPS)):
        lines[i].set_xdata(times[i])
        lines[i].set_ydata(amps[i])

        # autoscale
        axs[i].relim()
        axs[i].autoscale_view() 


if __name__ == "__main__":
    # define plot outline
    max_plot_cols = 3
    _ncols = min(len(DEVICE_IPS), max_plot_cols)
    _nrows = int(len(DEVICE_IPS) / max_plot_cols + 1-1e-10)
    fig, axs = plt.subplots(_nrows, _ncols, figsize=(3*_ncols, 2*_nrows))

    # parse axs to a 1-dimensional list
    axs = axs.flatten() if len(DEVICE_IPS) > 1 else [axs]

    # initial data
    times, amps = get_data(DEVICE_IPS, PORT, params=GET_PARAMS)

    # initial plot
    lines = []
    for i in range(len(DEVICE_IPS)):
        line, = axs[i].plot(times[i], amps[i])
        lines.append(line)

    # create an animation
    anim = FuncAnimation(fig, update, frames = None)
    plt.show()
