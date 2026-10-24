from math import isqrt
from plotly.subplots import make_subplots

def two_factors(n):
    """Return (a, b) with a * b == n, a <= b, and a as large as possible."""
    if n < 1:
        raise ValueError("n must be a positive integer")
    for a in range(isqrt(n), 0, -1):
        if n % a == 0:
            return a, n // a

def figure(nrow, ncol, shared_xaxes = False, shared_yaxes = False) :
    fig = make_subplots(rows=nrow, cols=ncol, shared_xaxes = shared_xaxes, shared_yaxes = shared_yaxes)

    return fig