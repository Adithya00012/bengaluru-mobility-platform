# Troubleshooting Guide

Real issues encountered while building this project, and how they were resolved.

## "dbt --version" shows an empty Plugins section
**Cause:** `dbt-sqlite`'s installed version doesn't support your installed `dbt-core` version.
**Fix:** `pip install --upgrade dbt-sqlite` — pip will automatically select a compatible `dbt-core` version.

## dbt: "No dbt_project.yml found at expected path"
**Cause:** Running `dbt run`/`dbt test` from the wrong folder.
**Fix:** `cd` into `bengaluru_mobility_dbt/` before any dbt command — dbt must run from the folder containing `dbt_project.yml`.

## GitHub Actions: "cannot import name 'Credentials' from dbt.adapters.base"
**Cause:** The CI runner installed the newest `dbt-core`, incompatible with the pinned `dbt-sqlite` version.
**Fix:** Pin exact versions in the install step: `pip install dbt-core==1.11.15 dbt-sqlite==1.10.0`.

## GitHub Actions workflow disappears from the Actions tab after a push
**Cause:** Invalid YAML syntax (commonly, incorrect indentation) in the workflow file — GitHub silently stops recognizing it.
**Fix:** Check indentation carefully; every step under `steps:` must align consistently (typically 6 spaces before each `- name:`).

## Power BI: "There are pending changes in your queries"
**Cause:** Power Query cached transformation steps referencing columns from a previous version of the source file.
**Fix:** Delete the broken query in Power Query Editor and re-import the CSV fresh, rather than trying to patch the existing query.

## Power BI: dragging a field only shows a date hierarchy (Year/Quarter/Month/Day)
**Cause:** Using the Fields pane checkbox (auto-add) instead of dragging directly into a specific visual's field well.
**Fix:** Always drag fields directly into the Columns/Axis/Legend wells for precise control; avoid the checkbox shortcut for anything beyond a single quick field.

## ML model has negative R² or near-baseline classification accuracy
**Cause:** Very likely insufficient training data relative to the number of features, or a raw sample size too small for the model to detect real patterns.
**Fix:** Check accuracy against an explicit baseline (e.g., always-predict-majority-class) before concluding a model is "good" or "bad." If underperforming, reduce feature count first; if data volume is the bottleneck, expanding the dataset (even synthetically, with realistic built-in patterns) is often the real fix, not different modeling code.