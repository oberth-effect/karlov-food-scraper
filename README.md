# Karlov Food Scraper

Simple scraper that scrapes menus of selected restaurants.
If supplied with a webhook it posts them to Slack.

Not very reusable, except for `MenickaCzScraper.py` which can be used for any restaurant that publishes lunch menus to [menicka.cz](https://menicka.cz/).

## Installation
### 1. Clone repo
```bash
git clone 
```

### 2. Install using pip
```bash
cd karlov-food-scraper
pip install .
```

## Usage
### Print to terminal

```bash
karlov_lunch
```

### Post to Slack
```bash
karlov_lunch -s <slack_webhook_url>
```

