from parsel import Selector
import httpx

class Buscape:
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

        product_selectors = selector.css(".ProductCard_ProductCard_Inner__mdriI")
        products = []

        for product_selector in product_selectors:
            product = {
                "title": product_selector.css(".ProductCard_ProductCard_Name__7UxBX::text").get(),
                "image_url": product_selector.css(".ProductCard_ProductCard_Image__lG_w9 img[loading='lazy']::attr(src), .ProductCard_ProductCard_Image__lG_w9 noscript img::attr(src)").get(),
                "price": Buscape._string_price_to_number(product_selector.css(".Text_MobileHeadingS__XS_Au::text").get()),
                "page_url": product_selector.css("::attr(href)").get()
            }

            products.append(product)

        return products

    def search(self, query: str) -> list[dict]:
        url = f"https://www.buscape.com.br/search?q={query}"
        response = httpx.get(url)
        selector = Selector(response.text)

        product_selectors = selector.css(".ProductCard_ProductCard_Inner__gapsh")
        products = []

        for product_selector in product_selectors:
            product = {
                "title": product_selector.css(".ProductCard_ProductCard_Name__U_mUQ::text").get(),
                "image_url": product_selector.css(".ProductCard_ProductCard_Image__4v1sa img::attr(src)").get(),
                "price": Buscape._string_price_to_number(product_selector.css(".Text_MobileHeadingS__HEz7L::text").get()),
                "page_url": product_selector.css("::attr(href)").get()
            }

            products.append(product)

        return products
