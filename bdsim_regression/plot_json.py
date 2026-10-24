import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from math import isqrt
from .plot_common import two_factors
from .plot_common import figure

def compare(json_file1, json_file2, show = False, file_name = "comparison_json.html"):
    json_dict1 = json.load(open(json_file1))
    json_dict2 = json.load(open(json_file2))

    hist_dict1 = json_dict1['histograms']
    hist_dict2 = json_dict2['histograms']

    if len(hist_dict1) != len(hist_dict2):
        print("Histogram length do not match")

    # all histograms
    hist_set = set()
    hist_set |= set(hist_dict1.keys())
    hist_set |= set(hist_dict2.keys())
    hist_set = list(hist_set)
    hist_set.sort()

    # number of columns and rows
    nrow, ncol = two_factors(len(hist_set))
    # print(nrow, ncol)

    # create figure
    fig = figure(nrow, ncol)

    # loop over histograms
    for ihist, hist in enumerate(hist_set):
        icol = ihist % ncol
        irow = int((ihist - icol)/nrow)
        # print(hist, icol, irow)

        icol = icol + 1
        irow = irow + 1

        h1 = None
        h2 = None
        if hist in hist_dict1 :
            h1 = hist_dict1[hist]
        if hist in hist_dict2 :
            h2 = hist_dict2[hist]

        if h1 != None :
            if h1['type'] == "histo1d" :
                t1 = hist1d(hist_dict1[hist], hist)
            elif h1['type'] == "bar1d" :
                t1 = bar1d(hist_dict1[hist], hist, x_as_string=True)
            fig.add_trace(t1, row=irow, col=icol)

        if h2 != None :
            if h2['type'] == "histo1d" :
                t2 = hist1d(hist_dict2[hist], hist)
            elif h2['type'] == "bar1d" :
                t2 = bar1d(hist_dict2[hist], hist, x_as_string=True)
            fig.add_trace(t2, row=irow, col=icol)

        if h1 != None :
            fig.update_xaxes(title_text=h1['xlabel'], row=irow, col=icol)
            if "yscale" in h1 :
                fig.update_yaxes(type=h1['yscale'], row=irow, col=icol)
        if h2 != None :
            fig.update_xaxes(title_text=h2['xlabel'], row=irow, col=icol)
            if "yscale" in h2 :
                fig.update_yaxes(type=h2['yscale'], row=irow, col=icol)

    fig.update_layout(template="plotly_white")
    if show :
        fig.show()

    if file_name is not None  and file_name != "":
        fig.write_html(file_name, include_plotlyjs="cdn")

def bar1d(histDict,
          name = "data",
          x_as_string = False) :

    x = np.array(histDict['xcentres'])
    y = np.array(histDict['contents'])

    if x_as_string :
        x = x.astype(str)

    return go.Bar(
        x=x,
        y=y,
        name=name
    )

def hist1d(histDict,
           name ="data",
           x_as_string = False):

    try :
        x = np.array(histDict['xedges'])
    except :
        x = np.array(histDict['xcentres'])

    if x_as_string :
        x = x.astype(str)

    y = np.append(histDict['contents'], histDict['contents'][-1])

    sca = go.Scatter(
        x=x,
        y=y,  # repeat last value so len(y) == len(edges)
        mode="lines",
        line_shape="hv",  # horizontal-then-vertical steps
        name=name,
    )

    return sca

def hist2d(histDict,
           name = "data") :
    xedges = np.array(histDict['xedges'])
    yedges = np.array(histDict['yedges'])
    contents = np.array(histDict['contents'])

    return go.Heatmap(x=0.5 * (xedges[:-1] + xedges[1:]),  # bin centres
                      y=0.5 * (yedges[:-1] + yedges[1:]),
                      z=contents.T,  # transpose: histogram2d is indexed [x, y], heatmap wants [y, x]
                      # colorscale="Viridis",
                      # name=name
    )

    return
