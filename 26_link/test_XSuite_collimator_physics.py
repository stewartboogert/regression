"""Physical regression tests for Xcoll's BDSIM link.

The same transverse proton distribution is transported through open and
closed Geant4 collimators made from three different materials.  Standard
and tipped jaws are exercised with both parallel and tilted geometries.
Persistent particle-count and spectrum summaries make it possible to
compare Xcoll before and after changes to BDSLink.
"""

from __future__ import annotations

import json
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np
import pytest
import xcoll as xc
import xpart as xp
import xtrack as xt


pytestmark = pytest.mark.xfail(reason="requires bdsim and the Xcoll Geant4 interface")

NPRIMARY = 2_000
P0C = 7e12
COLLIMATOR_LENGTH = 0.6
OPEN_JAW = 0.5e-3
CLOSED_JAW = 10e-6
OPEN_JAW_TILT = 1e-3
CLOSED_JAW_TILT = 10e-6
TIP_THICKNESS = 0.05
SEED = 1234

ENERGY_RATIO_BINS = np.linspace(0, 1.01, 102)
ANGLE_BINS = np.linspace(-5e-3, 5e-3, 101)


def _material(name: str) -> Any:
    """Return one of the elemental materials used in the regression."""
    return getattr(xc.materials, name)


def _particles(nprimary: int) -> xp.Particles:
    """Create a deterministic flat beam spanning both collimator jaws."""
    half_step = 1e-3 / nprimary
    x = np.linspace(-1e-3, 1e-3, nprimary, endpoint=False) + half_step
    particle_id = np.arange(nprimary, dtype=np.int64)
    return xp.Particles(
        _capacity=50 * nprimary,
        p0c=P0C,
        q0=1,
        mass0=xp.PROTON_MASS_EV,
        pdg_id=2212,
        x=x,
        px=np.zeros(nprimary),
        y=np.zeros(nprimary),
        py=np.zeros(nprimary),
        zeta=np.zeros(nprimary),
        delta=np.zeros(nprimary),
        particle_id=particle_id,
    )


def _collimator(
    collimator_type: str,
    material_name: str,
    jaw: float,
    tilt: float,
) -> xc.Geant4Collimator:
    """Build a standard or tipped Geant4 jaw collimator."""
    kwargs = {
        "length": COLLIMATOR_LENGTH,
        "material": _material(material_name),
        "jaw": jaw,
        "tilt": tilt,
    }
    if collimator_type == "jaw":
        return xc.Geant4Collimator(**kwargs)
    if collimator_type == "tip":
        return xc.Geant4CollimatorTip(
            **kwargs,
            tip_material=xc.materials.Tungsten,
            tip_thickness=TIP_THICKNESS,
        )
    raise ValueError(f"Unsupported collimator type: {collimator_type}")


def _histogram(values: np.ndarray, bins: np.ndarray) -> dict[str, list[float] | list[int]]:
    """Return a JSON-serialisable histogram with fixed bin edges."""
    counts, edges = np.histogram(values, bins=bins)
    return {"counts": counts.tolist(), "edges": edges.tolist()}


def _summarise(particles: xp.Particles, nprimary: int) -> dict[str, Any]:
    """Summarise primary suppression and the returned secondary spectra."""
    state = np.asarray(particles.state)
    particle_id = np.asarray(particles.particle_id)
    valid = (state != 0) & (particle_id >= 0)
    primary = valid & (particle_id < nprimary)
    secondary = valid & ~primary
    alive = state > 0

    energy = np.asarray(particles.energy)
    reference_energy = float(particles.energy0[0])
    energy_ratio = energy / reference_energy
    high_energy_primary = primary & alive & (energy_ratio > 0.99)

    pdg_ids, pdg_counts = np.unique(
        np.asarray(particles.pdg_id)[valid], return_counts=True
    )

    return {
        "primary_alive": int(np.count_nonzero(primary & alive)),
        "primary_lost": int(np.count_nonzero(primary & ~alive)),
        "primary_high_energy": int(np.count_nonzero(high_energy_primary)),
        "secondary_alive": int(np.count_nonzero(secondary & alive)),
        "secondary_lost": int(np.count_nonzero(secondary & ~alive)),
        "pdg_counts": {
            str(int(pdg_id)): int(count)
            for pdg_id, count in zip(pdg_ids, pdg_counts)
        },
        "energy_ratio": _histogram(energy_ratio[valid & alive], ENERGY_RATIO_BINS),
        "px": _histogram(np.asarray(particles.px)[valid & alive], ANGLE_BINS),
        "py": _histogram(np.asarray(particles.py)[valid & alive], ANGLE_BINS),
    }


def _ensure_geant4_interface() -> None:
    """Compile the Xcoll bridge once when it is not already available."""
    if not xc.geant4.interface.compiled:
        xc.geant4.interface.compile(verbose=True)
    assert xc.geant4.interface.ready


@pytest.mark.parametrize(
    "material_name, aperture_name, jaw, collimator_type, tilt",
    [
        pytest.param("Copper", "open", OPEN_JAW, "jaw", 0.0, id="copper-open-jaw"),
        pytest.param("Copper", "closed", CLOSED_JAW, "jaw", 0.0, id="copper-closed-jaw"),
        pytest.param("Iron", "open", OPEN_JAW, "jaw", 0.0, id="iron-open-jaw"),
        pytest.param("Iron", "closed", CLOSED_JAW, "jaw", 0.0, id="iron-closed-jaw"),
        pytest.param("Tungsten", "open", OPEN_JAW, "jaw", 0.0, id="tungsten-open-jaw"),
        pytest.param("Tungsten", "closed", CLOSED_JAW, "jaw", 0.0, id="tungsten-closed-jaw"),
        pytest.param("Copper", "open", OPEN_JAW, "jaw", OPEN_JAW_TILT, id="copper-open-jaw-tilted"),
        pytest.param("Copper", "closed", CLOSED_JAW, "jaw", CLOSED_JAW_TILT, id="copper-closed-jaw-tilted"),
        pytest.param("Copper", "open", OPEN_JAW, "tip", 0.0, id="copper-open-tip"),
        pytest.param("Copper", "closed", CLOSED_JAW, "tip", 0.0, id="copper-closed-tip"),
        pytest.param("Copper", "open", OPEN_JAW, "tip", OPEN_JAW_TILT, id="copper-open-tip-tilted"),
        pytest.param("Copper", "closed", CLOSED_JAW, "tip", CLOSED_JAW_TILT, id="copper-closed-tip-tilted"),
    ],
)
def test_xcoll_collimator_physics(
    testdata_store: Any,
    tmp_path: Path,
    material_name: str,
    aperture_name: str,
    jaw: float,
    collimator_type: str,
    tilt: float,
) -> None:
    """Track the same proton beam through each material/aperture case."""
    _ensure_geant4_interface()

    tilt_name = "tilted" if tilt else "parallel"
    case_name = (
        f"{material_name.lower()}_{aperture_name}_{collimator_type}_{tilt_name}"
    )
    collimator = _collimator(collimator_type, material_name, jaw, tilt)
    line = xt.Line(elements=[collimator], element_names=[case_name])
    line.particle_ref = xp.Particles(
        p0c=P0C,
        q0=1,
        mass0=xp.PROTON_MASS_EV,
        pdg_id=2212,
    )
    line.build_tracker()
    particles = _particles(NPRIMARY)

    engine = xc.geant4.engine
    run_directory = tmp_path / case_name
    run_directory.mkdir(parents=True)
    start = perf_counter()
    try:
        engine.start(line=line, cwd=run_directory, seed=SEED)
        line.xcoll.scattering.enable()
        line.track(particles)
    finally:
        if engine.is_running():
            engine.stop(clean=True)
    elapsed = perf_counter() - start

    summary = {
        "configuration": {
            "material": material_name,
            "geant4_material": _material(material_name).geant4_name,
            "aperture": aperture_name,
            "collimator_type": collimator_type,
            "jaw": jaw,
            "jaw_corners": {
                "left_upstream": collimator.jaw_LU,
                "left_downstream": collimator.jaw_LD,
                "right_upstream": collimator.jaw_RU,
                "right_downstream": collimator.jaw_RD,
            },
            "tilt": tilt,
            "length": COLLIMATOR_LENGTH,
            "p0c": P0C,
            "nprimary": NPRIMARY,
            "seed": SEED,
        },
        "result": _summarise(particles, NPRIMARY),
    }
    if collimator_type == "tip":
        summary["configuration"]["tip_material"] = "W"
        summary["configuration"]["tip_thickness"] = TIP_THICKNESS

    output_path = Path(__file__).parent / f"xcoll_{case_name}.json"
    output_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")

    if aperture_name == "open" and not tilt:
        assert 900 < summary["result"]["primary_alive"] < 1200
        assert 900 < summary["result"]["primary_high_energy"] < 1100
        assert 800 < summary["result"]["primary_lost"] < 1100
    elif aperture_name == "open":
        # The tilted channel moves transversely along the collimator, so its
        # through-acceptance is smaller than for otherwise identical
        # parallel jaws.
        assert 400 < summary["result"]["primary_alive"] < 800
        assert 400 < summary["result"]["primary_high_energy"] < 800
        assert 1200 < summary["result"]["primary_lost"] < 1600
        assert summary["result"]["secondary_alive"] > 0
    else:
        assert summary["result"]["primary_lost"] > 1000
        assert summary["result"]["primary_high_energy"] < 500
        assert summary["result"]["secondary_alive"] > 0

    test_entry = testdata_store.new_test_entry(
        f"26_link/xcoll_{case_name}", __file__, NPRIMARY, elapsed
    )
    test_entry.add_input_parameter_dict(summary["configuration"])
    test_entry.add_output_parameter_dict(
        {
            "primary_alive": summary["result"]["primary_alive"],
            "primary_lost": summary["result"]["primary_lost"],
            "primary_high_energy": summary["result"]["primary_high_energy"],
            "secondary_alive": summary["result"]["secondary_alive"],
            "secondary_lost": summary["result"]["secondary_lost"],
        }
    )
    test_entry.add_output_file(str(output_path), "json")
