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
    pass

def visit_trajectories(t, daugher_index, daughter_step, itraj_start, traj_hash_func = None) :
    pass


def traverse_trajectories(t, traj_hash_func = None) :
    daughter_index, daughter_step = build_topdown_tree(t)

    # recurse down tree
    visit_trajectories(t, daughter_index, daughter_step, traj_hash_func)


