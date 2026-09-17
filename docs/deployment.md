# Local and Optional GitHub Deployment

## Local use: no credentials

Build a directory containing only the public static dashboard:

```sh
python3 tools/build_rsi.py --output-dir dist
python3 -m http.server 8000 --bind 127.0.0.1 --directory dist
```

Open `http://127.0.0.1:8000/?lang=en`. The server binds to your computer only. It does not contact GitHub, refresh remote experiments, or require a token. Python's development server is suitable for a local preview; use your preferred static web server to host `dist/` on your own infrastructure.

For a shared deployment, publish the generated `dist/` directory, not a directory containing private episode records. The HTML embeds aggregate data; hiding a model in the chart does not remove its data from the file.

## GitHub Pages: opt in on your own repository

1. Fork or copy this repository into an account you control. Use your own GitHub login, Git credentials, or authorized token when pushing; no credential from this project's author is needed.
2. Copy `deploy/github-pages.yml.example` to `.github/workflows/deploy-pages.yml` in your copy, then commit and push it to the default branch. You can do this in GitHub's browser editor while signed in.
3. In your repository's **Settings → Pages**, select **GitHub Actions** as the publishing source.
4. Under **Actions**, choose **Deploy visualization to GitHub Pages**, then **Run workflow**. It builds and uploads `dist/`; the deployment URL appears in the run.

The example has only a manual trigger and is inactive in its shipped `.example` location. It does not enable Pages or deploy when you merely clone the repository. Your repository or organization must allow Pages and Actions.

The workflow uses GitHub's automatic token for **your repository**, with `contents: read`, `pages: write`, and `id-token: write`. A separate personal access token is normally unnecessary for this workflow. Personal tokens, if your separate tooling requires them, belong in that tooling's credential store or your own repository secrets, never in HTML, committed files, or a URL. Use an account with the permissions required by the chosen operation.

See GitHub's official documentation on [publishing sources](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) and [custom Pages workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages).

## Existing branch-based hosting

A repository already configured to publish from `main` at `/` can keep using its committed root `index.html` and `rsi/` files. Run `python3 tools/build_rsi.py` before committing a dashboard update. This repository's original hosted preview uses that configuration; the optional workflow does not change those settings.

Choose one publishing method in your own repository. When enabling the workflow, select GitHub Actions as described above. To keep everything local, leave Pages unconfigured and do not copy the workflow into `.github/workflows/`.
