import hashlib as _hashlib

def find_primary_index(t) :
    ntraj = t.n

    for itraj in range(ntraj) :
        if t.parentID[itraj] == 0 :
            return itraj

def build_topdown_tree(t) :
    '''
    Build arrays to allow top down tree navigation (daugter_index and daugter_step)
    '''
    ntraj = t.n

    daughter_index = [[] for _ in range(ntraj)]
    daughter_step = [[] for _ in range(ntraj)]

    # loop over all trajectories
    for itraj in range(ntraj) :

        if t.parentID[itraj] == 0 :
            continue

        parent_index = t.parentIndex[itraj]
        parent_step  = t.parentStepIndex[itraj]
        daughter_index[parent_index].append(itraj)
        daughter_step[parent_index].append(parent_step)

    # loop over all trajectories and sort on daughter_step
    for itraj in range(ntraj) :
        sorted_pairs = sorted(zip(daughter_step[itraj], daughter_index[itraj]))
        if len(sorted_pairs) == 0 :
            continue
        daughter_step_sorted, daughter_index_sorted = zip(*sorted_pairs)

        daughter_index[itraj] = list(daughter_index_sorted)
        daughter_step[itraj] = list(daughter_step_sorted)

    return daughter_index, daughter_step

def hash_trajectory(t, itraj) :

    nstep = t.xyz[itraj].size()

    depth = t.depth[itraj]
    parentID = t.parentID[itraj]
    parentIndex = t.parentIndex[itraj]
    parentStepIndex = t.parentStepIndex[itraj]
    partID = t.partID[itraj]

    charge = t.charge[itraj]
    energyDeposit = t.energyDeposit[itraj]
    ionA = t.ionA[itraj]
    ionZ = t.ionZ[itraj]
    kineticEnergy = t.kineticEnergy[itraj]
    mass = t.mass[itraj]
    modelIndicies = t.modelIndicies[itraj]
    nElectrons = t.nElectrons[itraj]

    pxpypz = t.pxpypz[itraj]
    PXPYPZ = t.PXPYPZ[itraj]
    xyz = t.xyz[itraj]
    XYZ = t.XYZ[itraj]
    T = t.T[itraj]
    S = t.S[itraj]

    hash = _hashlib.sha256(str(nstep).encode('utf-8')).digest()
    hash += _hashlib.sha256(str(depth).encode('utf-8')).digest()
    hash += _hashlib.sha256(str(parentID).encode('utf-8')).digest()
    hash += _hashlib.sha256(str(parentIndex).encode('utf-8')).digest()
    hash += _hashlib.sha256(str(parentStepIndex).encode('utf-8')).digest()
    hash += _hashlib.sha256(str(partID).encode('utf-8')).digest()

    for istep in range(nstep) :
        hash += _hashlib.sha256(str(charge[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(energyDeposit[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(ionA[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(ionZ[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(kineticEnergy[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(mass[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(modelIndicies[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(nElectrons[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(xyz[istep][0]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(xyz[istep][1]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(xyz[istep][2]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(XYZ[istep][0]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(XYZ[istep][1]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(XYZ[istep][2]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(pxpypz[istep][0]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(pxpypz[istep][1]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(pxpypz[istep][2]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(PXPYPZ[istep][0]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(PXPYPZ[istep][1]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(PXPYPZ[istep][2]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(T[istep]).encode('utf-8')).digest()
        hash += _hashlib.sha256(str(S[istep]).encode('utf-8')).digest()

    return hash

def visit_trajectories(t, itraj, daugher_index, daughter_step, itraj_start, traj_hash_func = None) :
    visited = [itraj]

    hash = hash_trajectory(t,itraj)

    for dtraj in daugher_index[itraj]:
        dvisited, dhash = visit_trajectories(t, dtraj, daugher_index, daughter_step, traj_hash_func)
        visited.extend(dvisited)
        hash = _hashlib.sha256(hash + dhash).digest()

    return visited, hash

def traverse_trajectories(t, traj_hash_func = None) :

    # build top down trajectory
    daughter_index, daughter_step = build_topdown_tree(t)

    # find primary
    iprimary = find_primary_index(t)

    # recurse down tree
    visted, hash = visit_trajectories(t, iprimary, daughter_index, daughter_step, traj_hash_func)

    assert len(visted) == len(set(visted))

    return visted, hash

# fd164e65e786b400e08990cdeaf0d57aa21d3a78d3c92f7a40c1f28d914be8c9
# 31a652830cffa07905a4be0224b6b4388ad3d84f7fdb08ffdcd15603adaaf1a2