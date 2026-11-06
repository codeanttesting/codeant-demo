# CI security pipeline

Copy [the workflow](../../.github/workflows/codeant-security.yml), then:

1. Enable secrets, SAST, and SCA analysis in CodeAnt.
2. Open **Settings → Code Analysis → Quality Gates**, select your repository,
   and turn **Quality Gate** **On**.
3. Add **Full Code** conditions for **SAST Security Rating** and **SCA Security
   Rating**, using **Less Than or Equals → C**. Changes save automatically.
4. Store a CodeAnt token with the **Codeant CI/CD** role as the Actions secret
   `CODEANT_TOKEN`. This test repository also accepts its existing legacy secret.
5. Replace the workflow's branch triggers with your target branch and run it.

Set `quality_gate: 'true'` to fail the action on a failed native verdict or results
timeout. Set it to `'false'` for report-only runs. The pinned action revision
supports this input; `v0.0.5` does not. See [action PR #5](https://github.com/CodeAnt-AI/codeant-ci-scan-action/pull/5).

Configure thresholds before enforcing: without conditions, CodeAnt can return
PASSED. Native full-code gates cover SAST/SCA/IaC ratings and duplicate code.
Secrets appear in reports but have no native full-code gate metric.

Download **codeant-results** from the run's **Artifacts** section. It contains
native `results.json`, `codeant.sarif`, and `codeant-qg.xml`. The action does not
generate CSV/PDF. Reports upload even when the scan step fails.

Replace the deployment placeholder with your command and keep `needs: security`.
Require the check in branch protection to block merges. Fork PRs are skipped
because they do not receive repository secrets.

## Verified action runs

Both runs returned 48 findings and a native FAILED verdict (SAST C, SCA D).

| Input | Run | Result |
| --- | --- | --- |
| `quality_gate: 'false'` | [42309878084](https://github.com/codeanttesting/codeant-demo/actions/runs/42309878084) | Scan succeeded; deployment placeholder ran. |
| `quality_gate: 'true'` | [42310207026](https://github.com/codeanttesting/codeant-demo/actions/runs/42310207026) | Scan step failed; deployment was skipped; reports uploaded. |

Native reports and selected logs are preserved in [`evidence/report-only`](evidence/report-only)
and [`evidence/enforce`](evidence/enforce). Future finding counts may differ.
