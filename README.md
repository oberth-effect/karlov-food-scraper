# Karlov Food Scraper

Simple scraper that scrapes menus of selected restaurants.
If supplied with a webhook it posts them to Slack.

Not very reusable, except for `MenickaCzScraper.py` which can be used for any restaurant that publishes lunch menus to [menicka.cz](https://menicka.cz/).

## Installation
### 1. Clone repo
```shell
git clone https://github.com/oberth-effect/karlov-food-scraper.git
```

### 2. Install using pip
```shell
cd karlov-food-scraper
pip install .
```

## Usage
```console
> karlov_lunch --help
usage: karlov_food_scraper [-h] [-s [webhook-url]]

Displays the lunch menu of selected restaurants near Karlov MFF, Optionally sends Slack message via webhook.

options:
  -h, --help            show this help message and exit
  -s [webhook-url], --slack [webhook-url]
                        Send menu to Slack instead of printing it to stdout (uses 'Incoming Webhook').

Looks like meat's back on the menu boys
```

