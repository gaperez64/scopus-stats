#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

years = [2020, 2021, 2022, 2023, 2024, 2025]
files = [f"Statistics QEST TPC - {y}.csv" for y in years]
bins = list(range(50))

for y, f in zip(years, files):
    print(f)
    df = pd.read_csv(f)
    data = df["H-Index Google Scholar"].to_list()
    data = [int(x) for x in data if not pd.isna(x) and str(x) != "-"]
    plt.hist(data,
             align="left",
             # bins=bins,
             alpha=0.5,
             label=f"Year {y}")

plt.legend(loc="best")
plt.title(f"Histogram: Program committee x Google Scholar h-index")
plt.xlabel("H-Indices")
plt.ylabel("No. of PC members")
plt.show()
