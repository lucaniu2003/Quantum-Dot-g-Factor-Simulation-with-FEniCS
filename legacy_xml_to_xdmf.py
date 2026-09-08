"""Legacy FEniCS XML mesh -> XDMF converter. FALLBACK ONLY - not needed if you have Rooney3D.geo.

Use this ONLY when starting from legacy FEniCS 2019 XML mesh files
(Rooney3D.xml + Rooney3D_physical_region.xml + Rooney3D_facet_region.xml).
For the normal Gmsh workflow (Rooney3D.geo -> .msh), use gmsh_to_xdmf.py instead.

Run this in the LEGACY environment (it needs `import dolfin` from FEniCS 2019):

    conda activate fenics
    python legacy_xml_to_xdmf.py Rooney3D.xml Rooney3D_physical_region.xml Rooney3D_facet_region.xml

Outputs (read by "Strain Simulation FEniCSx.ipynb", GRID_NAME = "mesh"):
    rooney3d.xdmf / rooney3d.h5             - mesh
    rooney3d_subdomains.xdmf / .h5          - cell tags (materials)
    rooney3d_boundaries.xdmf / .h5          - facet tags (boundary conditions)
"""

import sys

import dolfin as fn


def main(mesh_xml, subdomains_xml, boundaries_xml, out_prefix="rooney3d"):
    mesh = fn.Mesh(mesh_xml)

    subdomains = fn.MeshFunction("size_t", mesh, subdomains_xml)
    subdomains.rename("subdomains", "subdomains")

    boundaries = fn.MeshFunction("size_t", mesh, boundaries_xml)
    boundaries.rename("boundaries", "boundaries")

    with fn.XDMFFile(out_prefix + ".xdmf") as f:
        f.write(mesh)
    with fn.XDMFFile(out_prefix + "_subdomains.xdmf") as f:
        f.write(subdomains)
    with fn.XDMFFile(out_prefix + "_boundaries.xdmf") as f:
        f.write(boundaries)

    print("Wrote %s.xdmf, %s_subdomains.xdmf, %s_boundaries.xdmf"
          % (out_prefix, out_prefix, out_prefix))


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(*sys.argv[1:4], out_prefix=sys.argv[4] if len(sys.argv) > 4 else "rooney3d")
