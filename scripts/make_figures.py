#!/usr/bin/env python3
"""Regenerate every figure in figures/ from data already committed to this repo.

Nothing here recomputes science. Each panel reads a summary file or a saved
pose that an experiment produced, and plots it as-is.

    uv run scripts/make_figures.py

Sources
-------
fig1  research/experiments/exp-002/derived/native_redocking_summary.json
      research/experiments/exp-003/derived/results_summary.json
fig2  research/experiments/exp-003/derived/results_summary.json
      research/experiments/exp-004/derived/results_summary.json
fig3  research/experiments/exp-004/derived/results_summary.json
fig4  research/experiments/exp-002/derived/native_0EU_bound_reference.pdb
      research/experiments/exp-002/derived/receptor_3tdc_assembly2_prepared.pdb
      research/experiments/exp-002/tables/native_site_contacts.csv
      research/experiments/exp-002/poses/native_0EU/seed-1001.pdbqt
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
EXP2 = ROOT / "research/experiments/exp-002"
EXP3 = ROOT / "research/experiments/exp-003"
EXP4 = ROOT / "research/experiments/exp-004"

# Colour-blind-safe pairs (Okabe-Ito).
BLUE = "#0072b2"
ORANGE = "#d55e00"
GREEN = "#009e73"
GREY = "#666666"

plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 200,
    "savefig.bbox": "tight",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "legend.frameon": False,
})


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def save(fig, stem: str) -> None:
    FIG.mkdir(exist_ok=True)
    for ext in ("png", "svg"):
        fig.savefig(FIG / f"{stem}.{ext}")
    plt.close(fig)
    print(f"wrote figures/{stem}.png and figures/{stem}.svg")


# ---------------------------------------------------------------------------
# Figure 1 - redocking controls: one failed, one passed
# ---------------------------------------------------------------------------
def figure_redocking_controls() -> None:
    acc2 = load(EXP2 / "derived/native_redocking_summary.json")["run_summaries"]
    sert = load(EXP3 / "derived/results_summary.json")["run_summaries"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.0, 3.6), sharey=True)

    # -- ACC2 -------------------------------------------------------------
    seeds = [str(r["seed"]) for r in acc2]
    top = [r["top_pose_RMSD_A"] for r in acc2]
    closest = [r["closest_sampled_RMSD_A"] for r in acc2]
    x = range(len(seeds))
    w = 0.36
    ax1.bar([i - w / 2 for i in x], top, w, color=ORANGE, label="top-ranked pose")
    ax1.bar([i + w / 2 for i in x], closest, w, color=GREY,
            label="closest pose sampled (any rank)")
    for i, (t, c, r) in enumerate(zip(top, closest, acc2)):
        ax1.text(i - w / 2, t + 0.15, f"{t:.1f}", ha="center", fontsize=7.5)
        ax1.text(i + w / 2, c + 0.15, f"{c:.1f}\n(rank {r['closest_sampled_mode']})",
                 ha="center", fontsize=7.5)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels(seeds)
    ax1.set_xlabel("Vina seed")
    ax1.set_ylabel("RMSD to deposited ligand (Å)")
    ax1.set_title("ACC2 · 3TDC, native ligand 0EU\nFAILED — pilot stopped here", color=ORANGE)
    ax1.legend(loc="upper center", fontsize=7.5, ncol=2, bbox_to_anchor=(0.5, 1.02))

    # -- SERT -------------------------------------------------------------
    labels = [f"{r['state'].split('_')[1][:4]}.\n{r['seed']}" for r in sert]
    vals = [r["top_pose_RMSD_A"] for r in sert]
    colors = [BLUE if r["formal_charge"] == 0 else GREEN for r in sert]
    ax2.bar(range(len(vals)), vals, 0.6, color=colors)
    for i, (v, r) in enumerate(zip(vals, sert)):
        ax2.text(i, v + 0.15, f"{v:.2f}", ha="center", fontsize=7.5)
    ax2.set_xticks(range(len(labels)))
    ax2.set_xticklabels(labels, fontsize=7.5)
    ax2.set_xlabel("paroxetine preparation · seed")
    ax2.set_title("SERT · 6VRH, native ligand paroxetine\nPASSED — closest mode was rank 1 in all six runs",
                  color=GREEN)
    handles = [plt.Rectangle((0, 0), 1, 1, color=BLUE),
               plt.Rectangle((0, 0), 1, 1, color=GREEN)]
    ax2.legend(handles, ["neutral", "protonated"], loc="upper center", fontsize=7.5,
               ncol=2, bbox_to_anchor=(0.5, 1.02))

    ax1.set_ylim(0, 12.6)
    fig.suptitle("Native-ligand redocking controls, run before any PRL-8-53 docking", y=1.03)
    fig.text(0.5, -0.16,
             "Direct RMSD in the unchanged deposited frame over stereochemistry-preserving heavy-atom graph automorphisms; "
             "no ligand or receptor fitting.\nNo numerical pass/fail threshold was declared in either protocol — the measured "
             "geometry and ranking are reported as they came out.",
             ha="center", fontsize=7.5, color=GREY)
    save(fig, "fig1-redocking-controls")


# ---------------------------------------------------------------------------
# Figure 2 - Vina scores in the one shared SERT setup
# ---------------------------------------------------------------------------
def figure_scores() -> None:
    sert = load(EXP3 / "derived/results_summary.json")["run_summaries"]
    prl = load(EXP4 / "derived/results_summary.json")["run_summaries"]

    groups: list[tuple[str, list[float], str]] = []
    for state, color in (("paroxetine_neutral", BLUE), ("paroxetine_protonated", GREEN)):
        groups.append((state.replace("_", "\n"),
                       [r["top_score"] for r in sert if r["state"] == state], color))
    for state, conf in (("neutral", "c1"), ("neutral", "c2"),
                        ("protonated", "c1"), ("protonated", "c2")):
        groups.append((f"PRL-8-53\n{state} {conf}",
                       [r["top_score"] for r in prl
                        if r["state"] == state and r["conformer"] == conf], ORANGE))

    fig, ax = plt.subplots(figsize=(8.2, 3.8))
    for i, (label, vals, color) in enumerate(groups):
        ax.scatter([i] * len(vals), vals, s=44, color=color, zorder=3,
                   edgecolor="white", linewidth=0.6)
        ax.hlines(sum(vals) / len(vals), i - 0.28, i + 0.28, color=color, lw=2, zorder=2)
    ax.set_xticks(range(len(groups)))
    ax.set_xticklabels([g[0] for g in groups], fontsize=8)
    ax.set_ylabel("top-ranked Vina score (arbitrary units)")
    ax.axvline(1.5, color=GREY, ls=":", lw=1)
    ax.invert_yaxis()
    ax.text(0.125, 1.03, "reference ligand (paroxetine)", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=8, color=GREY)
    ax.text(0.62, 1.03, "PRL-8-53 (exploratory)", transform=ax.transAxes,
            ha="center", va="bottom", fontsize=8, color=GREY)
    ax.set_title("Top-ranked scores in the one shared SERT setup (6VRH, identical rigid receptor and box)",
                 pad=26)
    fig.text(0.5, -0.17,
             "Every point is one search; three fixed seeds per preparation. Vina's score is an empirical function, not a free energy, "
             "affinity or probability.\nComparing PRL-8-53 to paroxetine here is a comparison of model output in one box — it is NOT a "
             "potency comparison and says nothing about whether PRL-8-53 binds SERT.",
             ha="center", fontsize=7.5, color=GREY)
    save(fig, "fig2-vina-scores")


# ---------------------------------------------------------------------------
# Figure 3 - how reproducible the exploratory PRL-8-53 poses were
# ---------------------------------------------------------------------------
def figure_pose_variability() -> None:
    var = load(EXP4 / "derived/results_summary.json")["pairwise_variability"]
    keys = [("top_modes_across_seeds_same_starting_conformer",
             "same starting conformer,\ndifferent seed"),
            ("top_modes_across_starting_conformers",
             "different starting\nconformer")]

    colors = {"neutral": BLUE, "protonated": GREEN}
    rows = []
    for key, label in keys:
        for state in ("neutral", "protonated"):
            rows.append((f"{state}  —  {label}", var[state][key], colors[state]))
    rows.reverse()

    fig, ax = plt.subplots(figsize=(8.4, 3.4))
    for y, (label, d, color) in enumerate(rows):
        ax.hlines(y, d["minimum_A"], d["maximum_A"], color=color, lw=9, alpha=0.30)
        ax.plot([d["minimum_A"], d["maximum_A"]], [y, y], "|", color=color, ms=11, mew=1.6)
        ax.plot([d["median_A"]], [y], "o", color=color, ms=9, zorder=3)
        ax.text(6.55, y, f"{d['minimum_A']:.2f}   {d['median_A']:.2f}   {d['maximum_A']:.2f}"
                f"     n={d['count']}", fontsize=8, va="center", color=color,
                family="monospace")
    ax.text(6.55, len(rows) - 0.4, "min   median   max", fontsize=8, va="center",
            color=GREY, family="monospace")
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.5)
    ax.set_xlim(-0.2, 6.5)
    ax.set_ylim(-0.7, len(rows) - 0.1)
    ax.set_xlabel("RMSD between top-ranked poses (Å)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#dddddd", lw=0.7)
    ax.set_axisbelow(True)
    ax.set_title("Exploratory PRL-8-53 docking: how far apart the top-ranked poses landed (exp-004)",
                 loc="left", pad=14)
    fig.text(0.5, -0.15,
             "12 fixed searches (2 charge states × 2 starting conformers × 3 seeds), 240 modes, 14,280 within-state pairwise RMSDs. "
             "Cross-state pairs were not pooled.\nThe sampled protonated preparations moved around less than the neutral ones. That is "
             "an observation about this sampling, not evidence for a physiological protonation state or for SERT binding.",
             ha="center", fontsize=7.5, color=GREY)
    save(fig, "fig3-prl-pose-variability")


# ---------------------------------------------------------------------------
# Figure 4 - the ACC2 site, and where the docked poses actually went
# ---------------------------------------------------------------------------
def _read_pdb_het(path: Path) -> list[tuple[float, float]]:
    pts = []
    for line in path.read_text().splitlines():
        if line.startswith(("ATOM", "HETATM")) and line[76:78].strip() != "H":
            pts.append((float(line[30:38]), float(line[38:46])))
    return pts


def _read_pdbqt_models(path: Path) -> dict[int, list[tuple[float, float]]]:
    models: dict[int, list[tuple[float, float]]] = {}
    current = None
    for line in path.read_text().splitlines():
        if line.startswith("MODEL"):
            current = int(line.split()[1])
            models[current] = []
        elif line.startswith(("ATOM", "HETATM")) and current is not None:
            if line[77:79].strip().upper().startswith("H"):
                continue
            models[current].append((float(line[30:38]), float(line[38:46])))
    return models


def _contact_ca(receptor: Path, contacts: Path) -> list[tuple[str, str, float, float]]:
    wanted = {}
    with contacts.open() as fh:
        for row in csv.DictReader(fh):
            if row["within_4.5_A"].strip().lower() != "true":
                continue
            chain = "B" if row["chain"].startswith("B") else "A"
            wanted[(chain, int(row["author_residue_number"]))] = row["residue"]
    out = []
    for line in receptor.read_text().splitlines():
        if not line.startswith("ATOM") or line[12:16].strip() != "CA":
            continue
        key = (line[21], int(line[22:26]))
        if key in wanted:
            out.append((key[0], f"{wanted[key]}{key[1]}",
                        float(line[30:38]), float(line[38:46])))
    return out


def figure_acc2_site() -> None:
    ref = _read_pdb_het(EXP2 / "derived/native_0EU_bound_reference.pdb")
    models = _read_pdbqt_models(EXP2 / "poses/native_0EU/seed-1001.pdbqt")
    summary = load(EXP2 / "derived/native_redocking_summary.json")["run_summaries"][0]
    contacts = _contact_ca(EXP2 / "derived/receptor_3tdc_assembly2_prepared.pdb",
                           EXP2 / "tables/native_site_contacts.csv")

    def centroid(pts):
        return (sum(p[0] for p in pts) / len(pts), sum(p[1] for p in pts) / len(pts))

    fig, ax = plt.subplots(figsize=(7.0, 6.2))
    for chain, color, label in (("A", BLUE, "chain A"), ("B", ORANGE, "symmetry mate")):
        pts = [(x, y) for ch, _lab, x, y in contacts if ch == chain]
        if pts:
            ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=90, color=color,
                       marker="P", alpha=0.85,
                       label=f"{label}: {len(pts)} Cα within 4.5 Å", zorder=2)

    close_rank = summary["closest_sampled_mode"]
    series = [
        (ref, "black", "o", "deposited 0EU (crystal pose)"),
        (models[1], ORANGE, "^",
         f"top-ranked docked pose — {summary['top_pose_RMSD_A']:.1f} Å from deposited"),
        (models[close_rank], GREEN, "s",
         f"closest pose sampled, rank {close_rank} — {summary['closest_sampled_RMSD_A']:.1f} Å"),
    ]
    for pts, color, marker, label in series:
        ax.scatter([p[0] for p in pts], [p[1] for p in pts], s=18, color=color,
                   marker=marker, alpha=0.40, zorder=3)
        cx, cy = centroid(pts)
        ax.scatter([cx], [cy], s=170, color=color, marker=marker, zorder=5,
                   edgecolor="white", linewidth=1.4, label=label)

    ax.set_aspect("equal")
    ax.set_xlabel("x (Å, deposited frame)")
    ax.set_ylabel("y (Å, deposited frame)")
    ax.set_title("Why the ACC2 pilot stopped\n3TDC carboxyltransferase pocket, XY projection, seed 1001")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.11), fontsize=8)
    fig.text(0.5, -0.31,
             "The pocket is split across a crystallographic symmetry interface: 14 of the 20 residues within 4.5 Å of the deposited "
             "ligand belong to the symmetry mate.\nThe search reproducibly top-ranked an orientation ~9 Å from the deposited pose, so "
             "the setup could not be used as a reference and no PRL-8-53 score was ever produced.\n"
             "Small markers are heavy atoms, large markers are their centroids. RMSD is per-atom over the best graph mapping, not a "
             "centroid distance — a flipped pose can keep the centroid and still be 9 Å away.\n"
             "Projected onto x/y only; apparent overlaps may be separated in z.",
             ha="center", fontsize=7.5, color=GREY)
    save(fig, "fig4-acc2-site-and-poses")


if __name__ == "__main__":
    figure_redocking_controls()
    figure_scores()
    figure_pose_variability()
    figure_acc2_site()
