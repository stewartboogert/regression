import os

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

    #b = bdsim.BDSIM(p)
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

def bdsimParserElement() :
    import bdsim

    p = bdsim.BDSParser()

    b = p.GetBeam()
    b.set_value("particle","e-")
    b.set_value("energy",10.0)
    b.set_value("distrType","reference")

    o = p.GetOptions()
    o['batch'] = True
    o['outputFormat'] ="none"

    e = p.GetGlobal_Parameters()
    e.flush()
    #e['name'] = "d1"
    #e['type'] = bdsim.elementtype.ElementType.DRIFT # TODO
    e['l'] = 1.0
    p.write_table(e.name,e.type,False)

    p.PrintElements()
    p.PrintBeamline()

    b = bdsim.BDSIM(p)
    b.BeamOn(10)

    return 0


def bdsimParserBeamline() :
    import bdsim

    p = bdsim.BDSParser()

    b = p.GetBeam()
    b['particle'] = 'e-'
    b['energy'] = 10.0
    b['distrType'] = 'reference'

    o = p.GetOptions()
    # o.set_value("batch",1)
    o['batch'] = True # set_value for batch does not work
    o['outputFormat'] = 'none'

    e = p.GetGlobal_Parameters()

    # drift 1
    e.flush()
    # e['name'] = "d1"
    #e['type'] = bdsim.elementtype.ElementType.DRIFT
    e['l'] = 1.0
    p.write_table(e.name,e.type,False)

    # drift 2
    e.flush()
    # e['name']= "d2"
    e['l'] = 2.0
    # p.write_table(e.name,e.type,False) # TODO duplicate name

    # line 0
    e.flush()
    # e['name'] = "l0"
    #e['type'] = bdsim.elementtype.ElementType.LINE
    #p.add_element_temp("d1",1,False,bdsim.elementtype.ElementType.DRIFT)
    # p.add_element_temp("d2",1,False,bdsim.elementtype.ElementType.DRIFT) # TODO duplicate name
    #p.write_table(e.name, e.type, False)

    #p.expand_line("l0","d1","d2")
    # p.GetSequence("l0")

    # print out beamlines
    p.PrintElements()
    p.PrintBeamline()

    # b = bdsim.BDSIM(p)
    # b.BeamOn(10)

    return 0

def bdsimParserAperture() :
    import bdsim

    p = bdsim.BDSParser.Instance("./trackerInterface.gmad")

    ga = p.GetGlobal_Aperture()
    a = bdsim.Aperture()
    a['apertureType'] = 'elliptical'
    a['aper1'] = 1.0
    a['aper2'] = 2.0
    a['aper3'] = 3.0
    a['aper4'] = 4.0
    ga.copy_from(a)
    p.Add_Aperture()

    ar = p.GetApertures()

def bdsimParserAtoms():
    pass

def bdsimParserBeam() :
    pass

def bdsimParserElements() :
    pass

def bdsimParserOptions() :
    pass

def test_bdsimSetup_fromFile(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserSetup_fromFile, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetup_fromEmpty(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserSetup_fromEmpty, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserAccessors(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserAccessors, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupElement(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserElement, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimSetupBeamline(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserBeamline, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)

def test_bdsimParserAperture(make_bdsim_test_code, run_bdsim_test_code_as_subprocess) :
    code_to_run = make_bdsim_test_code(bdsimParserAperture, args="", dir=os.path.dirname(os.path.abspath(__file__)))
    output = run_bdsim_test_code_as_subprocess(code_to_run)
