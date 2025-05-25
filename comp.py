#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


years = [2020, 2021, 2022]
# A conferences
adsets = {"QEST": "qest-scopus.csv",
          "FORMATS": "formats-scopus.csv",
          "CONCUR": "concur-scopus.csv",
          "FM": "fm-scopus.csv",
          "IJCAR": "ijcar-scopus.csv",
          "TACAS": "tacas-scopus.csv",
          "FOSSCAS": "fossacs-scopus.csv",
          "SAT": "sat-scopus.csv"}
# B conferences
bdsets = {"QEST": "qest-scopus.csv",
          "FORMATS": "formats-scopus.csv",
          "CSL": "csl-scopus.csv",  # "LPAR": "lpar-scopus.csv",
          "ATVA": "atva-scopus.csv",
          "FMCAD": "fmcad-scopus.csv",
          "VMCAI": "vmcai-scopus.csv"}
qpcts = [.05, .10, .25, .50]
width = 0.8 / 8  # len(dsets)


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

    # Add data to plot
    plt.bar(qs, pcts, width, label=f"{dsname}, #papers={npaps}")

    # Return the aggreagated information: mean and median per year
    df = df.groupby(df["Year"]).agg({"Cited by": ["mean", "median"]})
    df.columns = [dsname + "_" + col[1] for col in df.columns]
    return df


if __name__ == "__main__":
    assert len(sys.argv) == 2
    plt.title(f"Citations for years={years}")
    plt.xlabel("Top percentiles")
    plt.ylabel("Percentage of papers cited >= than quantile")

    if sys.argv[1] == "A":
        dsets = adsets
    elif sys.argv[1] == "B":
        dsets = bdsets
    else:
        print("Expected A or B as unique argument!")
        exit(1)

    # Prepare plots
    aggs = []
    for i, (dset, fname) in enumerate(dsets.items()):
        print(f"Going into conference {fname}")
        aggs.append(load_bibs(fname, dset, i))

    # Save aggregated data to csv
    df = pd.concat(aggs, axis=1)
    df.to_csv(f"aggs-{sys.argv[1]}.csv")

    # Finalize plot
    plt.xticks(np.array(range(len(qpcts))) + ((len(dsets) - 1) * width) / 2,
               [str(p * 100) for p in qpcts])
    plt.legend(loc="best")
    plt.show()
