#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


years = [2020, 2021, 2022, 2023, 2024, 2025]
# B conferences
bdsets = {"QEST+FORMATS": "qest+formats-scopus.csv",
          "CSL": "csl-scopus.csv",
          "VMCAI": "vmcai-scopus.csv",
          "ICPE": "icpe-scopus.csv",
          "IFM": "ifm-scopus.csv",
          "RV": "rv-scopus.csv"}
confs = sorted(bdsets.keys())
width = 1 / 3  # len(dsets)
ori_df = pd.read_csv("papers.csv").sort_values(by=["Conference"])


def load_bibs(year, ithbar, fig, ax):
    df = ori_df.loc[ori_df["Year"] == year]
    sub = df["Submissions"].to_list()
    acc = df["Published"].to_list()
    assert all([s >= a for (s, a) in zip(sub, acc)])
    sub_acc = [s - a for (s, a) in zip(sub, acc)]
    weights = {
        "Accepted": np.array(acc),
        "Submitted": np.array(sub_acc),
    }

    # Add data to plot
    offset = ithbar * width * (len(confs) + 2)
    x = np.array([i * width for i in range(len(confs))])
    bottom = np.zeros(len(confs))
    for i, (b, w) in enumerate(weights.items()):
        assert len(confs) == len(w)
        rects = ax.bar(x + offset, w, width, label=b, bottom=bottom)
        if i == 0:
            pcts = [f"{int(100 * a / s)}% {c}" if s > 0 else ""
                    for (s, a, c) in zip(sub, acc, confs)]
            print(pcts)
            ax.bar_label(rects, labels=np.array(pcts),
                         padding=-10, rotation=90)
        bottom += w

    return


if __name__ == "__main__":
    fig, ax = plt.subplots(layout='constrained')
    plt.title("Acceptance rates")
    plt.xlabel("Years")
    plt.ylabel("Papers")

    # Prepare citation-count plots
    for i, year in enumerate(years):
        load_bibs(year, i, fig, ax)

    # Finalize plot
    period = (len(confs) + 2) * width
    off = len(confs) * width / 2
    plt.xticks(np.array([off + i * period
                        for i in range(len(years))]),
               years)
    # plt.legend(loc="best")
    plt.show()
