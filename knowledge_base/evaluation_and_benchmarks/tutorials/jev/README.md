# Jev (TypeSafe) tutorial

Two Jupyter notebooks on the **Jev** model from TypeSafe (https://docs.typesafe.ai):

- `jev_tutorial.ipynb` — how to *use* Jev in Python: basic examples from the docs, the standard
  patterns, and an advanced section that reviews `~/git/fleet` (architecture scorecard, ranked
  improvement backlog, per-file code-smell scan).
- `jev_eval_tutorial.ipynb` — how to *test* Jev before trusting it: a noise floor, accuracy on
  synthetic tasks with a computable ground truth, a calibration/reliability check, invariance to
  meaning-preserving perturbations, and discrimination on controlled sweeps.

Requires `TYPESAFE_API_KEY` in your shell environment.

```bash
just install       # uv sync
just models        # ping the API, list models
just jupyter       # JupyterLab with jev_tutorial.ipynb open
just run           # execute jev_tutorial.ipynb headless
just build         # regenerate jev_tutorial.ipynb from build_notebook.py
just jupyter-eval  # JupyterLab with jev_eval_tutorial.ipynb open
just run-eval      # execute jev_eval_tutorial.ipynb headless
just build-eval    # regenerate jev_eval_tutorial.ipynb from build_eval_notebook.py
```

Full explanation: `index.md`.
