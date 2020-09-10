MICM Collection
====================

Storage place for mechanisms, configured mechanisms, and environmental conditions.

[![License](https://img.shields.io/github/license/NCAR/micm-collection.svg)](https://github.com/NCAR/micm-collection/blob/master/LICENSE)

Copyright (C) 2018&ndash;2020 National Center for Atmospheric Research

- Collect Tag from chemistry cafe, **get_tag.py**
- Use web-service preprocessor to convert the tag to Fortran, **preprocess_tag.py**
- Collect Environmental Conditions File from FTP Server, **get_environmental_conditions.py**
- Place environmental conditions and fortran code (corresponding to the tag) in place to be compiled, **stage_tag.py**


## Usage is available for each of these scripts
```
> python3 get_tag.py --help
> python3 preprocess_tag.py --help
> python3 stage_tag.py --help
```

