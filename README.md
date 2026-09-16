# AutoTrain-Bench visualizations

- [RSI / meta-learning dashboard](https://xiehuanyi.github.io/autotrain-bench-viz/):
  the latest selected single-H200 Track A/B campaign, with model filters,
  postmortem candidate trajectories, TEST quality/cost plots, and paired tables.

Only the latest selected H200 campaign is displayed. Older experiment pages
have been removed from the published site. `/rsi/` is an alias of the homepage.

## Rebuild the RSI dashboard

Python 3 standard library only; no installation or browser-side dependencies.
The public aggregate JSON is committed so anyone can reproduce the page:

```sh
python3 tools/build_rsi.py
```

To update it from a new trusted `atb_viz` snapshot:

```sh
python3 tools/build_rsi.py --snapshot /path/to/viewer/data.json
```

The exporter checks completed-run data/evaluator identities and selects only
model identifiers, numeric results, candidate trajectories and public metadata.
It does not export raw transcripts, commands, workspace text, private paths,
or credentials. The HTML embeds `rsi/data.json` and works offline.

Source: `tools/build_rsi.py` and `tools/rsi-template.html`.
GitHub Pages serves `main` from the repository root. Commit and push generated
`index.html`, `rsi/index.html` and `rsi/data.json` to publish; this is a snapshot, not a live monitor.

A/B both allow adaptation and have different budgets. Candidate ANALYSIS is
computed after research ends, not provided to the Agent during research.
Observed improvements and A/B differences are not causal RSI effect estimates.
