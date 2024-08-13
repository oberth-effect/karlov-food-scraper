import argparse
from datetime import datetime

import requests
from tabulate import SEPARATING_LINE, tabulate

from . import slack_lib
from .BuketScraper import BuketScraper
from .FoodScraper import DailyMenu, FoodScraper
from .RespublicaScraper import RespublicaScraper
from .ZlutaPumpaScraper import ZlutaPumpaScraper

SCRAPERS: list[FoodScraper] = [
    BuketScraper(),
    ZlutaPumpaScraper(),
    RespublicaScraper(),
]

parser = argparse.ArgumentParser(
    prog="karlov_food_scraper",
    description="Displays the lunch menu of selected restaurants near Karlov MFF, Optionally sends Slack message via webhook.",  # noqa: E501
    epilog="Looks like meat's back on the menu boys",
)
parser.add_argument(
    "-s",
    "--slack",
    nargs="?",
    type=str,
    help="Send menu to Slack instead of printing it to stdout (uses 'Incoming Webhook').",
    metavar="webhook-url",
)


def console_print(day_menus: list[DailyMenu]):
    for dm in day_menus:
        name_string = f"**********  {dm.restaurant_name}  **********"
        soup_rows = [["", s.food_name, s.fmt_price] for s in dm.soups]
        menu_rows = [["", m.name_food, m.fmt_price] for i, m in enumerate(dm.menus)]
        food_rows = [
            ["", f.food_name, f.fmt_price] for f in [m.food for m in dm.menus if m.food.price_czk] + dm.additional_foods
        ]

        print(name_string)
        print(
            tabulate(
                ([["Polevky"]] if soup_rows else [])
                + soup_rows
                + ([SEPARATING_LINE] + [["Meny (+ polevka)"]] if menu_rows else [])
                + menu_rows
                + ([SEPARATING_LINE] + [["Jidla"]] if food_rows else [])
                + food_rows
            )
        )
        print("")


def send_slack(url: str, payload: dict):
    print("Sending Slack message...")
    r = requests.post(url, json=payload)
    print(f"Got Http {r.status_code}")


def build_blocks(menu: DailyMenu) -> list[dict]:
    soups_text = "\n".join(str(s) for s in menu.soups)
    foods_text = "\n".join(str(m) for m in menu.menus) + "\n\n" + "\n".join(str(f) for f in menu.additional_foods)

    restaurant_text = soups_text + "\n\n" + foods_text
    return [slack_lib.header(menu.restaurant_name), slack_lib.mrkdwn_section(restaurant_text)] + [slack_lib.divider()]


def build_slack_payload(day_menus: list[DailyMenu]) -> dict:
    restaurant_blocks = [block for m in day_menus for block in build_blocks(m)]
    date = datetime.today().strftime("%d.%m.%Y")

    return {
        "text": f"Menus for {date}",
        "blocks": [
            slack_lib.header(date),
            slack_lib.divider(),
        ]
        + restaurant_blocks
        + [
            slack_lib.plain_context(
                "Bloky: Polévky (malá/velká); Menu (bez polévky/s polévkou); Samostatná jídla bez polévky."  # noqa: E501
            )
        ],
    }


def run_scraper():
    args = parser.parse_args()
    menus = [s.get_food_list() for s in SCRAPERS]

    if args.slack:
        payload = build_slack_payload(menus)
        send_slack(args.slack, payload)
    else:
        console_print(menus)
