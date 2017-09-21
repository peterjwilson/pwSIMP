# pwSIMP

pwSIMP is a small dip into gradient-based optimisation using the Solid Isotropic Material with Penalisation (SIMP) method. This approach is implemented in Python, with a basic Tkinter GUI and matlibplot visualisation.

## The SIMP method
A global volume fraction between 0.0 and 1.0 is specified by the user which indicates the proportion of material in the total domain. The optimisation problem is thus:
_Where should this scarce material be allocated within the domain such that structural stiffness is maximised (alternatively, strain energy is minimised)_.

The SIMP method tackles this problem by scaling the Young's modulus (_E_o_) of each element with it's individual volume fraction (_vol_frac_) which is penalised with the global penalty factor (_p_). Mathematically: _E_e = E_0 vol_frac^p_. This penalisation attempts to encourage binary element volume fractions.

The total system strain energy can be determined by summing element strain energies, which, via their constitutive relations, are functions of individual element volume fractions. The system stiffness is optimised by calculating the sensitivity vector of the total system strain energy across each individual element volume fraction.

## Example
An example of a centrally loaded membrane supported at each end is provided:

![](https://github.com/peterjwilson/pwSIMP/blob/master/wiki/bridge_example.png)

## References
1. Sigmund, O. (2001). A 99 line topology optimization code written in Matlab. Structural and multidisciplinary optimization, 21(2), 120-127.
2. Bletzinger, K-U. (2017). Structural optimisation lecture notes, Technical University of Munich.
