import os
from pathlib import Path

def pybdsim_pandas_transfer_check(root_object, pandas_object) :
    import types
    import cppyy
    root_obj_attributes = dir(root_object)

    root_obj_attributes_set = set()
    root_obj_attributes_tocheck = []

    for att_key in root_obj_attributes :
        att = getattr(root_object, att_key)

        att_type = type(att)

        root_obj_attributes_set.add(str(att_type))

        if att_type == types.MethodWrapperType :
            pass
        elif att_type == types.MethodType :
            pass
        elif att_type == types.BuiltinFunctionType :
            pass
        elif att_type == dict :
            pass
        elif att_type == types.NoneType:
            pass
        elif att_type == bool :
            root_obj_attributes_tocheck.append(att_key)
        elif att_type == int :
            root_obj_attributes_tocheck.append(att_key)
        elif att_type == float :
            root_obj_attributes_tocheck.append(att_key)
        elif att_type == cppyy.gbl.std.string :
            root_obj_attributes_tocheck.append(att_key)
        else :
            try :
                if type(att_type.__cpp_name__) == str:
                    if att_type.__cpp_name__.startswith("std::vector") :
                        root_obj_attributes_tocheck.append(att_key)
            except AttributeError:
                pass

    # loop over root object keys
    for att_key in root_obj_attributes_tocheck :
        try :
            pandas_object[att_key]
        except :
            print("Not found", att_key)

def test_import_pybdsim(testdata_store) :
    import pybdsim

    # log test run
    te = testdata_store.new_test_entry("01_output/import_pybdsim", __file__, 0, 0)

def test_import_pandas(testdata_store) :
    import pandas

    # log test run
    te = testdata_store.new_test_entry("01_output/import_pandas", __file__, 0, 0)

def test_output_pandas_file_not_found(testdata_store) :
    import pybdsim

    try :
        pd = pybdsim.DataPandas.BDSIMOutput("boom")
    except FileNotFoundError:
        pass

    # log test run
    te = testdata_store.new_test_entry("01_output/import_pandas_file_not_found", __file__, 0, 0)

def test_output_pandas_basic(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output.gmad", "output-basic-1", ngenerate=10, seed=1)
    pybdsim.Run.Bdsim("output.gmad", "output-basic-2", ngenerate=10, seed=1)
    pybdsim.Run.Bdsim("output.gmad", "output-basic-3", ngenerate=10, seed=1)

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-*.root")

    # root object
    root_beam = pd.root_file.GetBeam().beam
    pandas_beam = pd.get_beam()

    # pybdsim_pandas_transfer_check(root_beam, pandas_beam)

    te = testdata_store.new_test_entry("01_output/output_pandas_basic", __file__,10, 0)

def test_output_pandas_header(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    b = pd.get_header()

    te = testdata_store.new_test_entry("01_output/output_pandas_header", __file__,0, 0)

def test_output_pandas_run(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    b = pd.get_run()

def test_output_pandas_beam(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    b = pd.get_beam()

    te = testdata_store.new_test_entry("01_output/output_pandas_beam", __file__,0, 0)


def test_output_pandas_options(testdata_store):
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    b = pd.get_options()

    te = testdata_store.new_test_entry("01_output/output_pandas_options", __file__,0, 0)


def test_output_pandas_events(testdata_store):
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    e = pd.get_events()

    te = testdata_store.new_test_entry("01_output/output_pandas_events", __file__,0, 0)


def test_output_pandas_primary(testdata_store):
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    p = pd.get_primary()

    te = testdata_store.new_test_entry("01_output/output_pandas_primary", __file__,0, 0)


def test_output_pandas_primary_global(testdata_store):
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    pg = pd.get_primary_global()

    te = testdata_store.new_test_entry("01_output/output_pandas_global", __file__,0, 0)


def test_output_pandas_sampler(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    snames = pd.get_sampler_names()
    s = pd.get_sampler(snames[0])

    te = testdata_store.new_test_entry("01_output/output_pandas_sampler", __file__,0, 0)


def test_output_pandas_sampler_placement(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output_sampler_placement.gmad", "output_sampler_placement", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_sampler_placement.root")

    te = testdata_store.new_test_entry("01_output/output_pandas_sampler_placement", __file__,0, 0)


def test_output_pandas_csampler(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output_csampler.gmad", "output_csampler", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_csampler.root")

    te = testdata_store.new_test_entry("01_output/output_pandas_csampler", __file__,0, 0)

    snames = pd.get_csampler_names()
    s = pd.get_csampler(snames[0])

def test_output_pandas_ssampler(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output_ssampler.gmad", "output_ssampler", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_ssampler.root")

    te = testdata_store.new_test_entry("01_output/output_pandas_ssampler", __file__,0, 0)

    snames = pd.get_ssampler_names()
    # TODO check get_ssampler is in gmad or pybdsim
    # s = pd.get_ssampler(snames[0])

def test_output_eloss(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output-basic-1.root")

    e = pd.get_eloss()

    te = testdata_store.new_test_entry("01_output/output_pandas_eloss", __file__,0, 0)


def test_output_trajectory(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output_trajectory.gmad", "output_trajectory", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_trajectory.root")

    ts = pd.get_trajectories(0)
    t  = pd.get_trajectory(0,0)

    te = testdata_store.new_test_entry("01_output/output_pandas_trajectory", __file__,0, 0)

def test_output_pandas_aperture(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output_aperture.gmad", "output_aperture", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_aperture.root")

    te = testdata_store.new_test_entry("01_output/output_pandas_aperture", __file__,0, 0)


def test_output_pandas_collimators(testdata_store) :
    os.chdir(Path(__file__).resolve().parent)

    import pybdsim

    pybdsim.Run.Bdsim("output_collimator.gmad", "output_collimator", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_collimator.root")

    cnames = pd.get_collimator_names()
    c = pd.get_collimator(cnames[0])

    te = testdata_store.new_test_entry("01_output/output_pandas_collimators", __file__,0, 0)

