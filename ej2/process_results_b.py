import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path

# ============================================
# INPUT DATA
# ============================================

filenames = [
    "out/material_0_neff_ng_vs_wavelength_TE0_TM0.txt",
    "out/material_1_neff_ng_vs_wavelength_TE0_TM0.txt",
]

coeff_file = []

for filename in filenames:
    coeff_file.append(filename)
    wls_te = []
    neff_real_te = []

    wls_tm = []
    neff_real_tm = []

    wls = wls_te
    neff_real = neff_real_te

    with open(filename, "r") as f:
        for line in f:

            # Remove leading/trailing spaces
            line = line.strip()

            # Skip empty/header lines
            if (
                not line
                or "material" in line
                or "wavelength" in line
                or "=" in line
            ):
                continue

            if "TE0" in line:
                wls = wls_te
                neff_real = neff_real_te
                continue

            if "TM0" in line:
                wls = wls_tm
                neff_real = neff_real_tm
                continue

            # Split columns
            parts = line.split()

            # First column
            wl = float(parts[0])

            # Second column: complex number like
            # (1.447+1.269e-10j)
            neff_complex = complex(parts[1].strip("()"))

            wls.append(wl)
            neff_real.append(neff_complex.real)


    for wls, neff_real, mode in zip([wls_te, wls_tm], [neff_real_te, neff_real_tm], ["TE0", "TM0"]):
        # Convert to numpy arrays
        wl = np.array(wls)
        n = np.array(neff_real)

        # w_min = 0.0
        # w_max = 0.75

        # mask1 = wl > w_min
        # mask2 = wl < w_max

        # wl = wl[mask1 & mask2]
        # n = n[mask1 & mask2]

        l = len(wl)

        # Reference frequency
        wl0 = wl[l//2]
        n0 = n[l//2]

        # ============================================
        # BUILD FIT MATRIX
        # ============================================

        x = wl - wl0
        y = n - n0

        max_fit_order = 5
        x_powered = np.array([np.power(x, i) for i in range(max_fit_order)])

        plt.figure(figsize=(7,5))

        plt.title(f"{Path(filename).name} - {mode}")
        plt.plot(wl, n, label=f"Simulation", marker='*')


        for fit_order in range(1, max_fit_order):
            A = np.column_stack(x_powered[1:fit_order+1])
            bs = np.linalg.lstsq(A, y, rcond=None)[0]
            coeff_file.append(f"Fit coefficients - order ({fit_order}) ({mode}):")
            for i, b in enumerate(bs,1):
                coeff_file.append(f"b{i} = {b:.6e}")
            coeff_file.append("")

            n_fit = n0 + np.sum(bs[:, None] * x_powered[1:fit_order+1], axis=0)
            n_fit = np.squeeze(n_fit)

            plt.plot(wl, n_fit, "--", label=f"polyfit (n={fit_order})")
        
        plt.xlabel("wavelength [um]")
        plt.ylabel("n(w)")
        plt.grid(True)
        plt.legend()

        outfile = Path(filename).with_suffix(f".{mode}.png")
        plt.savefig(outfile)

with open("polyfit_coefs.txt", "w") as f:
    f.write("\n".join(coeff_file))

plt.show()