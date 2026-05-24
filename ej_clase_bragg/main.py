import numpy as np
import matplotlib.pyplot as plt
# import re
import numpy as np
import sys
from pathlib import Path

# ============================================
# INPUT DATA
# ============================================

if len(sys.argv) == 1:
    print(f"Usage: python {Path(sys.argv[0]).name} results_material_1.txt [results_material_1.txt [...]]")
    exit

for filename in sys.argv[1:]:
    widths_te = []
    neff_real_te = []

    widths_tm = []
    neff_real_tm = []

    widths = widths_te
    neff_real = neff_real_te

    with open(filename, "r") as f:
        for line in f:

            # Remove leading/trailing spaces
            line = line.strip()

            # Skip empty/header lines
            if (
                not line
                or "material" in line
                or "width" in line
                or "=" in line
            ):
                continue

            if "TE0" in line:
                widths = widths_te
                neff_real = neff_real_te
                continue

            if "TM0" in line:
                widths = widths_tm
                neff_real = neff_real_tm
                continue

            # Split columns
            parts = line.split()

            # First column
            width = float(parts[0])

            # Second column: complex number like
            # (1.447+1.269e-10j)
            neff_complex = complex(parts[1].strip("()"))

            widths.append(width)
            neff_real.append(neff_complex.real)

    plt.figure(figsize=(7,5))

    for widths, neff_real, mode in zip([widths_te, widths_tm], [neff_real_te, neff_real_tm], ["TE0", "TM0"]):
        # Convert to numpy arrays
        w = np.array(widths)
        n = np.array(neff_real)

        w_min = 0.0
        w_max = 0.75

        mask1 = w > w_min
        mask2 = w < w_max

        w = w[mask1 & mask2]
        n = n[mask1 & mask2]

        l = len(w)

        # Reference frequency
        w0 = w[l//2]
        n0 = n[l//2]

        # ============================================
        # BUILD FIT MATRIX
        # ============================================

        x = w - w0
        y = n - n0


        # Model:
        # y(w) = b1*x + b2*x^2 + b3*x^3

        A = np.column_stack([
            x,
            x**2,
            x**3
        ])

        # ============================================
        # LEAST-SQUARES FIT
        # ============================================

        b1, b2, b3 = np.linalg.lstsq(A, y, rcond=None)[0]

        print(f"Fit coefficients ({mode}):")
        print(f"b1 = {b1:.6e}")
        print(f"b2 = {b2:.6e}")
        print(f"b3 = {b3:.6e}")

        # ============================================
        # FITTED CURVE
        # ============================================

        n_fit = (
            n0 
            + b1 * x
            + b2 * x**2
            + b3 * x**3
        )

        # ============================================
        # PLOT
        # ============================================

        plt.title(Path(filename).name)

        plt.plot(w, n, label=f"Simulation ({mode})")
        plt.plot(w, n_fit, "--", label="Polynomial fit")

        plt.xlabel("w")
        plt.ylabel("n(w)")
        plt.legend()
        plt.grid(True)

        outfile = Path(filename).with_suffix(".png")
    
    plt.savefig(outfile)

plt.show()