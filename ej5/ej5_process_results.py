from collections import namedtuple
import json
from lumjson import LumDecoder
import numpy as np
import matplotlib.pyplot as plt


# filename = "ej5/out/untitled.json"
# outdir = ".ej5/out/"

# with open(filename) as f:
#    data = json.load(f, cls=LumDecoder)

# result = data['result']

# print(result[0,90,10:20,0])

# plt.figure()
# plt.title("3era dimension")
# plt.plot(result[0,90,:,0])
# plt.show()

# filename = "./out/untitled.json"
filename = "./out/gap_sweep.json"
outdir = "./out/"

with open(filename) as f:
   data = json.load(f, cls=LumDecoder)

um = 1e-6

wavelength = data["wavelength0"]




for m in range(2):
    ns = np.squeeze(data['neff'][m,:,0])
    na = np.squeeze(data['neff'][m,:,1])

    gs = np.squeeze(data['gs']/um)
    Lc = wavelength/2/(np.abs(ns)-np.abs(na))/um

    print(ns[10])
    print(na[10])
    print(wavelength)
    print(Lc[10])

    B, logA = np.polyfit(gs, np.log(Lc), 1)

    A = np.exp(logA)

    gs_fit = np.linspace(gs[0], gs[-1], 100)
    Lc_fit = A * np.exp(B * gs_fit)
    print(f"material {m}")
    with open(f"./out/coeffs_{m}.txt", "w") as f:
        f.write(f"A={A}\n")
        f.write(f"B={B}\n")

    plt.figure(figsize=(8, 5))

    plt.semilogy(gs, Lc, label="Simulación")
    plt.semilogy(gs_fit, Lc_fit, label="Ajuste exponencial")

    plt.xlabel(r"gap (um)")
    plt.ylabel(r"$L_{\mathrm{crossover}}$ (um)")

    plt.minorticks_on()
    plt.grid(True, which="major")
    plt.grid(True, which="minor", alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.savefig(f"./out/sim_{m}.png")
plt.show()
print("Done!")