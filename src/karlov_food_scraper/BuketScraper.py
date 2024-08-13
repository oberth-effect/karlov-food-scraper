import re
from dataclasses import dataclass
from datetime import datetime

from bs4 import element

from .FoodScraper import DailyMenu, FoodItem, FoodScraper, MenuCombination


@dataclass
class BuketPrices:
    meat_food: int
    meat_menu: int
    vege_food: int
    vege_menu: int
    soup_large: int
    soup_small: int


@dataclass
class BuketFoodDay:
    soup: str
    meat_food: str
    vege_food: str


BUKET_DAYS = {0: "Pondělí", 1: "Úterý", 2: "Středa", 3: "Čtvrtek", 4: "Pátek"}


class BuketScraper(FoodScraper):
    menu_url = "https://www.buket-buket.cz/nase-menu/"

    def _get_menu_element(self) -> element.Tag:
        soup = self._get_html_soup()
        menu_element = soup.find(string="Týdenní menu").find_parent("div", class_="ez-c")
        return menu_element

    def _parse_food_list(self, menu_element: element.Tag, day: int) -> BuketFoodDay:
        food_list = menu_element.find(string=BUKET_DAYS[day]).find_parent("div")
        foods = food_list.find_all("p")
        return BuketFoodDay(
            soup=foods[0].text,
            meat_food=foods[1].text,
            vege_food=foods[2].text,
        )

    def _parse_prices(self, menu_element: element.Tag) -> BuketPrices:
        price_el = menu_element.find(string="CENA MENU:").find_parent("div")
        price_text = price_el.p.text.lower()
        return BuketPrices(
            meat_food=int(re.search(r"masové\sjídlo\s([0-9]+)\skč", price_text).group(1)),
            meat_menu=int(re.search(r"masové\sjídlo\ss\spolévkou\s([0-9]+)\skč", price_text).group(1)),
            vege_food=int(re.search(r"vegetariánské\sjídlo\s([0-9]+)\skč", price_text).group(1)),
            vege_menu=int(re.search(r"vegetariánské\sjídlo\ss\spolévkou\s([0-9]+)\skč", price_text).group(1)),
            soup_large=int(re.search(r"([0-9]+)\skč\svelká", price_text).group(1)),
            soup_small=int(re.search(r"polévka\s([0-9]+)\skč\smalá", price_text).group(1)),
        )

    def get_food_list(self) -> DailyMenu:
        m = self._get_menu_element()

        day = datetime.today().weekday()

        food_list = self._parse_food_list(m, day)
        prices = self._parse_prices(m)

        soup = FoodItem(food_name=food_list.soup, price_czk=prices.soup_small, alternative_price_czk=prices.soup_large)

        meat_food = FoodItem(food_list.meat_food, prices.meat_food)
        vege_food = FoodItem(food_list.vege_food, prices.vege_food)

        menus = [
            MenuCombination(meat_food, prices.meat_menu, menu_name="MENU 1"),
            MenuCombination(vege_food, prices.vege_menu, menu_name="MENU 2"),
        ]

        return DailyMenu(
            restaurant_name="Buket",
            soups=[
                soup,
            ],
            menus=menus,
            additional_foods=[],
        )
