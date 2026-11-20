# MAS — Materials and mass properties

**CATIA-class equivalent:** Materials library / Measure Inertia / Weight Engineering  
**Autevra workspace:** Breakdown (mass roll-up); Loads (materials)  
**Scope:** Shared  
**Cases:** 108 (Have 100, Partial 0, Gap 8)

Material assignment, density, mass, centre of gravity and inertia with exact references.

[← Back to the index](../README.md)

## Features

- Primitive mass properties — 36 cases (Have)
- Roll-ups and targets — 24 cases (Have)
- Material library — 48 cases (Have)

## Primitive mass properties

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAS-0001 | Box 100×50×20 in steel | Accuracy | P2 | Create, assign the material, measure inertia. | m = 0.785 kg; CG (50,25,10); Ixx(CG) = m(b²+c²)/12 = 189.71 kg·mm². |  |
| MAS-0002 | Cylinder r=25 h=100 in steel | Accuracy | P2 | Measure inertia. | m = 1.5413 kg; Izz = mr²/2 = 481.67; Ixx = m(3r²+h²)/12 = 1525.3 kg·mm². |  |
| MAS-0003 | Sphere r=40 in steel | Accuracy | P2 | Measure inertia. | m = 2.1044 kg; I = 2/5·mr² = 1346.8 kg·mm². |  |
| MAS-0004 | Tube Ø60×2.5×200 in steel | Accuracy | P2 | Measure inertia. | m = 1.3564 kg; Izz = m(ro²+ri²)/2 = 1034.2 kg·mm². |  |
| MAS-0005 | Cone r=30 h=90 in steel | Accuracy | P2 | Measure inertia. | m = 0.66586 kg; CG at h/4 = 22.5 mm from base; Izz = 3/10·mr² = 179.78 kg·mm². |  |
| MAS-0006 | Torus R=60 r=10 in steel | Accuracy | P2 | Measure inertia. | m = 2π²Rr²ρ = 0.92972 kg. |  |
| MAS-0007 | Box 100×50×20 in aluminium | Accuracy | P2 | Create, assign the material, measure inertia. | m = 0.27 kg; CG (50,25,10); Ixx(CG) = m(b²+c²)/12 = 65.25 kg·mm². |  |
| MAS-0008 | Cylinder r=25 h=100 in aluminium | Accuracy | P2 | Measure inertia. | m = 0.53014 kg; Izz = mr²/2 = 165.67; Ixx = m(3r²+h²)/12 = 524.62 kg·mm². |  |
| MAS-0009 | Sphere r=40 in aluminium | Accuracy | P2 | Measure inertia. | m = 0.72382 kg; I = 2/5·mr² = 463.25 kg·mm². |  |
| MAS-0010 | Tube Ø60×2.5×200 in aluminium | Accuracy | P2 | Measure inertia. | m = 0.46653 kg; Izz = m(ro²+ri²)/2 = 355.73 kg·mm². |  |
| MAS-0011 | Cone r=30 h=90 in aluminium | Accuracy | P2 | Measure inertia. | m = 0.22902 kg; CG at h/4 = 22.5 mm from base; Izz = 3/10·mr² = 61.836 kg·mm². |  |
| MAS-0012 | Torus R=60 r=10 in aluminium | Accuracy | P2 | Measure inertia. | m = 2π²Rr²ρ = 0.31978 kg. |  |
| MAS-0013 | Box 100×50×20 in titanium | Accuracy | P2 | Create, assign the material, measure inertia. | m = 0.443 kg; CG (50,25,10); Ixx(CG) = m(b²+c²)/12 = 107.06 kg·mm². |  |
| MAS-0014 | Cylinder r=25 h=100 in titanium | Accuracy | P2 | Measure inertia. | m = 0.86983 kg; Izz = mr²/2 = 271.82; Ixx = m(3r²+h²)/12 = 860.77 kg·mm². |  |
| MAS-0015 | Sphere r=40 in titanium | Accuracy | P2 | Measure inertia. | m = 1.1876 kg; I = 2/5·mr² = 760.07 kg·mm². |  |
| MAS-0016 | Tube Ø60×2.5×200 in titanium | Accuracy | P2 | Measure inertia. | m = 0.76545 kg; Izz = m(ro²+ri²)/2 = 583.65 kg·mm². |  |
| MAS-0017 | Cone r=30 h=90 in titanium | Accuracy | P2 | Measure inertia. | m = 0.37577 kg; CG at h/4 = 22.5 mm from base; Izz = 3/10·mr² = 101.46 kg·mm². |  |
| MAS-0018 | Torus R=60 r=10 in titanium | Accuracy | P2 | Measure inertia. | m = 2π²Rr²ρ = 0.52467 kg. |  |
| MAS-0019 | Box 100×50×20 in CFRP | Accuracy | P2 | Create, assign the material, measure inertia. | m = 0.155 kg; CG (50,25,10); Ixx(CG) = m(b²+c²)/12 = 37.458 kg·mm². |  |
| MAS-0020 | Cylinder r=25 h=100 in CFRP | Accuracy | P2 | Measure inertia. | m = 0.30434 kg; Izz = mr²/2 = 95.107; Ixx = m(3r²+h²)/12 = 301.17 kg·mm². |  |
| MAS-0021 | Sphere r=40 in CFRP | Accuracy | P2 | Measure inertia. | m = 0.41553 kg; I = 2/5·mr² = 265.94 kg·mm². |  |
| MAS-0022 | Tube Ø60×2.5×200 in CFRP | Accuracy | P2 | Measure inertia. | m = 0.26782 kg; Izz = m(ro²+ri²)/2 = 204.21 kg·mm². |  |
| MAS-0023 | Cone r=30 h=90 in CFRP | Accuracy | P2 | Measure inertia. | m = 0.13148 kg; CG at h/4 = 22.5 mm from base; Izz = 3/10·mr² = 35.498 kg·mm². |  |
| MAS-0024 | Torus R=60 r=10 in CFRP | Accuracy | P2 | Measure inertia. | m = 2π²Rr²ρ = 0.18357 kg. |  |
| MAS-0025 | Box 100×50×20 in ABS | Accuracy | P2 | Create, assign the material, measure inertia. | m = 0.105 kg; CG (50,25,10); Ixx(CG) = m(b²+c²)/12 = 25.375 kg·mm². |  |
| MAS-0026 | Cylinder r=25 h=100 in ABS | Accuracy | P2 | Measure inertia. | m = 0.20617 kg; Izz = mr²/2 = 64.427; Ixx = m(3r²+h²)/12 = 204.02 kg·mm². |  |
| MAS-0027 | Sphere r=40 in ABS | Accuracy | P2 | Measure inertia. | m = 0.28149 kg; I = 2/5·mr² = 180.15 kg·mm². |  |
| MAS-0028 | Tube Ø60×2.5×200 in ABS | Accuracy | P2 | Measure inertia. | m = 0.18143 kg; Izz = m(ro²+ri²)/2 = 138.34 kg·mm². |  |
| MAS-0029 | Cone r=30 h=90 in ABS | Accuracy | P2 | Measure inertia. | m = 0.089064 kg; CG at h/4 = 22.5 mm from base; Izz = 3/10·mr² = 24.047 kg·mm². |  |
| MAS-0030 | Torus R=60 r=10 in ABS | Accuracy | P2 | Measure inertia. | m = 2π²Rr²ρ = 0.12436 kg. |  |
| MAS-0031 | Box 100×50×20 in magnesium AZ91 | Accuracy | P2 | Create, assign the material, measure inertia. | m = 0.181 kg; CG (50,25,10); Ixx(CG) = m(b²+c²)/12 = 43.742 kg·mm². |  |
| MAS-0032 | Cylinder r=25 h=100 in magnesium AZ91 | Accuracy | P2 | Measure inertia. | m = 0.35539 kg; Izz = mr²/2 = 111.06; Ixx = m(3r²+h²)/12 = 351.69 kg·mm². |  |
| MAS-0033 | Sphere r=40 in magnesium AZ91 | Accuracy | P2 | Measure inertia. | m = 0.48523 kg; I = 2/5·mr² = 310.55 kg·mm². |  |
| MAS-0034 | Tube Ø60×2.5×200 in magnesium AZ91 | Accuracy | P2 | Measure inertia. | m = 0.31275 kg; Izz = m(ro²+ri²)/2 = 238.47 kg·mm². |  |
| MAS-0035 | Cone r=30 h=90 in magnesium AZ91 | Accuracy | P2 | Measure inertia. | m = 0.15353 kg; CG at h/4 = 22.5 mm from base; Izz = 3/10·mr² = 41.453 kg·mm². |  |
| MAS-0036 | Torus R=60 r=10 in magnesium AZ91 | Accuracy | P2 | Measure inertia. | m = 2π²Rr²ρ = 0.21437 kg. |  |

## Roll-ups and targets

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAS-0037 | mass sum at part level | Accuracy | P2 | Compute the mass sum at part level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0038 | CG combination at part level | Accuracy | P2 | Compute the CG combination at part level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0039 | inertia via parallel axis at part level | Accuracy | P2 | Compute the inertia via parallel axis at part level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0040 | mass target vs actual at part level | Accuracy | P2 | Compute the mass target vs actual at part level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0041 | maturity-weighted estimate (estimated/calculated/weighed) at part level | Accuracy | P2 | Compute the maturity-weighted estimate (estimated/calculated/weighed) at part level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0042 | configuration variant delta at part level | Accuracy | P2 | Compute the configuration variant delta at part level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0043 | mass sum at sub-system level | Accuracy | P2 | Compute the mass sum at sub-system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0044 | CG combination at sub-system level | Accuracy | P2 | Compute the CG combination at sub-system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0045 | inertia via parallel axis at sub-system level | Accuracy | P2 | Compute the inertia via parallel axis at sub-system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0046 | mass target vs actual at sub-system level | Accuracy | P2 | Compute the mass target vs actual at sub-system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0047 | maturity-weighted estimate (estimated/calculated/weighed) at sub-system level | Accuracy | P2 | Compute the maturity-weighted estimate (estimated/calculated/weighed) at sub-system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0048 | configuration variant delta at sub-system level | Accuracy | P2 | Compute the configuration variant delta at sub-system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0049 | mass sum at system level | Accuracy | P2 | Compute the mass sum at system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0050 | CG combination at system level | Accuracy | P2 | Compute the CG combination at system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0051 | inertia via parallel axis at system level | Accuracy | P2 | Compute the inertia via parallel axis at system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0052 | mass target vs actual at system level | Accuracy | P2 | Compute the mass target vs actual at system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0053 | maturity-weighted estimate (estimated/calculated/weighed) at system level | Accuracy | P2 | Compute the maturity-weighted estimate (estimated/calculated/weighed) at system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0054 | configuration variant delta at system level | Accuracy | P2 | Compute the configuration variant delta at system level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0055 | mass sum at product level | Accuracy | P2 | Compute the mass sum at product level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0056 | CG combination at product level | Accuracy | P2 | Compute the CG combination at product level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0057 | inertia via parallel axis at product level | Accuracy | P2 | Compute the inertia via parallel axis at product level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0058 | mass target vs actual at product level | Accuracy | P2 | Compute the mass target vs actual at product level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0059 | maturity-weighted estimate (estimated/calculated/weighed) at product level | Accuracy | P2 | Compute the maturity-weighted estimate (estimated/calculated/weighed) at product level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |
| MAS-0060 | configuration variant delta at product level | Accuracy | P2 | Compute the configuration variant delta at product level. | Equals the hand roll-up of the children (Σm, Σm·x/Σm, Steiner) within 1e-9 rel. |  |

## Material library

Status in Autevra: **Have**

| ID | Test case | Type | Pri | Steps | Expected result | Data / reference |
|---|---|---|---|---|---|---|
| MAS-0061 | Material density: read | Functional | P2 | read the density of a material. | Value consistent everywhere it is used. |  |
| MAS-0062 | Material density: edit (user library) | Functional | P2 | edit (user library) the density of a material. | Value consistent everywhere it is used. |  |
| MAS-0063 | Material density: units display | Functional | P2 | units display the density of a material. | Value consistent everywhere it is used. |  |
| MAS-0064 | Material density: used by FEA/LCA | Functional | P2 | used by FEA/LCA the density of a material. | Value consistent everywhere it is used. |  |
| MAS-0065 | Material Young's modulus: read | Functional | P2 | read the Young's modulus of a material. | Value consistent everywhere it is used. |  |
| MAS-0066 | Material Young's modulus: edit (user library) | Functional | P2 | edit (user library) the Young's modulus of a material. | Value consistent everywhere it is used. |  |
| MAS-0067 | Material Young's modulus: units display | Functional | P2 | units display the Young's modulus of a material. | Value consistent everywhere it is used. |  |
| MAS-0068 | Material Young's modulus: used by FEA/LCA | Functional | P2 | used by FEA/LCA the Young's modulus of a material. | Value consistent everywhere it is used. |  |
| MAS-0069 | Material Poisson's ratio: read | Functional | P2 | read the Poisson's ratio of a material. | Value consistent everywhere it is used. |  |
| MAS-0070 | Material Poisson's ratio: edit (user library) | Functional | P2 | edit (user library) the Poisson's ratio of a material. | Value consistent everywhere it is used. |  |
| MAS-0071 | Material Poisson's ratio: units display | Functional | P2 | units display the Poisson's ratio of a material. | Value consistent everywhere it is used. |  |
| MAS-0072 | Material Poisson's ratio: used by FEA/LCA | Functional | P2 | used by FEA/LCA the Poisson's ratio of a material. | Value consistent everywhere it is used. |  |
| MAS-0073 | Material yield strength: read | Functional | P2 | read the yield strength of a material. | Value consistent everywhere it is used. |  |
| MAS-0074 | Material yield strength: edit (user library) | Functional | P2 | edit (user library) the yield strength of a material. | Value consistent everywhere it is used. |  |
| MAS-0075 | Material yield strength: units display | Functional | P2 | units display the yield strength of a material. | Value consistent everywhere it is used. |  |
| MAS-0076 | Material yield strength: used by FEA/LCA | Functional | P2 | used by FEA/LCA the yield strength of a material. | Value consistent everywhere it is used. |  |
| MAS-0077 | Material UTS: read | Functional | P2 | read the UTS of a material. | Value consistent everywhere it is used. |  |
| MAS-0078 | Material UTS: edit (user library) | Functional | P2 | edit (user library) the UTS of a material. | Value consistent everywhere it is used. |  |
| MAS-0079 | Material UTS: units display | Functional | P2 | units display the UTS of a material. | Value consistent everywhere it is used. |  |
| MAS-0080 | Material UTS: used by FEA/LCA | Functional | P2 | used by FEA/LCA the UTS of a material. | Value consistent everywhere it is used. |  |
| MAS-0081 | Material thermal expansion: read | Functional | P2 | read the thermal expansion of a material. | Value consistent everywhere it is used. |  |
| MAS-0082 | Material thermal expansion: edit (user library) | Functional | P2 | edit (user library) the thermal expansion of a material. | Value consistent everywhere it is used. |  |
| MAS-0083 | Material thermal expansion: units display | Functional | P2 | units display the thermal expansion of a material. | Value consistent everywhere it is used. |  |
| MAS-0084 | Material thermal expansion: used by FEA/LCA | Functional | P2 | used by FEA/LCA the thermal expansion of a material. | Value consistent everywhere it is used. |  |
| MAS-0085 | Material conductivity: read | Functional | P2 | read the conductivity of a material. | Value consistent everywhere it is used. |  |
| MAS-0086 | Material conductivity: edit (user library) | Functional | P2 | edit (user library) the conductivity of a material. | Value consistent everywhere it is used. |  |
| MAS-0087 | Material conductivity: units display | Functional | P2 | units display the conductivity of a material. | Value consistent everywhere it is used. |  |
| MAS-0088 | Material conductivity: used by FEA/LCA | Functional | P2 | used by FEA/LCA the conductivity of a material. | Value consistent everywhere it is used. |  |
| MAS-0089 | Material cost per kg: read | Functional | P2 | read the cost per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0090 | Material cost per kg: edit (user library) | Functional | P2 | edit (user library) the cost per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0091 | Material cost per kg: units display | Functional | P2 | units display the cost per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0092 | Material cost per kg: used by FEA/LCA | Functional | P2 | used by FEA/LCA the cost per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0093 | Material CO2e per kg: read | Functional | P2 | read the CO2e per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0094 | Material CO2e per kg: edit (user library) | Functional | P2 | edit (user library) the CO2e per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0095 | Material CO2e per kg: units display | Functional | P2 | units display the CO2e per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0096 | Material CO2e per kg: used by FEA/LCA | Functional | P2 | used by FEA/LCA the CO2e per kg of a material. | Value consistent everywhere it is used. |  |
| MAS-0097 | Material recyclability: read | Functional | P2 | read the recyclability of a material. | Value consistent everywhere it is used. |  |
| MAS-0098 | Material recyclability: edit (user library) | Functional | P2 | edit (user library) the recyclability of a material. | Value consistent everywhere it is used. |  |
| MAS-0099 | Material recyclability: units display | Functional | P2 | units display the recyclability of a material. | Value consistent everywhere it is used. |  |
| MAS-0100 | Material recyclability: used by FEA/LCA | Functional | P2 | used by FEA/LCA the recyclability of a material. | Value consistent everywhere it is used. |  |
| MAS-0101 | Material fatigue S-N curve: read | Functional | P2 | read the fatigue S-N curve of a material. | Value consistent everywhere it is used. |  |
| MAS-0102 | Material fatigue S-N curve: edit (user library) | Functional | P2 | edit (user library) the fatigue S-N curve of a material. | Value consistent everywhere it is used. |  |
| MAS-0103 | Material fatigue S-N curve: units display | Functional | P2 | units display the fatigue S-N curve of a material. | Value consistent everywhere it is used. |  |
| MAS-0104 | Material fatigue S-N curve: used by FEA/LCA | Functional | P2 | used by FEA/LCA the fatigue S-N curve of a material. | Value consistent everywhere it is used. |  |
| MAS-0105 | Material anisotropic stiffness: read | Functional | P2 | read the anisotropic stiffness of a material. | Value consistent everywhere it is used. |  |
| MAS-0106 | Material anisotropic stiffness: edit (user library) | Functional | P2 | edit (user library) the anisotropic stiffness of a material. | Value consistent everywhere it is used. |  |
| MAS-0107 | Material anisotropic stiffness: units display | Functional | P2 | units display the anisotropic stiffness of a material. | Value consistent everywhere it is used. |  |
| MAS-0108 | Material anisotropic stiffness: used by FEA/LCA | Functional | P2 | used by FEA/LCA the anisotropic stiffness of a material. | Value consistent everywhere it is used. |  |
