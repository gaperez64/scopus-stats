#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


years = [2018, 2019, 2020]
dsets = {"QEST": "qest-scopus.csv",
         "CONCUR": "concur-scopus.csv",
         "FORMATS": "formats-scopus.csv"}
qpcts = [.05, .10, .25, .50]
width = 0.8 / len(dsets)


def load_bibs(fpath, dsname, ithbar):
    df = pd.read_csv(fpath)
    df = df.loc[df["Year"].isin(years)]
    df = df.loc[df["Document Type"] == "Conference paper"]
    npaps = len(df.index)
    print(f"No. of papers = {npaps}")
    qs = df["Cited by"]

    # Get the top quantiles instead of low
    qs = qs.quantile([1 - q for q in qpcts]).values.tolist()
    print(f"Top quantiles {qpcts} = {qs}")
    counts = []
    for low in qs:
        print(f"low = {low}")
        band = df.loc[(df["Cited by"] >= low)]
        counts.append(len(band.index))
    print(f"Papers per quant = {counts}")
    pcts = np.array([(100 * c / npaps) for c in counts])
    qs = np.array(range(len(qpcts))) + (ithbar * width)

    plt.bar(qs, pcts, width, label=f"{dsname}, #papers={npaps}")


if __name__ == "__main__":
    assert len(sys.argv) == 1
    plt.title(f"Citations for years={years}")
    plt.xlabel("Top percentiles")
    plt.ylabel("Percentage of papers cited >= than quantile")

    # Prepare plots
    for i, (dset, fname) in enumerate(dsets.items()):
        load_bibs(fname, dset, i)

    plt.xticks(np.array(range(len(qpcts))) + ((len(dsets) - 1) * width) / 2,
               [str(p * 100) for p in qpcts])
    plt.legend(loc="best")
    plt.show()
