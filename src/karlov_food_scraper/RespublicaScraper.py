from .FoodScraper import DailyMenu, FoodItem, FoodScraper, MenuCombination
from .MenickaCzScraper import MenickaCzScraper
import re


def is_menu_name(name: str) -> bool:
    return bool(re.search(r"menu\s[0-9]+", name.lower()))


def try_find_food(name: str, food_list: list[FoodItem]) -> FoodItem | None:
    f = list(filter(lambda f: f.food_name == name, food_list))
    if f:
        return f[0]


def parse_menu(raw: FoodItem, foods: list[FoodItem]) -> MenuCombination:
    menu_price = raw.price_czk
    menu_food_name = raw.food_name.split("-")[1].split("+")[0].strip()
    menu_name = raw.food_name.split("-")[0].strip()
    try_food = try_find_food(menu_food_name, foods)
    food = try_food if try_food else FoodItem(menu_food_name, None)

    return MenuCombination(food=food, menu_price_czk=menu_price, menu_name=menu_name)


def deduplicate(menus: list[MenuCombination], foods: list[FoodItem]) -> list[FoodItem]:
    menus_food = [m.food for m in menus]
    return list(filter(lambda f: f not in menus_food, foods))


class RespublicaScraper(FoodScraper):
    menicka_cz_scraper = MenickaCzScraper("Respublika", 3599)

    def get_food_list(self) -> DailyMenu:
        fl = self.menicka_cz_scraper.get_food_list()

        soups = list(filter(lambda s: not is_menu_name(s.food_name), fl.soups))
        foods = list(
            filter(
                lambda s: not is_menu_name(s.food_name) and "menu box" not in s.food_name.lower(), fl.additional_foods
            )
        )

        raw_menus = list(filter(lambda s: is_menu_name(s.food_name), fl.soups + fl.additional_foods))
        menus = [parse_menu(m, foods) for m in raw_menus]
        menus.sort(key=lambda m: m.menu_name)

        return DailyMenu(
            restaurant_name=fl.restaurant_name, soups=soups, menus=menus, additional_foods=deduplicate(menus, foods)
        )
