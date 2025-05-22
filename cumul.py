#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_bibs(fpath):
    df = pd.read_csv(fpath)
    years = [2020, 2021, 2022]
    df = df.loc[df["Year"].isin(years)]
    npaps = len(df.index)
    print(f"No. of papers = {npaps}")
    qs = df["Cited by"]
    qpcts = [.05, .10, .25, .50]
    qs = qs.quantile(qpcts).values.tolist()
    print(f"Quantiles {qpcts} = {qs}")
    counts = []
    for up in qs:
        print(f"up = {up}")
        band = df.loc[(df["Cited by"] <= up)]
        counts.append(len(band.index))
    print(f"Papers per quant = {counts}")
    pcts = np.array([(100 * c / npaps) for c in counts])
    qstr = np.array([str(p * 100) for p in qpcts])

    fig = plt.figure()
    ax = fig.add_subplot()
    ax.set_title(f"Citations: File={fpath}|Years={years}|#papers={npaps}")
    plt.bar(qstr, pcts)
    plt.xlabel("Cumulative Percentiles")
    plt.ylabel("Percentage of papers in 0-x percentiles")
    plt.show()


if __name__ == "__main__":
    assert len(sys.argv) == 2
    load_bibs(sys.argv[1])
