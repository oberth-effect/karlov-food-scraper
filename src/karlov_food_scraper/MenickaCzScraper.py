from datetime import datetime

from bs4 import element

from .FoodScraper import DailyMenu, FoodItem, FoodScraper

EMPTY_DAY = "Pro tento den nebylo zadáno menu."


def parse_food_item(e: element) -> FoodItem:
    name = e.find("td", class_="food").text
    price = e.find("td", class_="prize").text.split(" ")[0]

    return FoodItem(name, int(price) if price else None)


class MenickaCzScraper(FoodScraper):
    restaurant_name: str
    restaurant_id: int

    def __init__(self, restaurant_name: str, restaurant_id: int) -> None:
        super().__init__()
        self.restaurant_name = restaurant_name
        self.restaurant_id = restaurant_id
        self.menu_url = f"https://www.menicka.cz/tisk.php?restaurace={restaurant_id}"

    def _get_day_food_list(self, day: int) -> DailyMenu:
        soup = self._get_html_soup()
        day_elem = soup.find_all("div", class_="content")[day]
        soup_elems = day_elem.find_all("tr", class_="soup")
        food_elems = day_elem.find_all("tr", class_="main")
        soups = list(filter(lambda f: f.food_name != EMPTY_DAY, [parse_food_item(e) for e in soup_elems]))
        foods = [parse_food_item(e) for e in food_elems]

        return DailyMenu(restaurant_name=self.restaurant_name, soups=soups, menus=[], additional_foods=foods)

    def get_food_list(self) -> DailyMenu:
        day = datetime.today().weekday()
        return self._get_day_food_list(day)
