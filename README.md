# Integration of multi-modal data and visualization using TissUUmaps 4

Course materials for the workshop _Integration of multi-modal data and visualization using TissUUmaps 4_ at [I2KxBINA2026](https://www.bioimagingnorthamerica.org/events/i2kxbina2026/#program).

## Overview

This repository contains the Jupyter notebooks, helper code and software environment used during the workshop. <!--The accompanying slides are available [here](https://example.com/slides) TODO: replace with link to slides -->.

## Prerequisites

- [Git](https://git-scm.com/) (optional, for cloning the repository)
- [Pixi](https://pixi.sh/latest/#installation) package manager
- A supported platform: Linux (x86-64), Windows (x86-64) or macOS (Apple Silicon) <!-- TODO: add osx-arm64 and osx-64 to platforms in pixi.toml and update pixi.lock -->
- The course data, available on [Zenodo](https://zenodo.org/records/22948439)

## Instructions

1. Clone the repository (or [download](https://github.com/BIIFSweden/I2KWorkshop_2026/archive/refs/heads/main.zip) it as a ZIP archive) and enter the directory:

   ```bash
   git clone https://github.com/BIIFSweden/I2KWorkshop_2026.git
   cd I2KWorkshop_2026
   ```

2. Download the three data archives from [Zenodo](https://zenodo.org/records/22948439) and extract them into the `data` folder, so that it looks like this (no additional nested folders):

   ```
   data/
   ├── BC_histology/
   │   ├── data.md
   │   └── ...
   ├── HE_LiverSections/
   └── MultimodalData/
   ```

3. Install the Pixi environments and register the Jupyter kernels:

   ```bash
   pixi install -e spatial
   pixi install -e registration

   pixi run -e spatial python -m ipykernel install --user --name i2k-spatial --display-name "I2K Spatial"
   pixi run -e registration python -m ipykernel install --user --name i2k-registration --display-name "I2K Registration"
   ```

4. Start Jupyter from the registration environment:

   ```
   pixi run -e registration jupyter notebook
   ```

5. Open the notebooks from the Jupyter interface in your browser and select the appropriate kernel:

   * `I2K Registration` kernel for `ImageRegistration.ipynb` and `ImageRegistrationHistology.ipynb`
   * `I2K Spatial` kernel for `SpatialData.ipynb`

## Repository contents

| Path                               | Description                                               |
| ---------------------------------- | --------------------------------------------------------- |
| `data/`                            | Course data (download from Zenodo, see above)             |
| `ImageRegistration.ipynb`          | Image registration notebook                               |
| `ImageRegistrationHistology.ipynb` | Image registration notebook (histology)                   |
| `SpatialData.ipynb`                | SpatialData notebook                                      |
| `registration_utils.py`            | Helper functions used by the image registration notebooks |
| `pixi.toml`, `pixi.lock`           | Software environment specification                        |

<!--## Citation

If you use these materials, please cite them as follows:

> SciLifeLab BioImage Informatics Unit (2026). _Integration of multi-modal data and visualization using TissUUmaps 4_ [Course materials]. Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX TODO: replace with Zenodo DOI -->

## License

The contents of this repository are licensed under the [MIT License](LICENSE).

## Acknowledgements

This workshop is conducted by the [SciLifeLab BioImage Informatics Unit](https://www.scilifelab.se/units/bioimage-informatics/) (BIIF) and National Bioinformatics Infrastructure Sweden (NBIS). We thank the organizers of I2KxBINA2026 for hosting the workshop.

## Contact

For questions, please contact [biif@scilifelab.se](mailto:biif@scilifelab.se) or [open an issue](https://github.com/BIIFSweden/I2KWorkshop_2026/issues).
