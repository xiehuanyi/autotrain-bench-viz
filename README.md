# AutoTrain-Bench visualizations

- [RSI / meta-learning dashboard](https://xiehuanyi.github.io/autotrain-bench-viz/):
  the latest selected single-H200 Track A/B campaign, with model filters,
  a single configurable chart and paired tables. Select candidate history or
  final results, choose either axis, swap axes, and use linear/log scales.
  Both views expose Score, NLL, perplexity, inference latency, evaluation time
  and throughput. Time, candidate/lease counts, improvements and Agent token
  usage are also available where recorded. Both views default to Score versus
  seconds per task (s/task). The initial data view is Final · TEST.
  A cursor-following tooltip shows full metrics on hover near a point; touch
  users can tap, and keyboard users can focus a point (Escape dismisses).
  Candidate metrics come from their own postmortem ANALYSIS evaluations;
  final metrics come from TEST. Perplexity is derived as exp(mean NLL).
  `Seconds per task (s/task)` uses the original `time_per_task` values, matching
  the earlier viewer. It is available on either axis in both views and is the
  default cost axis. The separate millisecond option remains available.

Only the latest selected H200 campaign is displayed. Older experiment pages
have been removed from the published site. `/rsi/` is an alias of the homepage.

## Languages

Use the **中文 / English** switch in the header. Navigation, chart metrics,
tooltips, tables, explanatory notes, and accessibility labels switch together.
Changing language preserves the selected track, models, axes, and data view.
The choice is saved locally. `?lang=en` and `?lang=zh` provide direct links and
override the saved preference; otherwise the browser language is used initially.
Translation strings are maintained in `tools/translations.json` and embedded
in the generated HTML, so both languages also work offline.

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

Source: `tools/build_rsi.py`, `tools/rsi-template.html`, and `tools/translations.json`.
GitHub Pages serves `main` from the repository root. Commit and push generated
`index.html`, `rsi/index.html` and `rsi/data.json` to publish; this is a snapshot, not a live monitor.

A/B both allow adaptation and have different budgets. Candidate ANALYSIS is
computed after research ends, not provided to the Agent during research.
Observed improvements and A/B differences are not causal RSI effect estimates.
