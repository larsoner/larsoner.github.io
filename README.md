# larsoner.github.io
larsoner.github.io website

Use `pip install -r requirements.txt` to get requirements.

## Previewing

`make html` builds the site into `output/`, and `make serve` serves it at
http://localhost:8000.

## Deploying

Pushing to the `source` branch deploys automatically: the
[Deploy workflow](.github/workflows/deploy.yml) runs `make github`, which builds
the site and pushes it to `master` (served by GitHub Pages). It can also be run
manually from the Actions tab.

To deploy without GitHub Actions, run the same command locally:

```bash
make github
```

This uses `python3 -m pelican` by default; override with e.g.
`make github PY=/path/to/python`.
