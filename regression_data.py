import json
import pandas as pd
from pathlib import Path
import shutil
import os
import dominate
from datetime import datetime


def load_regression_store(filename = "./regression_data.dat"):
    '''Load output from pytest and return as pandas dataframe'''
    with open(filename, "r") as f:
        data = json.load(f)

    return pd.DataFrame(data)

def copy_regression_data(filename = "./regression_data.dat",
                         destination = "../regression_data/data/"):
    '''Loop over output from pytest and copy files to destination (usually repository for regression output'''
    df = load_regression_store()

    # copy over configuration file
    shutil.copy2(filename, destination)

    # copy over all requested output files
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

def compare_regression_data(path1 = "./", path2 = None, html_path="./html"):
    from dominate.tags import table, tr, th, td, title, h1, link, script

    df = load_regression_store(path1+"/regression_data.dat")


    Path(html_path).mkdir(parents=True, exist_ok=True)

    doc = dominate.document(title='Regression tests')

    columns_display = ['testname', 'testfile', 'testfiletype',
                       'testfilesize', 'testobject','testnprimary']

    with doc:
        with doc.head:
            link(rel="stylesheet", href="styles.css")
            script(src="script.js")

        # page title
        now = datetime.now()
        h1("Regression tests (" + now.strftime("%Y-%m-%d %H:%M:%S") +")" )

        # loop over regression data frame
        with table(border="1"):
            with tr():
                for h in columns_display:
                    th(h)
            for index, row in df.iterrows():
                # if optics file make pdf

                # if rebdsim file make pdf

                # make table row
                with tr():
                    for column, cell in zip(df.columns,row):
                        if column in columns_display:
                            td(str(cell))

    with open(html_path+"/regression_data.html", "w") as f:
        f.write(str(doc))