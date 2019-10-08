QCPortal
==============================
[//]: # (Badges)
[![Travis Build Status](https://api.travis-ci.org/MolSSI/QCPortal.png)](https://travis-ci.org/MolSSI/QCPortal)

A client interface to the QC Archive Project.

This standalone client serves to hook into QCFractal instances from remote or local 
locations and is designed for end-users who which to access the QCFractal stores.

The main source code for this project is automatically ported over from the 
[QCFractal](https://github.com/molssi/qcfractal) automatically. Issues involving 
the source code itself (anything in the `qcfractal` directory) should raise an issue 
on the [QCFractal issue tracker](https://github.com/MolSSI/QCFractal/issues/new/choose) 
for the `interface`. Issues about the documentation, repository structure, or deployment 
of the standalone QCPortal can be raised on this repository. 

### QCPortal Version descriptions with QCFractal

QCPortal's release versions mostly match QCFractal's releases with the following standard form

```X.Y.Z```

for Major (X), Minor(Y), and Patch(Z) version respectively. However, because Portal is intrinsicly linked to
Fractal, the following rules must be adhered to:
1. Major release version **must** be the same as Fractal
2. Minor release version **must** be the same as Fractal
3. Patch version is unrestricted and can differ from Fractal

### Copyright

Copyright (c) 2018-2019, Molecular Software Sciences Institute (MolSSI)  


#### Acknowledgements
 
Project based on the 
[Computational Chemistry Python Cookiecutter](https://github.com/choderalab/cookiecutter-python-comp-chem)

