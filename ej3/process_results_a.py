from collections import namedtuple
import json
from lumjson import LumDecoder
import numpy as np
import matplotlib.pyplot as plt

GuidedMode = namedtuple("GuidedMode",["radius", "loss_mm", "loss_pr"])

filename = "./out/radius_sweep.json"
outdir = "./out/"

with open(filename) as f:
   data = json.load(f, cls=LumDecoder)

neff = data["neff"]
ng = data["ng"]
te_fraction = data["te_fraction"]
losses_mm = data['loss_mode_mismatch']
losses_pr = data['loss_propagation']
materials = [m["material"] for m in data["material_sweep"]]
heights = [m["wg_H"] for m in data["material_sweep"]]
radii = np.squeeze(data["radius_sweep"]) / 1e-6 # convert from m to um

_, n_radii, n_modes = neff.shape

te_modes_by_material = []
tm_modes_by_material = []

#loop through materials
for i, (m, h, n, loss_mm, loss_pr, f) in enumerate(zip(materials, heights, neff, losses_mm, losses_pr, te_fraction)):
    te_mask = f > 0.5
    neff_mask = n > 1.444

    # n_guided_modes = np.count_nonzero(neff_mask,axis=1)

    n_guided_te = np.where(te_mask & neff_mask, n, 0)
    # n_guided_tm = np.where(~te_mask & neff_mask, n, 0)

    loss_mm_guided_te = np.where(te_mask & neff_mask, loss_mm, 0)
    # loss_mm_guided_tm = np.where(~te_mask & neff_mask, loss_mm, 0)

    loss_pr_guided_te = np.where(te_mask & neff_mask, loss_pr, 0)
    # loss_pr_guided_tm = np.where(~te_mask & neff_mask, loss_pr, 0)

    te_modes = [GuidedMode([],[],[]) for _ in range(n_modes)]
    # tm_modes = [GuidedMode([],[],[]) for _ in range(n_modes)]
    
    # loop through radii
    for radius, n_guided_te_for_radius, loss_mm_guided_te_for_radius, loss_pr_guided_te_for_radius in zip(radii, n_guided_te, loss_mm_guided_te, loss_pr_guided_te):
        #te
        mask = np.abs(n_guided_te_for_radius) > 1e-10
        loss_mm_guided_te_for_radius = loss_mm_guided_te_for_radius[mask]
        loss_pr_guided_te_for_radius = loss_pr_guided_te_for_radius[mask]
        # loop through te modes
        for j, (loss_mm_guided_te_for_radius_for_mode, loss_pr_guided_te_for_radius_for_mode) in enumerate(zip(loss_mm_guided_te_for_radius, loss_pr_guided_te_for_radius)):
            te_modes[j].radius.append(radius)
            te_modes[j].loss_mm.append(loss_mm_guided_te_for_radius_for_mode)
            te_modes[j].loss_pr.append(loss_pr_guided_te_for_radius_for_mode)
        
        # #tm
        # mask = np.abs(n_guided_tm_for_radius) > 1e-10
        # n_guided_tm_for_radius = n_guided_tm_for_radius[mask]
        # ng_guided_tm_for_radius = ng_guided_tm_for_radius[mask]
        # # loop through tm modes
        # for j, (n_guided_tm_for_width_for_mode, ng_guided_tm_for_width_for_mode) in enumerate(zip(n_guided_tm_for_radius, ng_guided_tm_for_radius)):
        #     tm_modes[j].radius.append(radius)
        #     tm_modes[j].neff.append(n_guided_tm_for_width_for_mode)
        #     tm_modes[j].ng.append(ng_guided_tm_for_width_for_mode)

    te_modes_by_material.append(te_modes)
    # tm_modes_by_material.append(tm_modes)

    with open(f"{outdir}/material_{i}_loss_vs_radius_TE0.txt", "w") as f:
        print(f"=========", file=f)
        print(f"material: {m}", file=f)
        print(f"=========", file=f)
        print(f"TE0", file=f)
        print(f"=========", file=f)
        print(f"{'radius [um]':>10} {'loss_mm [dB]':>10} {'loss_pr [dB]':>10}", file=f)

        for radius, neffs, ngs in zip(*te_modes[0]):
            print(f"{radius:>10.4} {neffs:>10.6} {ngs:>10.6}", file=f)
        
        # print(f"=========", file=f)
        # print(f"TM0", file=f)
        # print(f"=========", file=f)
        # print(f"{'radius [um]':>10} {'neff':>10} {'ng':>10}", file=f)

        # for radius, neffs, ngs in zip(*tm_modes[0]):
        #     print(f"{radius:>10.4f} {neffs:>10.6f} {ngs:>10.6f}", file=f)


# plot losses

for i, (m, te_modes) in enumerate(zip(materials, te_modes_by_material)):
    plt.figure()
    for j, mode in enumerate(te_modes):
        if mode.radius:   # si no esta vacio el modo
            loss_mm = 2 * np.array(mode.loss_mm)    # 1 vez por entrar a la curva y 1 vez por salir
            loss_pr = np.array(mode.loss_pr)
            plt.semilogx(
                mode.radius,
                loss_mm + loss_pr,
                linestyle="-",
                marker="o",
                label=f"TE{j} - Total loss"
            )
            plt.semilogx(
                mode.radius,
                loss_mm,
                linestyle=":",
                marker="o",
                label=f"TE{j} - Mode mismatch loss"
            )
            plt.semilogx(
                mode.radius,
                loss_pr,
                linestyle=":",
                marker="o",
                label=f"TE{j} - Scattering loss"
            )
            opt_radius_i = np.argmin(loss_mm + loss_pr)
            opt_radius = mode.radius[opt_radius_i]
            plt.axvline(opt_radius)

    plt.xlim((3,130))
    # for j, mode in enumerate(tm_modes):
    #     if mode.radius:   # si no esta vacio el modo
    #         plt.plot(
    #             mode.radius,
    #             mode.neff,
    #             linestyle="--",
    #             marker="s",
    #             label=f"TM{j} - {m}"
    #         )

    plt.title(f"Losses vs. radius (90°) - {m}")
    plt.xlabel("Radius [um]")
    plt.ylabel("Loss [dB]")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=2)
    plt.grid(True)
    plt.savefig(f"{outdir}/material_{i}_loss_vs_radius.png", bbox_inches="tight")
