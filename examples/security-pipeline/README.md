# CI security pipeline

Copy [the workflow](../../.github/workflows/codeant-security.yml). No helper script,
policy file, or extra package is required.

1. Enable secrets, SAST, and SCA analysis in CodeAnt.
2. Open **Settings → Code Analysis → Quality Gates**, select your repository,
   and turn **Quality Gate** **On**.
3. Add **Full Code** conditions for **SAST Security Rating** and **SCA Security
   Rating**, using **Less Than or Equals → C**. Changes save automatically.
4. Store a CodeAnt token with the **Codeant CI/CD** role as the Actions secret
   `CODEANT_TOKEN`. This test repository also accepts its existing legacy secret.
5. Replace the workflow's branch triggers with your target branch and run it.

`ENFORCE_SECURITY: 'false'` warns on findings. Set it to `'true'` to fail the job
and skip deployment. Missing results or native gate conditions fail in both modes.

Thresholds are evaluated by CodeAnt. The inline gate step also checks for zero
reported secrets, because the native full-code response has no secrets gate metric.
The published action collects results but does not expose a `quality_gate` input.

Download **codeant-results** from the run's **Artifacts** section. It contains
native `results.json`, `codeant.sarif`, and `codeant-qg.xml`. The action does not
produce CSV or PDF. Do not upload credentials or environment dumps as artifacts.

The deployment step is a placeholder. Replace it with your deployment command and
keep `needs: security`. To block merges, require the check in branch protection.
The workflow skips fork PRs, which do not receive repository secrets.
