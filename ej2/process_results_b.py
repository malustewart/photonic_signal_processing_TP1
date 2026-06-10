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

coeff_file_neff = []
coeff_file_ng = []

for filename in filenames:
    coeff_file_neff.append(filename)
    coeff_file_ng.append(filename)

    wls_te = []
    neff_real_te = []
    ng_real_te = []

    wls_tm = []
    neff_real_tm = []
    ng_real_tm = []

    wls = wls_te
    neff_real = neff_real_te
    ng_real = ng_real_te

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
                ng_real = ng_real_te
                continue

            if "TM0" in line:
                wls = wls_tm
                neff_real = neff_real_tm
                ng_real = ng_real_tm
                continue

            # Split columns
            parts = line.split()

            # First column
            wl = float(parts[0])

            # Second column: complex number like
            # (1.447+1.269e-10j)
            neff_complex = complex(parts[1].strip("()"))
            ng_complex = complex(parts[2].strip("()"))

            wls.append(wl)
            neff_real.append(neff_complex.real)
            ng_real.append(ng_complex.real)


    for wls, neff_real, ng_real, mode in zip([wls_te, wls_tm], [neff_real_te, neff_real_tm], [ng_real_te, ng_real_tm], ["TE0", "TM0"]):
        # Convert to numpy arrays
        wl = np.array(wls)
        n = np.array(neff_real)
        ng = np.array(ng_real)


        l = len(wl)

        # Reference frequency
        wl0 = wl[l//2]
        n0 = n[l//2]
        ng0 = ng[l//2]

        # ============================================
        # BUILD FIT MATRIX
        # ============================================

        x = wl - wl0
        y = n - n0
        y2 = ng - ng0

        max_fit_order = 5
        x_powered = np.array([np.power(x, i) for i in range(max_fit_order)])

        # neff

        plt.figure(figsize=(7,5))

        plt.title(f"{Path(filename).name} - {mode}")
        plt.plot(wl, n, label=f"Simulation", marker='*')


        for fit_order in range(1, max_fit_order):
            A = np.column_stack(x_powered[1:fit_order+1])
            bs = np.linalg.lstsq(A, y, rcond=None)[0]
            n_fit = n0 + np.sum(bs[:, None] * x_powered[1:fit_order+1], axis=0)
            n_fit = np.squeeze(n_fit)
            nmse = ((n - n_fit)**2).mean()/n.mean()

            plt.plot(wl, n_fit, "--", label=f"polyfit (n={fit_order})")

            coeff_file_neff.append(f"Fit coefficients ({mode}) - order {fit_order}:")
            for i, b in enumerate(bs,1):
                coeff_file_neff.append(f"b{i} = {b:.6e}")
            
            coeff_file_neff.append(f"nmse: {nmse}")
            coeff_file_neff.append("")
        
        plt.xlabel("wavelength [um]")
        plt.ylabel("neff")
        plt.grid(True)
        plt.legend()

        outfile = Path(filename).with_suffix(f".{mode}_neff.png")
        plt.savefig(outfile)

        # ng

        plt.figure(figsize=(7,5))

        plt.title(f"{Path(filename).name} - {mode}")
        plt.plot(wl, ng, label=f"Simulation", marker='*')


        for fit_order in range(1, max_fit_order):
            A = np.column_stack(x_powered[1:fit_order+1])
            bs = np.linalg.lstsq(A, y2, rcond=None)[0]
            ng_fit = ng0 + np.sum(bs[:, None] * x_powered[1:fit_order+1], axis=0)
            ng_fit = np.squeeze(ng_fit)
            nmse = ((ng - ng_fit)**2).mean()/ng.mean()

            plt.plot(wl, ng_fit, "--", label=f"polyfit (n={fit_order})")

            coeff_file_ng.append(f"Fit coefficients ({mode}) - order {fit_order}:")
            for i, b in enumerate(bs,1):
                coeff_file_ng.append(f"b{i} = {b:.6e}")
            
            coeff_file_ng.append(f"nmse: {nmse}")
            coeff_file_ng.append("")
        
        plt.xlabel("wavelength [um]")
        plt.ylabel("n_g")
        plt.grid(True)
        plt.legend()

        outfile = Path(filename).with_suffix(f".{mode}_ng.png")
        plt.savefig(outfile)

with open("out/polyfit_coefs_neff.txt", "w") as f:
    f.write("\n".join(coeff_file_neff))

with open("out/polyfit_coefs_ng.txt", "w") as f:
    f.write("\n".join(coeff_file_ng))


plt.show()