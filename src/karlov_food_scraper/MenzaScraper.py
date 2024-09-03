from bs4 import BeautifulSoup, element

from .FoodScraper import DailyMenu, FoodItem, FoodScraper


def parse_food_item(e: element) -> FoodItem:
    name = e.text
    price = None
    return FoodItem(name, int(price) if price else None)


class MenzaScraper(FoodScraper):
    restaurant_name: str
    restaurant_id: int

    def __init__(self, restaurant_name: str, restaurant_id: int) -> None:
        super().__init__()
        self.restaurant_name = restaurant_name
        self.restaurant_id = restaurant_id
        self.menu_url = f"https://kamweb.ruk.cuni.cz/webkredit/Api/Ordering/Rss?canteenId={restaurant_id}&locale=cz"

    def _get_today_food_list(self) -> DailyMenu:
        soup = self._get_html_soup(xml=True)
        today_elem = soup.find_all("item")[0]
        food_html = today_elem.find("description").text
        food_bs = BeautifulSoup(food_html, "html.parser")
        food_blocks = food_bs.find_all("ul")

        soups = [parse_food_item(s) for s in food_blocks[0].find_all("li")]
        foods = [parse_food_item(f) for f in food_blocks[1].find_all("li")]

        return DailyMenu(restaurant_name=self.restaurant_name, soups=soups, menus=[], additional_foods=foods)

    def get_food_list(self) -> DailyMenu:
        return self._get_today_food_list()
