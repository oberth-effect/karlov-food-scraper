from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class FoodItem:
    food_name: str
    price_czk: int | None

    alternative_price_czk: int | None = None

    @property
    def fmt_price(self) -> str:
        if self.alternative_price_czk:
            return f"{self.price_czk if self.price_czk else "???"}/{self.alternative_price_czk} Kč"
        elif self.price_czk:
            return f"{self.price_czk} Kč"
        else:
            return ""

    def __str__(self):
        return f"{self.food_name} {self.fmt_price}"


@dataclass
class MenuCombination:
    food: FoodItem
    menu_price_czk: int

    menu_name: str | None = None
    any_soup: bool = True
    specific_soup: FoodItem | None = None

    @property
    def joined_price(self):
        return f"{self.food.price_czk if self.food.price_czk else "???"}/{self.menu_price_czk} Kč"

    @property
    def fmt_price(self):
        return f"{self.menu_price_czk} Kč"

    @property
    def name_food(self):
        prefix = self.menu_name + " " if self.menu_name else ""
        return f"{prefix}{self.food.food_name} "

    def __str__(self):
        return f"{self.name_food}  {self.joined_price}"


@dataclass
class DailyMenu:
    restaurant_name: str
    soups: list[FoodItem]
    menus: list[MenuCombination]
    additional_foods: list[FoodItem]


class FoodScraper:
    menu_url: str

    def _get_html_soup(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"  # noqa: E501
        }
        r = requests.get(self.menu_url, allow_redirects=True, headers=headers)
        if r.status_code != 200:
            raise Exception(f"Could not download the page, got HTTP Code {r.status_code}")
        soup = BeautifulSoup(r.text, "html.parser")
        return soup

    def get_food_list(self) -> DailyMenu:
        raise NotImplementedError
