#!/usr/bin/env python3
"""Pass Home Assistant app options to the upstream OpenInvento process."""

import json
import os
import sys


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("The OpenInvento image did not define a startup command")

    with open("/data/options.json", encoding="utf-8") as options_file:
        options = json.load(options_file)

    required = ("app_url", "init_admin_username", "init_admin_password", "secret_key")
    missing = [key for key in required if not options.get(key)]
    if missing:
        raise SystemExit("Set these required app options before starting: " + ", ".join(missing))

    env = os.environ.copy()
    env.update(
        {
            "DATA_DIRECTORY": "/data",
            "APP_URL": options["app_url"],
            "INIT_ADMIN_USERNAME": options["init_admin_username"],
            "INIT_ADMIN_PASSWORD": options["init_admin_password"],
            "CREATE_INIT_ADMIN": str(options["create_init_admin"]).lower(),
            "ENABLE_SIGNUP": str(options["enable_signup"]).lower(),
            "SECRET_KEY": options["secret_key"],
        }
    )
    if options.get("app_urls"):
        env["APP_URLS"] = options["app_urls"]

    os.execvpe(sys.argv[1], sys.argv[1:], env)


if __name__ == "__main__":
    main()
