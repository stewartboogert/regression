# BDSIM regression testing

Physics verification of [BDSIM](https://bdsim-collaboration.github.io/web/). Requires

* [BDSIM](https://bdsim-collaboration.github.io/web/)
* [pybdsim](https://github.com/bdsim-collaboration/pybdsim)
* [bdsim-organisation/testdata](https://github.com/bdsim-collaboration/testdata)
* Python 3.9 or newer
* [pytest](https://pytest.org/)

## Install

From this directory, install the regression suite and its Python test dependency:

```sh
python -m pip install -e '.[test]'
```

The test suite also requires a configured BDSIM/Geant4 environment and the
external regression data described above. Install the optional `html` extra to
render regression-data reports with the `dominate` package.


To run

* ```cd regression```
* ```pytest```

The regression-data utility is available as `bdsim-regression-data` after
installation. For example, `bdsim-regression-data html --file
regression_data.dat` writes an HTML report beside the data file. The historical
`python regression_data.py ...` command remains available from the checkout.

To clean up files after run

* ```cd regression```
* ```make clean```
