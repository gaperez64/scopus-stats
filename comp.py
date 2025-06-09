#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


years = [2020, 2021, 2022]
# A conferences
adsets = {"QEST+FORMATS": "qest+formats-scopus.csv",
          # "QEST": "qest-scopus.csv",
          # "FORMATS": "formats-scopus.csv",
          "CONCUR": "concur-scopus.csv",
          "FM": "fm-scopus.csv",
          "IJCAR": "ijcar-scopus.csv",
          "TACAS": "tacas-scopus.csv",
          "FOSSACS": "fossacs-scopus.csv",
          "SAT": "sat-scopus.csv",
          "ICALP": "icalp-scopus.csv",
          "ICDCS": "icdcs-scopus.csv",
          "ICST": "icst-scopus.csv",
          "ICWSM": "icwsm-scopus.csv",
          "ISSRE": "issre-scopus.csv",
          "MFCS": "mfcs-scopus.csv",
          "STACS": "stacs-scopus.csv"}
# B conferences
bdsets = {"QEST+FORMATS": "qest+formats-scopus.csv",
          # "QEST": "qest-scopus.csv",
          # "FORMATS": "formats-scopus.csv",
          "MASCOTS": "mascots-scopus.csv",
          "CSL": "csl-scopus.csv",  # "LPAR": "lpar-scopus.csv",
          "ATVA": "atva-scopus.csv",
          "FMCAD": "fmcad-scopus.csv",
          "VMCAI": "vmcai-scopus.csv",
          # "AiML": "aiml-scopus.csv",
          "ARES": "ares-scopus.csv",
          # "FCT": "fct-scopus.csv",
          "FSCD": "fscd-scopus.csv",
          "ICPE": "icpe-scopus.csv",
          "IFM": "ifm-scopus.csv",
          "ILP": "ilp-scopus.csv",
          "ISPASS": "ispass-scopus.csv",
          "MFPS": "mfps-scopus.csv",
          "PetriNets": "pn-scopus.csv",
          "RCIS": "rcis-scopus.csv",
          "RV": "rv-scopus.csv",
          "SAGT": "sagt-scopus.csv",
          "SEFM": "sefm-scopus.csv",
          "SRDS": "srds-scopus.csv",
          # "WADS": "wads-scopus.csv",
          "WALCOM": "walcom-scopus.csv"}
qpcts = [.05, .10, .25, .50]
width = 0.8 / 18  # len(dsets)


hdf = pd.read_csv("h_index.csv")


def get_max_hindex(row):
    if pd.isna(row["Author(s) ID"]):
        return 0
    # print(row)
    ids = [int(a) for a in str(row["Author(s) ID"]).split(";")]
    # print(ids)
    # print(hdf.columns)
    # print(hdf["id"].head())
    mx = hdf.loc[hdf["id"].isin(ids)].max()
    mx = mx["hidx"].astype(float)
    return mx


def load_bibs(fpath, dsname, ithbar, hidx=False):
    df = pd.read_csv(fpath)
    df = df.loc[df["Year"].isin(years)]
    df = df.loc[df["Document Type"] == "Conference paper"]
    npaps = len(df.index)
    print(f"No. of papers = {npaps}")
    kcol = "Cited by"
    if hidx:
        kcol = "hindex"
        df[kcol] = df.apply(get_max_hindex, axis=1)

    qs = df[kcol]

    # Get the top quantiles instead of low
    qs = qs.quantile([1 - q for q in qpcts]).values.tolist()
    print(f"Top quantiles {qpcts} = {qs}")
    counts = []
    for low in qs:
        print(f"low = {low}")
        band = df.loc[(df[kcol] >= low)]
        counts.append(len(band.index))
    print(f"Papers per quant = {counts}")
    pcts = np.array(counts)  # [(100 * c / npaps) for c in counts])
    qs = np.array(range(len(qpcts))) + (ithbar * width)

    # Add data to plot
    plt.bar(qs, pcts, width, label=f"{dsname}, #papers={npaps}")

    # Return the aggreagated information: mean and median per year
    # df = df.groupby(df["Year"]).agg({"Cited by": ["mean", "median"]})
    # df.columns = [dsname + "_" + col[1] for col in df.columns]
    return df[kcol].to_list()


if __name__ == "__main__":
    assert len(sys.argv) == 2
    if sys.argv[1] == "A":
        dsets = adsets
    elif sys.argv[1] == "B":
        dsets = bdsets
    else:
        print("Expected A or B as unique argument!")
        exit(1)

    # Citation plots
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    rainbow = [cm(1. * i / len(dsets)) for i in range(len(dsets))]
    ax.set_prop_cycle('color', rainbow)
    plt.title(f"Cited papers for years={years}")
    plt.xlabel("Top percentiles")
    plt.ylabel("Papers cited >= than quantile")

    # Prepare citation-count plots
    aggs = []
    for i, (dset, fname) in enumerate(dsets.items()):
        print(f"Going into conference {fname}")
        aggs.append(load_bibs(fname, dset, i))

    # Save aggregated data to csv
    # df = pd.concat(aggs, axis=1)
    # df.to_csv(f"aggs-{sys.argv[1]}.csv")

    # Finalize plot
    plt.xticks(np.array(range(len(qpcts))) + ((len(dsets) - 1) * width) / 2,
               [str(p * 100) for p in qpcts])
    plt.legend(loc="best")
    plt.show()

    # Boxplot graph now
    fig, ax = plt.subplots()
    plt.title(f"Citations for years={years}")
    plt.ylabel("Citations per paper")
    plt.yscale("log")
    ax.boxplot(aggs, notch=True)
    ax.set_xticklabels([dset for dset, _ in dsets.items()],
                       rotation=30)
    plt.show()

    # Hindex plots
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_prop_cycle('color', rainbow)
    plt.title(f"(Max) h-index of papers for years={years}")
    plt.xlabel("Top percentiles")
    plt.ylabel("Papers with h-index >= than quantile")
    aggs = []
    for i, (dset, fname) in enumerate(dsets.items()):
        print(f"Going into conference {fname}")
        aggs.append(load_bibs(fname, dset, i, hidx=True))
        print(aggs[-1])
    # Finalize plot
    plt.xticks(np.array(range(len(qpcts))) + ((len(dsets) - 1) * width) / 2,
               [str(p * 100) for p in qpcts])
    plt.legend(loc="best")
    plt.show()
    # Boxplot graph now
    fig, ax = plt.subplots()
    plt.title(f"(Max) h-index for years={years}")
    plt.ylabel("(max) h-index per paper")
    ax.boxplot(aggs, notch=True)
    ax.set_xticklabels([dset for dset, _ in dsets.items()],
                       rotation=30)
    plt.show()
