import html
import json
import re

from scrapy import Spider
from scrapy.exceptions import StopDownload
from scrapy.http import Request, Response


class BearspaceSpider(Spider):
    name = "bearspace"
    default_headers: dict[str, str] = {
        "authority": "www.bearspace.co.uk",
        "accept": "text/html,application/xhtml+xml,application"
        "/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }

    def start_requests(self):
        yield Request(
            url="https://www.bearspace.co.uk/purchase?page=1000",  # a high number of pages so we'll have all
            # the data in one call
            headers=self.default_headers,
            method="GET",
            callback=self.parse_gallery_details,
        )

    def parse_gallery_details(self, response: Response):
        resp_json = json.loads(response.css("#wix-warmup-data::text").extract_first())
        offers: list[dict] = []
        offers_count: int = 0
        for gallery in resp_json["appsWarmupData"].values():
            for catalog in gallery.values():
                products_meta_with_data = catalog["catalog"]["category"][
                    "productsWithMetaData"
                ]
                offers = products_meta_with_data["list"]
                offers_count = products_meta_with_data["totalCount"]

        assert len(offers), offers_count
        for offer in offers:
            yield Request(
                url=f"https://www.bearspace.co.uk/product-page/{offer['urlPart']}",
                headers=self.default_headers,
                method="GET",
                callback=self.parse,
                cb_kwargs={"offer": offer},
            )

    # The parsing could be easier with the api, but I'd prefer to write little bit of code and avoid dealing with
    # cookies and ban
    def parse(self, response: Response, offer):
        resp_json = json.loads(response.css("#wix-warmup-data::text").extract_first())
        offer: dict = next(iter(resp_json["appsWarmupData"].values()))[
            f"productPage_GBP_{offer['urlPart']}"
        ]["catalog"]["product"]
        media = [
            m
            for m in re.split(r"<\\?&?.*?>", html.unescape(offer["description"]))
            if m and not m.isdigit()
        ]
        height, width, media_details = self.parse_media(media)
        yield {
            "url": response.url,
            "title": offer["name"],
            "media": media_details,
            "height_cm": height,
            "width_cm": width,
            "price_gb": offer["price"],
        }

    @staticmethod
    def parse_media(media: list[str]):
        height, width, media_details = None, None, None
        dim_index = 0
        for i, m in enumerate(media):
            if "diam" in m.lower():
                height = width = re.findall(r"(\d+[\.|,]?\d?)[cm]?", m)[0]
                dim_index = i
                break
            try:
                parsed_dim = re.findall(r"(\d+\.?\d?)[cm]?", m)
                if len(parsed_dim) > 2:
                    height, width, _ = parsed_dim
                else:
                    height, width = parsed_dim
            except (ValueError, IndexError):
                continue
            if height and width:
                dim_index = i
                break
        # the needed data is either in the first or second element
        media_details = media[0 if dim_index == 1 else 1]
        if not height or not width or not media_details:
            raise StopDownload()
        return height, width, media_details
