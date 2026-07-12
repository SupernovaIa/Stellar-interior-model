# Physics

This document describes the physical model implemented in
[`src/star_class.py`](../src/star_class.py) and the equations it integrates.

## 1. The model

We model a massive main-sequence star with mass $M > 2\,M_\odot$. Such stars
have a two-zone interior:

- a **convective core**, where energy is carried by convection and the
  temperature gradient is (approximately) adiabatic, and
- a **radiative envelope**, where energy is carried by radiative diffusion.

The two zones meet at a **transition layer**, whose location is part of the
solution.

### Assumptions

- **Static, hydrostatic structure** — the star does not evolve in time.
- **Fully ionized ideal gas**, with radiation pressure neglected.
- **Uniform chemical composition** ($X$, $Y$, $Z$ constant throughout).
- **Nuclear energy** from the pp chain and the CNO cycle.
- Radiative transport with a **Kramers-type opacity** and adiabatic convection
  in the core.

## 2. Units

The code works in a **scaled CGS** system so that the variables are $O(1)$:

| Quantity | Symbol | Unit |
|----------|--------|------|
| Mass | $M$ | $10^{33}\ \mathrm{g}$ |
| Radius | $r$ | $10^{10}\ \mathrm{cm}$ |
| Luminosity | $L$ | $10^{33}\ \mathrm{erg\,s^{-1}}$ |
| Temperature | $T$ | $10^{7}\ \mathrm{K}$ |
| Pressure | $P$ | $10^{15}\ \mathrm{dyn\,cm^{-2}}$ |

## 3. Composition and equation of state

The metal fraction and mean molecular weight of a fully ionized ideal gas are

$$Z = 1 - X - Y, \qquad \mu = \frac{1}{2X + 0.75\,Y + 0.5\,Z}.$$

The ideal-gas equation of state gives the density

$$\rho = \frac{\mu\,P}{k_B N_A\,T},$$

where $k_B$ is the Boltzmann constant and $N_A$ is Avogadro's number
(`config/config.yaml`).

## 4. Equations of stellar structure

The interior is governed by the four structure equations. In the scaled units
above they take the form (see `radiative_envelope` and `three_layers_core`):

**Mass continuity** ($\mathrm{d}M/\mathrm{d}r = 4\pi r^2 \rho$):

$$\frac{\mathrm{d}M}{\mathrm{d}r} = C_m\,\frac{P\,r^2}{T}, \qquad C_m = 0.01523\,\mu.$$

**Hydrostatic equilibrium** ($\mathrm{d}P/\mathrm{d}r = -G M \rho / r^2$):

$$\frac{\mathrm{d}P}{\mathrm{d}r} = -C_p\,\frac{P\,M}{T\,r^2}, \qquad C_p = 8.084\,\mu.$$

**Energy generation** ($\mathrm{d}L/\mathrm{d}r = 4\pi r^2 \rho\,\varepsilon$).
Using $\rho \propto P/T$ and $\varepsilon \propto \rho\,T^{\nu}$ (Section 6):

$$\frac{\mathrm{d}L}{\mathrm{d}r} = C_l\,P^2\,T^{\nu-2}\,r^2,$$

where $C_l$ and $\nu$ depend on the active nuclear cycle.

**Radiative energy transport** (with a Kramers opacity $\kappa \propto \rho\,T^{-3.5}$):

$$\frac{\mathrm{d}T}{\mathrm{d}r} = -C_{t,\mathrm{rad}}\,\frac{P^2\,L}{T^{8.5}\,r^2}, \qquad C_{t,\mathrm{rad}} = 0.01679\,Z\,(1+X)\,\mu^2.$$

## 5. Convection and the polytropic core

In the convective core energy transport is adiabatic and the temperature
gradient is

$$\frac{\mathrm{d}T}{\mathrm{d}r} = -C_{t,\mathrm{conv}}\,\frac{M}{r^2}, \qquad C_{t,\mathrm{conv}} = 3.234\,\mu.$$

An adiabatic, fully ionized monatomic gas ($\gamma = 5/3$) behaves as a
**polytrope of index $n = 3/2$**, for which pressure and temperature are related
by

$$P = k\,T^{5/2}.$$

The polytropic constant $k$ (`k_polytrope`) is fixed at the transition layer,
$k = P/T^{5/2}$, and reused throughout the core.

### Convection criterion

The boundary between the radiative envelope and the convective core is detected
via the **transport parameter**

$$n + 1 = \frac{T}{P}\,\frac{\mathrm{d}P/\mathrm{d}r}{\mathrm{d}T/\mathrm{d}r}.$$

A layer is convective when $n + 1 < 2.5$. The transition radius is found by
interpolating to $n + 1 = 2.5$ (see `transition_layer_down`).

## 6. Nuclear energy generation

Energy is produced by two temperature-dependent cycles, each modelled with a
piecewise power law $\varepsilon \propto \rho\,T^{\nu}$ (with $T$ in $10^7$ K).

**pp chain** (`pp_chain`):

$$\varepsilon_\mathrm{pp} = \varepsilon_{1,\mathrm{pp}}\,X^2\,\rho\,(10\,T)^{\nu_\mathrm{pp}},$$

with $(\nu_\mathrm{pp}, \varepsilon_{1,\mathrm{pp}})$ tabulated by temperature
range (e.g. $\nu = 5$, $\varepsilon_1 = 10^{-6.04}$ for $0.6 \le T < 0.95$).

**CNO cycle** (`CNO_cycle`):

$$\varepsilon_\mathrm{CNO} = \varepsilon_{1,\mathrm{CNO}}\,X\,\tfrac{Z}{3}\,\rho\,(10\,T)^{\nu_\mathrm{CNO}},$$

again tabulated by temperature range (e.g. $\nu = 18$, $\varepsilon_1 = 10^{-19.8}$
for $1.6 \le T < 2.25$).

At each layer the model uses whichever cycle dominates (`energy_generation_rate`),
and derives the luminosity coefficient

$$C_l = 0.01845\,\varepsilon_1\,f_X\,10^{\nu}\,\mu^2,$$

where $f_X = X^2$ for the pp chain and $f_X = X\,Z/3$ for the CNO cycle.

## 7. Boundary conditions

**Surface** (`three_layers_surface`), assuming a radiative envelope with
$M \approx M_\mathrm{total}$ and $L \approx L_\mathrm{total}$:

$$T = A_1\!\left(\frac{1}{r} - \frac{1}{R_\mathrm{total}}\right), \qquad P = A_2\,T^{4.25},$$

$$A_1 = 1.9022\,\mu\,M_\mathrm{total}, \qquad A_2 = 10.645\,\sqrt{\frac{M_\mathrm{total}}{\mu\,Z\,(1+X)\,L_\mathrm{total}}}.$$

**Center** (`three_layers_core`), expanding the convective, polytropic core near
$r = 0$:

$$T = T_c - 0.008207\,\mu^2\,k\,T_c^{3/2}\,r^2, \qquad P = k\,T^{5/2},$$

$$M = \frac{C_m}{3}\,k\,T_c^{3/2}\,r^3, \qquad L = \frac{C_l}{3}\,k^2\,T_c^{\nu+3}\,r^3,$$

where $T_c$ is the central temperature.

The three unknowns $T_c$, $R_\mathrm{total}$ and $L_\mathrm{total}$ are fixed by
minimizing the mismatch at the transition layer — see
[numerical-method.md](numerical-method.md).
