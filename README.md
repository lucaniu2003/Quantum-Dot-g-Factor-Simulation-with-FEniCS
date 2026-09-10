# Quantum Dot g-Factor Simulation

This project simulates thermally induced strain in a Ge/SiGe double quantum dot
heterostructure (Rooney-style device geometry) and computes the resulting
corrections to the hole g-tensor. The workflow has two stages:

1. **Strain simulation** (FEniCSx) — solve a thermoelastic problem on a 3D
   device mesh and export strain/displacement fields to CSV.
2. **g-tensor analysis** (post-processing) — load the strain CSVs, compute
   site-dependent g-tensor corrections, and average them over the quantum dot
   wavefunctions (modeled as 3D Gaussians) as a function of the barrier gate
   voltage `Brm`.

## Software environment

- **Current pipeline**: FEniCSx (`dolfinx`) **0.11.0**, in the `fenicsx` conda
  environment (`conda activate fenicsx`). The exact version used for each
  archived run is recorded in that run's `parameters.json`.
- **Legacy notebooks** (`G-Factor Simulation*.ipynb`) use the legacy FEniCS
  `dolfin` API (with `mshr`) in the `fenics` conda environment. They are kept
  for reference; the FEniCSx notebook is the one used to generate the current
  data.
- Mesh generation/conversion: **Gmsh** (`gmsh -3`) plus `meshio` via
  `gmsh_to_xdmf.py`.
- Post-processing: NumPy, pandas, SciPy, matplotlib.

## Mesh files

Only the **medium-refined** mesh is kept in this repository; it is the mesh all
current data was generated with (727,475 cells):

- `Rooney3D_medium.geo` — Gmsh geometry script (region IDs: 295 = Al,
  296 = Al₂O₃, 297 = GeSi, 298 = Ge; boundary IDs 299/300 = outer boundaries).
- `Rooney3D_medium.msh` — generated with
  `gmsh -3 Rooney3D_medium.geo -o Rooney3D_medium.msh`.
- `rooney3d_medium.xdmf` / `.h5` — mesh in XDMF format.
- `rooney3d_medium_subdomains.xdmf` / `.h5` — subdomain (material) markers.
- `rooney3d_medium_boundaries.xdmf` / `.h5` — boundary (facet) markers.

The three XDMF sets are produced from the `.msh` file with
`python gmsh_to_xdmf.py Rooney3D_medium.msh rooney3d_medium`.

## Notebooks

### `Strain Simulation FEniCSx.ipynb` — main simulation

FEniCSx (dolfinx) thermoelastic strain simulation; the notebook that generates
all current data.

- **Mesh import**: reads `rooney3d_medium*.xdmf` (mesh + subdomain and boundary
  markers).
- **Material parameters**: per-region Lamé parameters (λ, μ) and thermal
  expansion coefficients (α) keyed on the subdomain markers.
- **Thermal problem**: steady-state heat equation with 280 K Dirichlet
  conditions on the outer boundaries (tags 299/300).
- **Strain problem**: displacement field from thermal expansion with
  fixed-displacement boundary conditions (CG + hypre BoomerAMG; Lagrange
  degree-2 vector space), then strain ε = sym(grad u).
- **Outputs**:
  - Raw run archive in `Raw Simulation Results/<timestamp>/` (see below).
  - CSV exports in `simulation_YYYY-MM-DD/` (see below).

### `3D_Average.ipynb` — g-tensor correction averaging over the dot wavefunctions

- Loads the 3D strain CSVs from `simulation_2026-09-08/strain_3D/`.
- Computes the site-dependent LH–HH splitting Δ_LH and the g-tensor correction
  components δg_xx, δg_xy, δg_zx, δg_zy from the strain (k·p parameters
  `b`, `κ`, `d`). Throughout the notebook these corrections are named
  `delta_g_*` (e.g. `delta_g_xx_data`, `delta_g_xx_func`) to distinguish them
  from the bare g-tensor itself; the only full-g quantities are the bare
  reference values `g0_in_plane = 0.15` and `g0_out_of_plane = 13.5`, used to
  express the corrections as percentages.
- Evaluates the 3D Gaussian wavefunctions from `Left_Dot_Gaussian.csv` /
  `Right_Dot_Gaussian.csv` (one row per `Brm` value) and computes the
  Gaussian-weighted average of each g-tensor correction component for the left
  and right dots at each `Brm`. Results are saved to
  `Left_Dot_Gaussian_Delta_G_Averages.csv` and
  `Right_Dot_Gaussian_Delta_G_Averages.csv` (columns `delta_g_xx`,
  `delta_g_xy`, `delta_g_zx`, `delta_g_zy`).
- Plots per-dot δg components vs. `Brm` and the effective g-factor correction
  δg\* as a function of in-plane field angle φ and `Brm` for the left dot,
  right dot, and the singlet-triplet qubit (difference of the two dots'
  corrections) →
  `graph/<date>/Left_Right_Dot_delta_g_combined.pdf`,
  `delta_g_correction_contour_comparison_3D.pdf`.

### `Average_G_Tensor_Distribution.ipynb` — 2D spatial distributions

- Loads the 2D strain slice CSVs from `simulation_2026-09-08/strain_2D/`.
- Plots the spatial distributions of the strain components, the LH–HH band
  gap Δ_LH, and the site-dependent g-tensor corrections (eqs. 9–12) on the
  z = 50 plane → `strain_distribution.pdf`, `LH-HH_band_gap.pdf`,
  `g_tensor_correction.pdf`.

### `Displacement_Calculation_and_Height_Dependence_Calculation.ipynb`

- **Displacement**: loads `simulation_2026-09-08/displacement/` and plots the
  displacement components on the z = 50 plane → `displacement_components.pdf`.
- **Dependence on height**: loads the 3D strain CSVs, splits the Ge well
  (z = 42–58) into 8 z-slices, and plots mean ± std of the strain components
  per slice plus the subset-to-global strain ratio →
  `maximum_strain_magnitudes.pdf`, `strain_subset_to_global_ratio.pdf`.

### `G-Factor Simulation.ipynb` / `G-Factor Simulation Quick.ipynb` — legacy

Legacy FEniCS (`dolfin`) versions of the strain simulation. They load the old
`Rooney3D.xml` mesh, run the same thermal + strain solves, and export 2D strain slices.
The Quick version skips intermediate visualizations and exports on a finer
grid. Superseded by `Strain Simulation FEniCSx.ipynb`.

## Helper scripts

- `gmsh_to_xdmf.py` — converts a Gmsh `.msh` file into the three XDMF/H5 sets
  (mesh, subdomains, boundaries) read by the FEniCSx notebook.
- `legacy_xml_to_xdmf.py` — converts legacy FEniCS XML meshes to XDMF (run in
  the `fenics` env; use `GRID_NAME = "mesh"` when reading the result).

## Data folders

### `simulation_2026-09-08/` — current dataset

CSV exports from `Strain Simulation FEniCSx.ipynb`. Coordinates are already in
the exported convention: x = mesh_x − 1.25, y = mesh_y − 108.05,
z = −z_mesh − 13 (Ge well spans z = 42–58, top to bottom edge). Each subfolder
has a `metadata.json` describing grid, ranges, and conventions.

- `displacement/` — `displacement_data.csv`: u_x, u_y, u_z on a 400×400 grid
  at z = 50.
- `strain_2D/` — six strain components (ε_yy−ε_xx, ε_yy+ε_xx, ε_zz, ε_xy,
  ε_xz, ε_yz) on a 400×400 grid at z = 50.
- `strain_3D/` — the same six components on a 300×300×30 grid covering the Ge
  well (z = 42–58).

> **Note: the 3D strain CSVs are not on GitHub.** Each `strain_*_3D.csv` file
> is ~200 MB (six files, ~1.2 GB total), far above GitHub's 100 MB per-file
> limit, so they must be regenerated locally. This is exactly reproducible —
> see "Regenerating the 3D strain CSVs" below. The small files
> (`metadata.json`, the 2D strain and displacement CSVs) are checked in.

### Regenerating the 3D strain CSVs

The 3D exports are a deterministic post-processing step: they are computed by
sampling the solved displacement field on a fixed 300×300×30 grid. Everything
needed to reproduce them bit-for-bit is stored in the much smaller raw run
archives (~45 MB each) under `Raw Simulation Results/` — no re-solving of the
PDE is required. To regenerate the current `simulation_2026-09-08/strain_3D/`
files:

1. Activate the environment: `conda activate fenicsx`.
2. Open `Strain Simulation FEniCSx.ipynb` and set
   `LOAD_RUN = "Raw Simulation Results/2026-09-07_10-08-24"` in the
   configuration cell (this is the archived medium-mesh run that the current
   dataset was exported from). When `LOAD_RUN` is set, the notebook loads the
   mesh, `parameters.json`, and `displacement.npy` from that archive instead
   of re-running the thermal/strain solves.
3. Run the initialization and mesh-import cells, then skip the "Solving"
   section and run the "Post-Processing" and "Generating Data Files" sections
   (specifically "Extract 3D Strain Values (3D CSV exports)"). The resulting
   CSVs are identical to the ones used for the figures in `graph/`.

The same procedure works for any archived run — point `LOAD_RUN` at its folder
to re-export its strain data at any grid resolution.

### `Raw Simulation Results/<timestamp>/` — archived raw runs

One folder per FEniCSx run, each containing a copy of the mesh files used,
`displacement.npy`, `temperature.npy`, and `parameters.json` (dolfinx version,
mesh, cell count, material properties, boundary conditions, solver settings,
grid configuration). The 2026-09-05 and 2026-09-07_00-40 runs used the
original (non-medium) `rooney3d` mesh; the later runs used the medium mesh.

### `graph/<date>/` — figures

PDF figures produced by the analysis notebooks, organized by the date they
were generated.

## Other files

- `Left_Dot_Gaussian.csv` / `Right_Dot_Gaussian.csv` — per-`Brm` 3D Gaussian
  fits (center + covariance) of the hole wavefunction |ψ|² in each dot.
  **Not generated in this repository** — they come from a separate
  electrostatic/Schrödinger simulation swept over the `Brm` gate voltage.
- `Left_Dot_Gaussian_Delta_G_Averages.csv` / `Right_Dot_Gaussian_Delta_G_Averages.csv` —
  Gaussian-averaged g-tensor correction components (δg; columns
  `delta_g_xx`, `delta_g_xy`, `delta_g_zx`, `delta_g_zy`) per `Brm`, generated
  by `3D_Average.ipynb`.

## Run order

1. `Strain Simulation FEniCSx.ipynb` (in the `fenicsx` env) — generates
   `simulation_YYYY-MM-DD/` and a `Raw Simulation Results/` archive.
2. Analysis notebooks (any order): `3D_Average.ipynb`,
   `Average_G_Tensor_Distribution.ipynb`,
   `Displacement_Calculation_and_Height_Dependence_Calculation.ipynb` — read
   from `simulation_2026-09-08/` and write figures to `graph/<date>/`.
