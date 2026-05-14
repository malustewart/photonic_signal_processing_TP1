from collections import namedtuple
import json
from lumjson import LumDecoder
import numpy as np
import matplotlib.pyplot as plt

GuidedMode = namedtuple("GuidedMode",["wg_width", "neff", "ng"])

filename = "out/wg_width_sweep.json"
outdir = "./out/"

with open(filename) as f:
   data = json.load(f, cls=LumDecoder)

neff = data["neff"]
ng = data["ng"]
te_fraction = data["te_fraction"]
materials = [m["material"] for m in data["material_sweep"]]
heights = [m["wg_H"] for m in data["material_sweep"]]
widths = np.squeeze(data["wg_width_sweep"]) / 1e-6 # convert from m to um

_, n_widths, n_modes = neff.shape

for i, (m, h, n, g, f) in enumerate(zip(materials, heights, neff, ng, te_fraction)):   #loop through materials
    te_mask = f > 0.5
    neff_mask = n > 1.444

    n_guided_modes = np.count_nonzero(neff_mask,axis=1)

    n_guided_te = np.where(te_mask & neff_mask, n, 0)
    n_guided_tm = np.where(~te_mask & neff_mask, n, 0)

    ng_guided_te = np.where(te_mask & neff_mask, g, 0)
    ng_guided_tm = np.where(~te_mask & neff_mask, g, 0)



    te_modes = [GuidedMode([],[],[]) for _ in range(n_modes)]
    tm_modes = [GuidedMode([],[],[]) for _ in range(n_modes)]
    for w, n_guided_te_for_width, n_guided_tm_for_width, ng_guided_te_for_width, ng_guided_tm_for_width in zip(widths, n_guided_te, n_guided_tm, ng_guided_te, ng_guided_tm):   #loop through widths
        #te
        mask = np.abs(n_guided_te_for_width) > 1e-10
        n_guided_te_for_width = n_guided_te_for_width[mask]
        ng_guided_te_for_width = ng_guided_te_for_width[mask]
        for j, (n_guided_te_for_width_for_mode, ng_guided_te_for_width_for_mode) in enumerate(zip(n_guided_te_for_width, ng_guided_te_for_width)): #loop through te modes
            te_modes[j].wg_width.append(w)
            te_modes[j].neff.append(n_guided_te_for_width_for_mode)
            te_modes[j].ng.append(ng_guided_te_for_width_for_mode)
        
        #tm
        mask = np.abs(n_guided_tm_for_width) > 1e-10
        n_guided_tm_for_width = n_guided_tm_for_width[mask]
        ng_guided_tm_for_width = ng_guided_tm_for_width[mask]
        for j, (n_guided_tm_for_width_for_mode, ng_guided_tm_for_width_for_mode) in enumerate(zip(n_guided_tm_for_width, ng_guided_tm_for_width)):  #loop through tm modes
            tm_modes[j].wg_width.append(w)
            tm_modes[j].neff.append(n_guided_tm_for_width_for_mode)
            tm_modes[j].ng.append(ng_guided_tm_for_width_for_mode)
        
    plt.figure()

    for j, mode in enumerate(te_modes):
        if mode.wg_width:   # si no esta vacio el modo
            plt.plot(
                mode.wg_width,
                mode.neff,
                linestyle="-",
                # marker="o",
                label=f"TE{j}"
            )

    for j, mode in enumerate(tm_modes):
        if mode.wg_width:   # si no esta vacio el modo
            plt.plot(
                mode.wg_width,
                mode.neff,
                linestyle="--",
                # marker="s",
                label=f"TM{j}"
            )
    plt.title(f"n_eff vs. wg width ({m})")
    plt.xlabel("Waveguide width [um]")
    plt.ylabel("neff")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{outdir}/material_{i}_neff_vs_width.png")

    plt.figure()
    plt.scatter(widths, n_guided_modes)
    plt.title(f"# guided modes vs. wg width ({m})")
    plt.xlabel("Waveguide width [um]")
    plt.ylabel("# of guided modes")
    plt.axhline(1)
    plt.grid(True)
    plt.ylim(-0.2,11)
    plt.savefig(f"{outdir}/material_{i}_num_guided_modes_vs_width.png")


    with open(f"{outdir}/material_{i}_neff_ng_vs_width_TE0_TM0.txt", "w") as f:
        print(f"=========", file=f)
        print(f"material: {m}", file=f)
        print(f"=========", file=f)
        print(f"TE0", file=f)
        print(f"=========", file=f)
        print(f"{'width[um]':>10} {'neff':>10} {'ng':>10}", file=f)

        for wg_width, neffs, ngs in zip(*te_modes[0]):
            print(f"{wg_width:>10.2} {neffs:>10.4} {ngs:>10.4}", file=f)
        
        print(f"=========", file=f)
        print(f"TM0", file=f)
        print(f"=========", file=f)
        print(f"{'width[um]':>10} {'neff':>10} {'ng':>10}", file=f)

        for wg_width, neffs, ngs in zip(*tm_modes[0]):
            print(f"{wg_width:>10.2f} {neffs:>10.4f} {ngs:>10.4f}", file=f)



