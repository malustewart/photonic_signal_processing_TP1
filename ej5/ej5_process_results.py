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

filename = "./out/untitled.json"
outdir = "./out/"

with open(filename) as f:
   data = json.load(f, cls=LumDecoder)

wavelength = data["wavelength0"]

for m in range(2):
    print(f"material {m+1}")

    ns = data['neff'][0,:,0]
    na = data['neff'][0,:,1]

    gs = data['gs']
    Lc = wavelength/2/(np.abs(ns)-np.abs(na))

    print(ns)
    print(na)
    plt.figure()
    plt.plot(gs, Lc)
plt.show()
print("Done!")