# OpenInvento for Home Assistant

Home Assistant app for [OpenInvento](https://github.com/openinvento/openinvento), a self-hosted inventory manager. It runs the upstream container, persists all application data in the Home Assistant app data volume, and exposes its web interface on a configurable host port.

## Add this repository

In Home Assistant, open **Settings → Apps → App store → ⋮ → Repositories** and add:

`https://github.com/openinvento/ha-openinvento-app`

Then install **OpenInvento**, configure its URL, initial administrator credentials, and secret key, set an available host port for port 80, and start the app. See [DOCS.md](DOCS.md) for details.

## Development

The repository root is the app directory. The Dockerfile extends the upstream multi-architecture image and uses `run.py` to translate Supervisor options into the environment variables documented by OpenInvento.

## Publishing an app image

The release workflow builds `amd64` and `aarch64` images and publishes a combined image to GitHub Container Registry. To publish the first installable release, create a GitHub release tagged exactly `1.0.0` (matching `version` in `config.yaml`) after pushing this repository and enabling Actions with package write access. Future releases must use a tag matching the version in `config.yaml`.
