import MDAnalysis as mda
import numpy as np

N = 6

bonds = np.array(
    [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 4],
        [4, 5],
        [5, 0],
    ]
)
benzene = mda.Universe.empty(
    N, atom_resindex=[0] * N, residue_segindex=[0], trajectory=True
)
benzene.add_TopologyAttr("bonds", bonds)


@profile
def am_slow(atoms):
    n_atoms = len(atoms)
    A = np.zeros((n_atoms, n_atoms), dtype=int)
    for bond in atoms.bonds:
        for i, ai in enumerate(atoms.atoms):
            for j, aj in enumerate(atoms.atoms):
                if ai in bond and aj in bond and i != j:
                    A[i, j] = 1
    return A


@profile
def am_fast(atoms):
    n_atoms = len(atoms)

    # Convert atom indices to range [0, n_atoms)
    b = atoms.bonds.to_indices()
    _, indices_flat = np.unique(b, return_inverse=True)
    indices = indices_flat.reshape(b.shape)

    A = np.zeros((n_atoms, n_atoms), dtype=int)
    A[indices[:, 0], indices[:, 1]] = 1

    return A + A.T


ams = am_slow(benzene.atoms)
amf = am_fast(benzene.atoms)

np.testing.assert_array_equal(ams, amf)
