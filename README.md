# G-Factor Simulation Project

## Description
This repository contains a series of Jupyter notebooks used for simulating and analyzing the G-Factor in a given material. The project includes detailed simulation steps, parameter validations, and data analysis.

## Table of Contents
- [Notebooks](#notebooks)
  - [G-Factor Simulation.ipynb](#g-factor-simulationipynb)
  - [G-Factor Simulation Quick.ipynb](#g-factor-simulation-quickipynb)
  - [Data Analysis.ipynb](#data-analysisipynb)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Code](#running-the-code)
- [Contact](#contact)

## Notebooks

### G-Factor Simulation.ipynb
This notebook is the initial simulation code that documents the entire thought process and problem-solving journey of the project. It includes:
- Validation of material-specific parameters (e.g., Lame coefficients).
- Output of simulation results in two formats:
  - **XDMF**: For viewing using Preview.
  - **CSV**: Contains values of strain components on a lattice of points for plotting in separate code.

### G-Factor Simulation Quick.ipynb
This streamlined notebook is designed for efficiency, keeping only the essential parts of the simulation:
- Focus on solving the PDE and extracting solution data.
- Optimized for quick modifications and solution retrieval.

### Data Analysis.ipynb
This notebook is used for:
- Analyzing the data of strain tensor components extracted from the simulation.
- Plotting the strain tensor and G-Factor correction distributions.

## Installation
To run the code, you need to install the FEniCS legacy version. Follow the installation instructions [here](https://fenicsproject.org/download/).

## Usage

### Running the Code
1. **Install FEniCS**: Follow the installation instructions for the FEniCS legacy version [here](https://fenicsproject.org/download/).
2. **Open Notebooks**: Use Jupyter to open the `.ipynb` files.
3. **Geometry and Mesh Generation**:
   - Use **gmsh** to open the `.geo` file and generate the mesh.
   - Save the generated mesh to a `.msh` file.
4. **Convert Mesh**:
   - Open the directory containing the `.msh` file in the terminal.
   - Use `dolfin-convert` to convert the `.msh` file to `.xml`:
     ```bash
     dolfin-convert mesh.msh mesh.xml
     ```

## Contact
For any questions or further information, please contact Mu Niu at lucaniu2003@g.ucla.edu
