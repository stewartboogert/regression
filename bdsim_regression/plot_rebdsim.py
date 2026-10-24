import pybdsim
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from .plot_common import two_factors
from .plot_common import figure

def comparision_optics(optics_filename1, optics_filename2, show = False, file_name = "comparison_optics.html") :
    o1 = pybdsim.Data.Load(optics_filename1)
    o2 = pybdsim.Data.Load(optics_filename2)

    fig = figure(5,1, shared_xaxes = True)
    t1 = plot_optics(o1.optics.S(), np.sqrt(o1.optics.Beta_x()), 1/2.*o1.optics.Sigma_Beta_x()/o1.optics.Sigma_Beta_x(), name="file 1 : beta x", mode="markers")
    t2 = plot_optics(o2.optics.S(), np.sqrt(o2.optics.Beta_x()), 1/2.*o1.optics.Sigma_Beta_x()/o2.optics.Sigma_Beta_x(), name="file 2 : beta x", mode="lines")
    t3 = plot_optics(o1.optics.S(), np.sqrt(o1.optics.Beta_y()), 1/2.*o1.optics.Sigma_Beta_y()/o1.optics.Sigma_Beta_y(), name="file 1 : beta y", mode="markers")
    t4 = plot_optics(o2.optics.S(), np.sqrt(o2.optics.Beta_y()), 1/2.*o2.optics.Sigma_Beta_y()/o2.optics.Sigma_Beta_y(), name="file 2 : beta y", mode="lines")
    fig.add_trace(t1, row=1, col=1)
    fig.add_trace(t2, row=1, col=1)
    fig.add_trace(t3, row=1, col=1)
    fig.add_trace(t4, row=1, col=1)

    t1 = plot_optics(o1.optics.S(), o1.optics.Alpha_x(), o1.optics.Sigma_Alpha_x(), name="file 1 : alpha x", mode="markers")
    t2 = plot_optics(o2.optics.S(), o2.optics.Alpha_x(), o2.optics.Sigma_Alpha_y(), name="file 2 : alpha x", mode="lines")
    t3 = plot_optics(o1.optics.S(), o1.optics.Alpha_y(), o1.optics.Sigma_Alpha_x(), name="file 1 : alpha y", mode="markers")
    t4 = plot_optics(o2.optics.S(), o2.optics.Alpha_y(), o2.optics.Sigma_Alpha_y(), name="file 2 : alpha y", mode="lines")
    fig.add_trace(t1, row=2, col=1)
    fig.add_trace(t2, row=2, col=1)
    fig.add_trace(t3, row=2, col=1)
    fig.add_trace(t4, row=2, col=1)

    t1 = plot_optics(o1.optics.S(), o1.optics.Disp_x(), o1.optics.Sigma_Disp_x(), name="file 1 : disp x", mode="markers")
    t2 = plot_optics(o2.optics.S(), o2.optics.Disp_x(), o2.optics.Sigma_Disp_y(), name="file 2 : disp x", mode="lines")
    t3 = plot_optics(o1.optics.S(), o1.optics.Disp_y(), o1.optics.Sigma_Disp_x(), name="file 1 : disp y", mode="markers")
    t4 = plot_optics(o2.optics.S(), o2.optics.Disp_y(), o2.optics.Sigma_Disp_y(), name="file 2 : disp y", mode="lines")
    fig.add_trace(t1, row=3, col=1)
    fig.add_trace(t2, row=3, col=1)
    fig.add_trace(t3, row=3, col=1)
    fig.add_trace(t4, row=3, col=1)

    t1 = plot_optics(o1.optics.S(), o1.optics.Disp_xp(), o1.optics.Sigma_Disp_xp(), name="file 1 : disp xp", mode="markers")
    t2 = plot_optics(o2.optics.S(), o2.optics.Disp_xp(), o2.optics.Sigma_Disp_yp(), name="file 2 : disp xp", mode="lines")
    t3 = plot_optics(o1.optics.S(), o1.optics.Disp_yp(), o1.optics.Sigma_Disp_xp(), name="file 1 : disp yp", mode="markers")
    t4 = plot_optics(o2.optics.S(), o2.optics.Disp_yp(), o2.optics.Sigma_Disp_yp(), name="file 2 : disp yp", mode="lines")
    fig.add_trace(t1, row=4, col=1)
    fig.add_trace(t2, row=4, col=1)
    fig.add_trace(t3, row=4, col=1)
    fig.add_trace(t4, row=4, col=1)

    t1 = plot_optics(o1.optics.S(), o1.optics.Npart(), np.zeros(len(o1.optics.Npart())), name="file 1 : N", mode="markers")
    t2 = plot_optics(o2.optics.S(), o2.optics.Npart(), np.zeros(len(o1.optics.Npart())), name="file 2 : N", mode="lines")
    fig.add_trace(t1, row=5, col=1)
    fig.add_trace(t2, row=5, col=1)

    if show == True :
        fig.show()

    if file_name is not None  and file_name != "":
        fig.write_html(file_name, include_plotlyjs="cdn")
        
def plot_optics(S, val, val_error, name = "data", mode= "markers") :
    return go.Scatter(x=S,
                      y=val,
                      mode=mode,
                      name=name,
                      error_y=dict(type="data", array=val_error, visible=True))



