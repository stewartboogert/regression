import json
import pandas as pd
from pathlib import Path
import shutil

def load_regression_store(filename = "./regression_data.dat"):
    '''Load output from pytest and return as pandas dataframe'''
    with open(filename, "r") as f:
        data = json.load(f)

    return pd.DataFrame(data)

def copy_regression_data(filename = "/regression_data.dat",
                         destination = "../regression_data/"):
    '''Loop over output from pytest and copy files to destination (usually repository for regression output'''
    df = load_regression_store()

    icopied = 0
    for index, row in df.iterrows():
        testname = row['testname']
        testfile = row['testfile']
        testfiletype = row['testtfiletype']

        testdir = testname.split("/")[0]
        filepath = Path("./"+testdir+"/"+testfile)
        destpath = Path(destination+"/"+testdir+"/")
        destfilepath = destpath / Path(testfile)

        # create output directory if does not exist
        if not destpath.exists() :
            destpath.mkdir()

        # copy file
        shutil.copy2(filepath, destfilepath)

        icopied += 1

    print(f"Copied : {icopied} to {destination}")
