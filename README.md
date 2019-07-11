# burrito.py
Collect Tag from chemistry cafe, Use MechanismToCode to convert to Fortran and place in MICM_chemistry

The Chemistry Cafe is a (web) database of reactions and mechanisms, including versioning. 
MechanismToCode is a web service converting mechanisms into differential equations and a sparse solver
burrito.py 
- orders from the Cafe using a mechanism tag number.
- submits that json representation of the mechanism to the MechanismToCode
- places the data in the appropriate place in MICM_chemistry and MusicBox
