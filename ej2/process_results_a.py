from collections import namedtuple
import json
from lumjson import LumDecoder
import numpy as np
import matplotlib.pyplot as plt

GuidedMode = namedtuple("GuidedMode",["wavelength", "neff", "ng"])

filename = "out/wl_sweep.json"
outdir = "./out/"

with open(filename) as f:
   data = json.load(f, cls=LumDecoder)

neff = data["neff"]
ng = data["ng"]
te_fraction = data["te_fraction"]
materials = [m["material"] for m in data["material_sweep"]]
heights = [m["wg_H"] for m in data["material_sweep"]]
wavelengths = np.squeeze(data["wl_sweep"]) / 1e-6 # convert from m to um

_, n_wavelengths, n_modes = neff.shape

te_modes_by_material = []
tm_modes_by_material = []

#loop through materials
for i, (m, h, n, g, f) in enumerate(zip(materials, heights, neff, ng, te_fraction)):
    te_mask = f > 0.5
    neff_mask = n > 1.444

    # n_guided_modes = np.count_nonzero(neff_mask,axis=1)

    n_guided_te = np.where(te_mask & neff_mask, n, 0)
    n_guided_tm = np.where(~te_mask & neff_mask, n, 0)

    ng_guided_te = np.where(te_mask & neff_mask, g, 0)
    ng_guided_tm = np.where(~te_mask & neff_mask, g, 0)

    te_modes = [GuidedMode([],[],[]) for _ in range(n_modes)]
    tm_modes = [GuidedMode([],[],[]) for _ in range(n_modes)]
    
    # loop through wavelengths
    for wl, n_guided_te_for_wl, n_guided_tm_for_wl, ng_guided_te_for_wl, ng_guided_tm_for_wl in zip(wavelengths, n_guided_te, n_guided_tm, ng_guided_te, ng_guided_tm):
        #te
        mask = np.abs(n_guided_te_for_wl) > 1e-10
        n_guided_te_for_wl = n_guided_te_for_wl[mask]
        ng_guided_te_for_wl = ng_guided_te_for_wl[mask]
        # loop through te modes
        for j, (n_guided_te_for_width_for_mode, ng_guided_te_for_width_for_mode) in enumerate(zip(n_guided_te_for_wl, ng_guided_te_for_wl)):
            te_modes[j].wavelength.append(wl)
            te_modes[j].neff.append(n_guided_te_for_width_for_mode)
            te_modes[j].ng.append(ng_guided_te_for_width_for_mode)
        
        #tm
        mask = np.abs(n_guided_tm_for_wl) > 1e-10
        n_guided_tm_for_wl = n_guided_tm_for_wl[mask]
        ng_guided_tm_for_wl = ng_guided_tm_for_wl[mask]
        # loop through tm modes
        for j, (n_guided_tm_for_width_for_mode, ng_guided_tm_for_width_for_mode) in enumerate(zip(n_guided_tm_for_wl, ng_guided_tm_for_wl)):
            tm_modes[j].wavelength.append(wl)
            tm_modes[j].neff.append(n_guided_tm_for_width_for_mode)
            tm_modes[j].ng.append(ng_guided_tm_for_width_for_mode)

    te_modes_by_material.append(te_modes)
    tm_modes_by_material.append(tm_modes)

    with open(f"{outdir}/material_{i}_neff_ng_vs_wavelength_TE0_TM0.txt", "w") as f:
        print(f"=========", file=f)
        print(f"material: {m}", file=f)
        print(f"=========", file=f)
        print(f"TE0", file=f)
        print(f"=========", file=f)
        print(f"{'wavelength [um]':>10} {'neff':>10} {'ng':>10}", file=f)

        for wl, neffs, ngs in zip(*te_modes[0]):
            print(f"{wl:>10.4} {neffs:>10.6} {ngs:>10.6}", file=f)
        
        print(f"=========", file=f)
        print(f"TM0", file=f)
        print(f"=========", file=f)
        print(f"{'wavelength [um]':>10} {'neff':>10} {'ng':>10}", file=f)

        for wl, neffs, ngs in zip(*tm_modes[0]):
            print(f"{wl:>10.4f} {neffs:>10.6f} {ngs:>10.6f}", file=f)


# plot neff

plt.figure()

for m, te_modes, tm_modes in zip(materials, te_modes_by_material, tm_modes_by_material):
    for j, mode in enumerate(te_modes):
        if mode.wavelength:   # si no esta vacio el modo
            plt.plot(
                mode.wavelength,
                mode.neff,
                linestyle="-",
                marker="o",
                label=f"TE{j} - {m}"
            )

    for j, mode in enumerate(tm_modes):
        if mode.wavelength:   # si no esta vacio el modo
            plt.plot(
                mode.wavelength,
                mode.neff,
                linestyle="--",
                marker="s",
                label=f"TM{j} - {m}"
            )
plt.title(f"n_eff vs. wavelength")
plt.xlabel("Wavelength [um]")
plt.ylabel("neff")
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
plt.grid(True)
plt.savefig(f"{outdir}/neff_vs_wavelength.png", bbox_inches="tight")

# plot ng

plt.figure()

for m, te_modes, tm_modes in zip(materials, te_modes_by_material, tm_modes_by_material):
    for j, mode in enumerate(te_modes):
        if mode.wavelength:   # si no esta vacio el modo
            plt.plot(
                mode.wavelength,
                mode.ng,
                linestyle="-",
                marker="o",
                label=f"TE{j} - {m}"
            )

    for j, mode in enumerate(tm_modes):
        if mode.wavelength:   # si no esta vacio el modo
            plt.plot(
                mode.wavelength,
                mode.ng,
                linestyle="--",
                marker="s",
                label=f"TM{j} - {m}"
            )
plt.title(f"n_g vs. wavelength")
plt.xlabel("Wavelength [um]")
plt.ylabel("ng")
plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.1), ncol=2)
plt.grid(True)
plt.savefig(f"{outdir}/ng_vs_wavelength.png", bbox_inches="tight")



