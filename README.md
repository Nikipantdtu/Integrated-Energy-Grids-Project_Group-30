# Integrated Energy Grids — Assignment 2 (Group 30)

This repository contains the data and Jupyter notebooks developed for **Assignment 2** in the **Integrated Energy Grids** course.

## Contents
- **Jupyter Notebooks**: main analysis, calculations, and results
- **Data files**: input datasets used by the notebooks (if applicable)
- **Supporting scripts**: small Python utilities (if applicable)

## How to run

> **Important:** Some datasets are included as **compressed (.zip) archives inside the repository** (especially under the `tasks/` folder) because the raw files are large and could not be committed directly to GitHub. You must unzip these archives *in place* before running the corresponding notebook/task.

### 1) Download the repository

1. On GitHub, click **Code → Download ZIP** to download the entire repository.
2. **Extract/unpack** the downloaded repository ZIP to a local folder.

### 2) Unzip task data (required for many tasks)

For each task you want to run:

1. Navigate into the task folder (e.g. `tasks/<task-name>/`).
2. If you see a `data/` folder that contains one or more **.zip** files, **extract them inside that same `data/` folder**.
   - After unzipping, you should have the actual dataset files/folders next to (or replacing) the zip file(s).
   - Keep the folder structure unchanged so the notebooks’ relative paths keep working.

### 3) Run notebooks/scripts

1. Open **Visual Studio Code** (or JupyterLab).
2. Open the **top-level repository folder** (the folder you extracted).
3. Run the notebooks/scripts with the repository root as your **working directory** so all relative paths resolve correctly.

### Notes / troubleshooting

- If you get “file not found” / `FileNotFoundError`, double-check that you have **unzipped the required data archives** for that specific task under `tasks/.../data/`.
- If you run a notebook/script from a different working directory, you may also get path errors because many paths are relative to the repository root.
- If you moved files or only downloaded individual folders, re-download the full repo ZIP and unzip again to restore the expected structure.

## Requirements
Typical setup (adjust to your environment):
- Python 3.x
- Jupyter Notebook / JupyterLab
- Common scientific libraries (e.g., `numpy`, `pandas`, `matplotlib`)

## Notes
- Notebook cells may need to be run in order (top to bottom) to reproduce results.
- If any file paths break, ensure datasets are located in the expected folders referenced in the notebooks.

## Authors
Group 30 (Integrated Energy Grids course)