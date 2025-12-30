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

def test_import_pybdsim() :
    import pybdsim

def test_import_pandas() :
    import pandas

def test_output_pandas_file_not_found() :
    import pybdsim

    try :
        pd = pybdsim.DataPandas.BDSIMOutput("boom")
    except FileNotFoundError:
        pass

def test_output_pandas_basic() :
    import pybdsim

    pybdsim.Run.Bdsim("output.gmad", "output", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    # root object
    root_beam = pd.root_file.GetBeam().beam
    pandas_beam = pd.get_beam()

    # pybdsim_pandas_transfer_check(root_beam, pandas_beam)

def test_output_pandas_header() :
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    b = pd.get_header()

def test_output_pandas_run() :
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    b = pd.get_run()

def test_output_pandas_beam() :
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    b = pd.get_beam()

def test_output_pandas_beam():
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    b = pd.get_options()

def test_output_pandas_events():
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    e = pd.get_events()

def test_output_pandas_primary():
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    p = pd.get_primary()

def test_output_pandas_primary_global():
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    pg = pd.get_primary_global()

def test_output_pandas_sampler() :
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    snames = pd.get_sampler_names()
    s = pd.get_sampler(snames[0])

def test_output_pandas_sampler_placement() :
    import pybdsim

    pybdsim.Run.Bdsim("output_sampler_placement.gmad", "output_sampler_placement", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_sampler_placement.root")

def test_output_pandas_csampler() :
    import pybdsim

    pybdsim.Run.Bdsim("output_csampler.gmad", "output_csampler", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_csampler.root")

    snames = pd.get_csampler_names()
    s = pd.get_csampler(snames[0])

def test_output_pandas_ssampler() :
    import pybdsim

    pybdsim.Run.Bdsim("output_ssampler.gmad", "output_ssampler", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_ssampler.root")

    snames = pd.get_ssampler_names()
    # s = pd.get_ssampler(snames[0])

def test_output_eloss() :
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("output.root")

    e = pd.get_eloss()

def test_output_trajectory() :
    import pybdsim

    pybdsim.Run.Bdsim("output_trajectory.gmad", "output_trajectory", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_trajectory.root")

    ts = pd.get_trajectories(0)
    t  = pd.get_trajectory(0,0)

def test_output_pandas_aperture() :
    import pybdsim

    pybdsim.Run.Bdsim("output_aperture.gmad", "output_aperture", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_aperture.root")

def test_output_pandas_collimators() :
    import pybdsim

    pybdsim.Run.Bdsim("output_collimator.gmad", "output_collimator", 10, 1)

    pd = pybdsim.DataPandas.BDSIMOutput("output_collimator.root")

    cnames = pd.get_collimator_names()
    c = pd.get_collimator(cnames[0])