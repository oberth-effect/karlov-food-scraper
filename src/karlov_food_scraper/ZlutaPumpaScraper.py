import re

from .FoodScraper import DailyMenu, FoodItem, FoodScraper, MenuCombination


def remove_description(s: str) -> str:
    name = "".join(s.split(":")[1:]).strip()
    return re.sub(r"\d\. ", "", name)


def get_price(s: str) -> int:
    if s:
        return int(s.lower().replace("kč", ""))


class ZlutaPumpaScraper(FoodScraper):
    menu_url = "https://zlutapumpa.cz/lunchcz/"

    def _get_menu_element(self):
        soup = self._get_html_soup()
        menu_el = soup.find("div", attrs={"field": "descr"})
        return menu_el

    def _get_menu_list(self) -> list[str, str]:
        m = self._get_menu_element()
        element_list = list(filter(None, [x.text for x in m.children]))
        start_elem = [
            x
            for x in element_list
            if "polévka:" in x.lower() or "předkrm:" in x.lower() or "hlavní jídlo:" in x.lower()
        ]
        start_ind = [element_list.index(e) for e in start_elem] + [len(element_list)]
        slices = [(start_ind[x], start_ind[x + 1]) for x in range(len(start_ind) - 1)]
        items = [
            ("".join(element_list[x : max(x + 1, y - 1)]), element_list[y - 1] if y - 1 != x else None)
            for x, y in slices
        ]
        if "polévka:" not in items[0][0].lower() and "předkrm:" in items[1][0].lower():
            raise Exception("Unexpected Format of Source")
        return items

    def get_food_list(self) -> DailyMenu:
        menu_list = self._get_menu_list()
        food_list = list(map(lambda x: (remove_description(x[0]), get_price(x[1])), menu_list))

        menus = [
            MenuCombination(food=FoodItem(f[0], None), menu_price_czk=f[1], menu_name=f"MENU {i+1}")
            for i, f in enumerate(food_list[2:])
        ]

        return DailyMenu(
            restaurant_name="Žlutá Pumpa",
            soups=[
                FoodItem(food_list[0][0], None),
            ],
            menus=menus,
            additional_foods=[],
        )
