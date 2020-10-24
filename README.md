# tstartel-pushover

Access T STAR's mobile data usage from emome and send it to pushover.

## Pre-installation

Install these packages first:

* chromium-browser
* chromium-chromedriver

And create symbolic link for chromedriver:

    sudo ln -s /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

## Setup

`~/.config/tstartel-pushover`:

    [default]
    password = password
    pushover_api_token = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    pushover_user_token = YYYYYYYYYYYYYYYYYYYYYYYYYYYYYY
    username = 0900000000

## License

See [LICENSE](LICENSE).
