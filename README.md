# plotly web app

Interactive Dash app for exploring how different positive/negative score splits across multiple pods affect per-pod and average ROC-AUC.

## Python and environment management

This project now targets **Python 3.12** and uses **`uv`** as the default workflow.

### Initialize the environment

```bash
uv python install 3.12
uv sync
```

`uv sync` creates a local `.venv/` and installs the package plus the minimal direct runtime dependencies declared in `pyproject.toml`.

### Direct runtime dependencies

The project keeps only the libraries it imports directly at runtime:

- `dash`
- `gunicorn`
- `numpy`
- `plotly`
- `scikit-learn`

Transitive packages such as Flask, SciPy, and Werkzeug are installed automatically through those top-level dependencies.

## Run locally

### Fully static Plotly.js version

This variant removes Dash from runtime entirely. Python is only used to precompute and export JSON; the browser renders smooth density curves and updates the controls client-side.

Build the static JSON payload:

```bash
uv run python build_static_app.py
```

Serve the static site locally:

```bash
uv run python serve_static_app.py --rebuild
```

Then open:

```text
http://127.0.0.1:8000
```

The static app files live in `static_app/`, and the generated dataset is written to `static_app/data/content.json`.

### Live version

This version recomputes the split distributions and ROC-AUC values on each slider update.

```bash
uv run python app.py
```

### Precomputed version

Generate the cached figures and ROC-AUC combinations first:

```bash
uv run python create_content.py
uv run python app_2.py
```

`app_2.py` is the faster variant and the default deployment target.


## Deployment

### Gunicorn

```bash
uv run gunicorn app_2:server -b 0.0.0.0:8050
```

### Google App Engine

`app.yaml` is configured for Python 3.12.

```bash
gcloud init
gcloud app deploy ./app.yaml -Y
```

### Docker

Build the image:

```bash
docker build -t plotly_app:1.0 . --build-arg runtime_path="."
```

Run it locally:

```bash
docker run --rm --name dash_app -d -p 80:80 plotly_app:1.0
```

If you want to run the published image on a VM:

```bash
chmod +x vm_docker_setup.sh
./vm_docker_setup.sh
```

