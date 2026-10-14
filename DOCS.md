# OpenInvento app

OpenInvento is a self-hosted inventory manager. This Home Assistant app runs the upstream `ghcr.io/openinvento/openinvento` image and stores its database and uploads under `/data`, which Home Assistant includes in app backups.

## Setup

1. Set **App URL** to the complete URL users will use to open OpenInvento, including the port when applicable. For example, `http://192.168.1.20:8080`. OpenInvento uses this value for CSRF protection, so it must match the browser URL.
2. Set a long random **Secret key**. Generate one with `openssl rand -hex 32`.
3. Set the initial administrator username and password. The initial administrator is created only when the database has no users. OpenInvento will ask for a password change on first login.
4. Save the configuration and start the app. Container port `80/tcp` is published on host port `8080` by default. If that port is already in use, change the host port under **Network** and update **App URL** to match.

The web interface is available through the configured port mapping. Keep **App URL** in sync with the address you use in the browser.

**Additional trusted URLs** accepts a comma-separated list of extra browser origins when OpenInvento is reached through more than one hostname or reverse proxy. Ensure each URL is trusted by your network and proxy configuration.

Public signup is disabled by default. Enable it only if you intend to allow new accounts to register. You can disable initial administrator creation for an existing installation; it has no effect once users exist.

## Data and updates

App data persists in `/data` and is covered by Home Assistant app backups. Create a backup before restoring or moving the app. The app image is based on the upstream `latest` image; updating this app rebuilds against the current upstream image.

## Links

- [OpenInvento project and configuration reference](https://github.com/openinvento/openinvento)
- [Home Assistant app documentation](https://developers.home-assistant.io/docs/apps)
