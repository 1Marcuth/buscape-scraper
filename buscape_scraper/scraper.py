from parsel import Selector
import httpx

class BuscapeScraper:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def _string_price_to_number(cls, string_price: str) -> int:
        price = int(
            float(
                string_price
                    .replace("R$ ", "")
                    .replace(".", "")
                    .replace(",", ".")
            ) * 1000
        )

        return price

    def get_best_offers(self, shop_id: str) -> list[dict]:
        url = f"https://www.buscape.com.br/cupom-de-desconto/{shop_id}/melhores-ofertas"
        response = httpx.get(url)
        selector = Selector(response.text)

        product_selectors = selector.css("[class^='ProductCard_ProductCard_Inner']")
        products = []

        for product_selector in product_selectors:
            product = {
                "title": product_selector.css("[class^='ProductCard_ProductCard_Name'] h2::text").get(),
                "image_url": product_selector.css("[class^='ProductCard_ProductCard_Image'] img[loading='lazy']::attr(src)").get(),
                "price": BuscapeScraper._string_price_to_number(product_selector.css("[data-testid='product-card::price']::text").get()),
                "page_url": product_selector.css("::attr(href)").get()
            }

            products.append(product)

        return products

    def search(self, query: str) -> list[dict]:
        url = f"https://www.buscape.com.br/search?q={query}"
        response = httpx.get(url)
        selector = Selector(response.text)

        product_selectors = selector.css("[class^='ProductCard_ProductCard_Inner']")
        products = []

        for product_selector in product_selectors:
            product = {
                "title": product_selector.css("[class^='ProductCard_ProductCard_Name'] h2::text").get(),
                "image_url": product_selector.css("[class^='ProductCard_ProductCard_Image'] img::attr(src)").get(),
                "price": BuscapeScraper._string_price_to_number(product_selector.css("[data-testid='product-card::price']::text").get()),
                "page_url": "https://www.buscape.com.br" + product_selector.css("::attr(href)").get()
            }

            products.append(product)

        return products
