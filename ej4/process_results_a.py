from collections import namedtuple
import json
from lumjson import LumDecoder
import numpy as np
import matplotlib.pyplot as plt
import os

filename = "./out/y_branch_optimization_profile.json"
outdir = "./out/"

os.makedirs(outdir, exist_ok=True)

with open(filename) as f:
   data = json.load(f, cls=LumDecoder)

# Load data
S_11 = data["S_11"]      # shape: (n_theta, n_lambda)
S_top = data["S_top"]    # S21
S_bot = data["S_bot"]    # S31

lambda_sweep = np.squeeze(data["lambda_sweep"]) / 1e-6  # m -> um
theta_sweep = np.squeeze(data["theta_sweep"])

#################
# PLOT s21, s31 #
#################


import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors

fig, ax = plt.subplots(figsize=(8, 5))

theta_sweep = theta_sweep[:8]

# Colormap based on theta
norm = colors.Normalize(
    vmin=np.min(theta_sweep),
    vmax=np.max(theta_sweep)
)
cmap = cm.jet



for i, theta in enumerate(theta_sweep):

    color = cmap(norm(theta))

    s21_db = 20 * np.log10(np.abs(S_top[i, :]))
    s31_db = 20 * np.log10(np.abs(S_bot[i, :]))

    ax.plot(
        lambda_sweep,
        s21_db,
        color=color,
        linestyle="-",
        linewidth=1.5,
        alpha=0.5,
        label = r"$\theta$" + f"={theta:.1f}°"
    )

    ax.plot(
        lambda_sweep,
        s31_db,
        color=color,
        linestyle="--",
        linewidth=1.5,
    )

# Dummy lines for legend
ax.plot([], [], "k-",alpha=0.5, label="S21")
ax.plot([], [], "k--", label="S31")

ax.set_xlabel("Wavelength (µm)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("S21 and S31 vs Wavelength")
ax.minorticks_on()
ax.grid(True, which="major")
ax.grid(True, which="minor", alpha=0.25)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=5
)

fig.subplots_adjust(bottom=0.2)

plt.tight_layout()
plt.savefig(
    os.path.join(outdir, "S21_S31_vs_wavelength.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.close()

###########
# PLOT IL #
###########

fig, ax = plt.subplots(figsize=(8, 5))

for i, theta in enumerate(theta_sweep):

    color = cmap(norm(theta))

    il_db = -10 * np.log10(
        np.abs(S_top[i, :])**2 +
        np.abs(S_bot[i, :])**2
    )

    ax.plot(
        lambda_sweep,
        il_db,
        color=color,
        linewidth=1.5,
        label = r"$\theta$" + f"={theta:.1f}°"
    )

sm = cm.ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

# cbar = plt.colorbar(sm, ax=ax)
# cbar.set_label(r"$\theta$°")

ax.set_xlabel("Wavelength (µm)")
ax.set_ylabel("Insertion Loss (dB)")
ax.set_title("Insertion Loss vs Wavelength")
ax.minorticks_on()
ax.grid(True, which="major")
ax.grid(True, which="minor", alpha=0.25)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=4
)

fig.subplots_adjust(bottom=0.2)

plt.tight_layout()
plt.savefig(
    os.path.join(outdir, "IL_vs_wavelength.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.close()

############
# PLOT s11 #
############

fig, ax = plt.subplots(figsize=(8, 5))

for i, theta in enumerate(theta_sweep):

    color = cmap(norm(theta))

    s11_db = 20 * np.log10(np.abs(S_11[i, :]))

    ax.plot(
        lambda_sweep,
        s11_db,
        color=color,
        linestyle="-",
        linewidth=1.5,
        label = r"$\theta$" + f"={theta:.1f}°"
    )

ax.set_xlabel("Wavelength (µm)")
ax.set_ylabel("Magnitude (dB)")
ax.set_title("S11 vs Wavelength")
ax.minorticks_on()
ax.grid(True, which="major")
ax.grid(True, which="minor", alpha=0.25)
ax.legend(
    loc="upper center",
    bbox_to_anchor=(0.5, -0.15),
    ncol=5
)

fig.subplots_adjust(bottom=0.2)

plt.tight_layout()
plt.savefig(
    os.path.join(outdir, "S11_vs_wavelength.png"),
    dpi=300,
    bbox_inches="tight"
)
plt.close()