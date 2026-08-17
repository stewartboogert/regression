import os
import pytest

pytestmark = pytest.mark.xfail(reason="requires bdsim")

def bdsimParserSetup_fromFile() :
    import bdsim

    p = bdsim.BDSParser.Instance("./trackerInterface.gmad")
    o = p.GetOptions()
    o['batch'] = True
    o['outputFormat'] = 'none'


    b = bdsim.BDSIM(p)
    b.BeamOn(10)

    return 0

def bdsimParserSetup_fromEmpty():
    import bdsim

    p = bdsim.BDSParser()

    b = p.GetBeam()
    b['particle'] = 'e-'
    b['energy'] = 10.0
    b['distrType'] = 'reference'

    o = p.GetOptions()
    o['batch'] = True
    o['outputFormat'] = 'none'

    b = bdsim.BDSIM(p)
    #b.BeamOn(10)

    return 0

def bdsimParserAccessors() :
    import bdsim

    p = bdsim.BDSParser.Instance("./trackerInterface.gmad")
    p.GetApertures()
    p.GetAtoms()
    p.GetBeam()
    p.GetBeamline()
    p.GetBiasing()
    p.GetBiasingVector()
    p.GetBLMs()
    p.GetCavityModels()
    p.GetColours()
    p.GetCoolingChannels()
    p.GetCrystals()
    p.GetElement("d1")
    p.GetFields()
    p.GetOptions()
    p.GetOptionsBase()
    p.GetLasers()
    p.GetMaterials()
    p.GetModulators()
    p.GetPlacements()
    p.GetSamplerFilterIDToSet()
    p.GetScorers()
    p.GetScorerMeshes()
    p.GetSequence("l0")

    return 0

def bdsimParserAperture() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Aperture()
    a = bdsim.Aperture()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables
    a['apertureType'] = 'elliptical'
    a['aper1'] = 1.0
    a['aper2'] = 2.0
    a['aper3'] = 3.0
    a['aper4'] = 4.0

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    # add to parser
    p.Add_Aperture()

    ar = p.GetApertures()

    # print
    print(ar)

    return 0

def bdsimParserAtom():
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Atom()
    a = bdsim.Atom()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables
    a['A'] = 10.1
    a['Z'] = 11.2
    a['name'] = 'unobtanium'
    a['symbol'] = 'Ub'

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    # add to parser
    p.Add_Atom()

    ar = p.GetAtoms()

    # print
    print(ar)

    return 0

def bdsimParserBeam() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Beam()
    a = bdsim.Beam()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables
    a['distrFileFromExecOptions'] = True
    a['distrFileLoopNTimes'] = 10
    a['energy'] = 1.1234 # double
    a['particle'] = 'e-' # string

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetBeam()

    # print
    print(ar)

    return 0

def bdsimParserBeamline() :
    import bdsim
    import os

    p = bdsim.BDSParser()

    b = p.GetBeam()
    b['particle'] = 'e-'
    b['energy'] = 10.0
    b['distrType'] = 'reference'

    o = p.GetOptions()
    o['batch'] = True
    o['outputFormat'] = 'rootevent'
    o['outputFileName'] = "bdsimParserBeamline.root"

    e = p.GetGlobal_Parameters()

    e.flush()
    e.name = "d1"
    e.type = bdsim.elementtype.ElementType.DRIFT
    e['l'] = 1.0
    p.write_table("d1",bdsim.elementtype.ElementType.DRIFT,False)

    # drift 2
    e.flush()
    e.name = "d2"
    e.type = bdsim.elementtype.ElementType.DRIFT
    e['l'] = 2.0
    p.write_table("d2",bdsim.elementtype.ElementType.DRIFT,False) # TODO duplicate name

    # line 0
    e.flush()
    e.name = "l0"
    e.type = bdsim.elementtype.ElementType.LINE
    p.add_element_temp("d1",1,False,bdsim.elementtype.ElementType.DRIFT)
    p.add_element_temp("d2",1,False,bdsim.elementtype.ElementType.DRIFT)
    p.write_table("l0",bdsim.elementtype.ElementType.LINE,True)

    p.current_line = "l0"
    p.expand_line("l0","d1","")
    # p.expand_sequences()

    p.add_sampler("", -2, bdsim.ElementType.DRIFT, "plane", [])

    # print out beamlines
    print("Elements")
    p.PrintElements()
    print("Beamline")
    p.PrintBeamline()

    try:
        b = bdsim.BDSIM(p)
        b.BeamOn(10)
    except Exception as e  :
        print("BDSIM failed")
        print(e)

    if "PYTEST_CURRENT_TEST" in os.environ:
        return 0
    else :
        return p

def bdsimParserBLMPlacement() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_BLMPlacement()
    a = bdsim.BLMPlacement()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables

    a['name'] = "test_name" # string
    a['axisAngle'] = True # bool
    a['referenceElementNumber'] = 1
    a['x'] = 1.23456789 # double

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetBLMs()

    # print
    print(ar)

    return 0

def bdsimParserCavityModel() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_CavityModel()
    a = bdsim.CavityModel()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables


    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetCavityModels()

    # print
    print(ar)

    return 0

def bdsimParserCoolingChannel() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_CoolingChannel()
    a = bdsim.CoolingChannel()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables
    a['mirrorCoils'] = True # bool
    a['nCells'] = 5 # int
    a['cellLengthZ'] = 10.0 # double
    a['name'] = "test_name" # string
    a['rfWindowThickness'] = [1,2,3,4] # numberical array
    a['absorberType'] = ['a','b','c','d'] # string array

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetCoolingChannels()

    # print
    print(ar)

    return 0

def bdsimParserElement() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Parameters()
    a = bdsim.Parameters()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # set some variables

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    # print
    print(a)

    return 0

def bdsimParserField() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Field()
    a = bdsim.Field()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetFields()

    # print
    print(ar)

    return 0

def bdsimParserMaterial() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Material()
    a = bdsim.Material()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetMaterials()

    # print
    print(ar)

    return 0

def bdsimParserModulator() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Modulator()
    a = bdsim.Modulator()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetModulators()

    # print
    print(ar)

    return 0

def bdsimParserNewColour() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_NewColour()
    a = bdsim.NewColour()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetColours()

    # print
    print(ar)

    return 0

def bdsimParserOption() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Options()
    a = bdsim.Options()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    # print
    print(a)

    return 0

def bdsimParserPhysicsBiasing() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_PhysicsBias()
    a = bdsim.PhysicsBiasing()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetBiasingVector()

    # print
    print(ar)

    return 0

def bdsimParserPlacement() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Placement()
    a = bdsim.Placement()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetPlacements()

    # print
    print(ar)

    return 0

def bdsimParserQuery() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Query()
    a = bdsim.Query()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetQueries()

    # print
    print(ar)

    return 0

def bdsimParserRegion() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Region()
    a = bdsim.Region()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetRegions()

    # print
    print(ar)

    return 0

def bdsimParserScorer() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Scorer()
    a = bdsim.Scorer()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetScorers()

    # print
    print(ar)

    return 0

def bdsimParserScorerMesh() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_ScorerMesh()
    a = bdsim.ScorerMesh()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetScorerMeshes()

    # print
    print(ar)

    return 0

def bdsimParserTunnel() :
    import bdsim

    p = bdsim.BDSParser()

    # get global and create local
    ag = p.GetGlobal_Tunnel()
    a = bdsim.Tunnel()

    # check ability to get and set via dict
    for k in a.keys():
        ag[k] = a[k]

    # copy from local to global
    ag.copy_from(a)

    # check equal
    assert a == ag

    ar = p.GetTunnels()

    # print
    print(ar)

    return 0

def test_bdsimSetup_fromFile(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserSetup_fromFile, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetup_fromEmpty(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserSetup_fromEmpty, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserAccessors(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserAccessors, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserAperture(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserAperture, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserAtom(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserAtom, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserBeam(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserBeam, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserBeamline(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserBeamline, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserBLMPlacement(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserBLMPlacement, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserCavityModel(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserCavityModel, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserCoolingChannel(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserCoolingChannel, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupElement(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserElement, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupField(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserField, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupMaterial(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserMaterial, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupModulator(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserModulator, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupNewColour(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserNewColour, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupOption(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserOption, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupPhysicsBiasing(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserPhysicsBiasing, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupPlacement(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserPlacement, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupQuery(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserQuery, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupRegion(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserRegion, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupScorer(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserScorer, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupScorerMesh(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserScorerMesh, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupTunnel(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserTunnel, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)