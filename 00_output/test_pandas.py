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

def test_run_bdsim_pybdsim() :
    import pybdsim
    pybdsim.Run.Bdsim("output.gmad", "runBdsimPybdsim", 10, 1)

def test_pybdsim_pandas() :
    import pybdsim

    pd = pybdsim.DataPandas.BDSIMOutput("runBdsimPybdsim.root")

    # root object
    root_beam = pd.root_file.GetBeam().beam
    pandas_beam = pd.get_beam()

    pybdsim_pandas_transfer_check(root_beam, pandas_beam)