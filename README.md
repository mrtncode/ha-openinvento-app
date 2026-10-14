# OpenInvento for Home Assistant

Home Assistant app for [OpenInvento](https://github.com/openinvento/openinvento), a self-hosted inventory manager. It runs the upstream container, persists all application data in the Home Assistant app data volume, and exposes its web interface on a configurable host port.

## Add this repository

In Home Assistant, open **Settings → Apps → App store → ⋮ → Repositories** and add:

`https://github.com/openinvento/ha-openinvento-app`

Then install **OpenInvento**, configure its URL, initial administrator credentials, and secret key, and start the app. Host port `8080` is configured by default; change it under **Network** if needed. See [DOCS.md](DOCS.md) for details.

## Development

The repository root is the app directory. The Dockerfile extends the upstream multi-architecture image and uses `run.py` to translate Supervisor options into the environment variables documented by OpenInvento.

## Publishing an app image

The release workflow builds `amd64` and `aarch64` images and publishes a combined image to GitHub Container Registry. A scheduled workflow checks the upstream OpenInvento releases daily. When it finds a newer stable release, it removes the leading `v` from the version, updates `config.yaml`, adds a linked entry to [CHANGELOG.md](CHANGELOG.md), builds and publishes the image, and creates a matching GitHub release here. You can also start the check from the Actions tab with **Sync OpenInvento release → Run workflow**.
