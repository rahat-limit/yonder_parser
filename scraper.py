import requests 
from bs4 import BeautifulSoup as bs4

async def scrape_menu_by_oranization_id(oranization_id: int):
    r = requests.get(f"https://yandex.kz/maps/org/{oranization_id}/menu/")
    soup = bs4(r.text, "html.parser")
    
    # Block to check does menu exists
    carousel = soup.find("div", class_="carousel__content")
    if carousel is None:
        return {"error": "Menu not found"}
    
    if carousel.find("a", text="Мәзір") is None:
        return {"error": "Menu not found"}

    # End block to check does menu exists


    # category_name class business-full-items-grouped-view__category
    # content class business-full-items-grouped-view__items

    # img class image__img
    # title class business-full-items-grouped-view__title
    # description class related-item-photo-view__description
    # price class related-product-view__price
    # volume class related-product-view__volume

    out = {}
    out["context"] = []
    counter = 0
    for category in soup.find_all("div", class_="business-full-items-grouped-view__category"):
        name = category.find("div", class_="business-full-items-grouped-view__title").text
        
        for item in category.find_all("div", class_="business-full-items-grouped-view__item _view_grid"):
            if item is None:
                continue
            item_data = {
                "id": str(oranization_id) + str(counter),
                "title": find_and_get_text(item, "div", "related-item-photo-view__title"),
                "description": find_and_get_text(item, "div", "related-item-photo-view__description"),
                "price": find_and_get_text(item, "span", "related-product-view__price"),
                "volume": find_and_get_text(item, "span", "related-product-view__volume")
            }
            out["context"].append(item_data)
            
            counter += 1
        
    return out

def find_and_get_text(item, tag, class_name):
    element = item.find(tag, class_=class_name)
    return element.text if element is not None else ""
