"""Gmsh mesh -> XDMF converter. THIS IS THE ONE USED FOR THE NEW FEniCSx SIMULATION.

Input:  a Gmsh .msh file generated from Rooney3D.geo (with physical groups:
        volumes 295=Al, 296=Al2O3, 297=GeSi, 298=Ge; surfaces 299=Base, 300=Top).
Run in the MODERN environment:

    conda activate fenicsx
    gmsh -3 Rooney3D.geo -o Rooney3D.msh
    python gmsh_to_xdmf.py Rooney3D.msh rooney3d

Outputs (read by "Strain Simulation FEniCSx.ipynb", GRID_NAME = "Grid"):
    rooney3d.xdmf / .h5            - tetrahedral volume mesh
    rooney3d_subdomains.xdmf / .h5 - cell tags (physical volumes: materials)
    rooney3d_boundaries.xdmf / .h5 - facet tags (physical surfaces: BCs)

(If starting from legacy FEniCS XML mesh files instead, use legacy_xml_to_xdmf.py.)
"""

import sys

import meshio
import numpy as np


def main(msh_file, out_prefix="rooney3d"):
    msh = meshio.read(msh_file)

    points = msh.points
    tetra = msh.get_cells_type("tetra")
    tetra_tags = msh.get_cell_data("gmsh:physical", "tetra")
    triangles = msh.get_cells_type("triangle")
    triangle_tags = msh.get_cell_data("gmsh:physical", "triangle")

    meshio.write(out_prefix + ".xdmf",
                 meshio.Mesh(points=points, cells={"tetra": tetra}))
    meshio.write(out_prefix + "_subdomains.xdmf",
                 meshio.Mesh(points=points, cells={"tetra": tetra},
                             cell_data={"subdomains": [tetra_tags]}))
    meshio.write(out_prefix + "_boundaries.xdmf",
                 meshio.Mesh(points=points, cells={"triangle": triangles},
                             cell_data={"boundaries": [triangle_tags]}))

    print(f"cells: {len(tetra)}, material tags: {np.unique(tetra_tags)}, "
          f"boundary tags: {np.unique(triangle_tags)}")
    print(f"Wrote {out_prefix}.xdmf, {out_prefix}_subdomains.xdmf, {out_prefix}_boundaries.xdmf")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "rooney3d")
