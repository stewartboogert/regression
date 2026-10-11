#!/usr/bin/env python3
"""Compatibility entry point for the regression-data tools."""

from bdsim_regression.regression_data import *  # noqa: F401,F403
from bdsim_regression.regression_data import main

if __name__ == "__main__":
    main()
