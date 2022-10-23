from __future__ import annotations

import re
from xml.etree.ElementTree import ElementTree

import pandas as pd
from lxml import html

html_page_path = '/home/mehdi/Downloads/Data_Engineer_Scraping_test_-_17-06-21/candidateEvalData/webpage.html'

with open(html_page_path) as f:
    doc_html: ElementTree = html.parse(f)
    art_data: dict[str, str] = {
        'artist_name': doc_html.find('//*[@id="main_center_0_lblLotPrimaryTitle"]')
        .text.split('(')[0]
        .strip(),  # easier to use than regex
        'painting_name': doc_html.find(
            '//*[@id="main_center_0_lblLotSecondaryTitle"]/i',
        ).text,
        'price_gbp': doc_html.find(
            '//*[@id="main_center_0_lblPriceRealizedPrimary"]',
        ).text.strip(),
        'price_us': doc_html.find(
            '//*[@id="main_center_0_lblPriceRealizedSecondary"]',
        ).text,
        'price_gbp_est': doc_html.find(
            '//*[@id="main_center_0_lblPriceEstimatedPrimary"]',
        ).text,
        'price_us_est': re.search(
            re.compile(r'\((?P<us_est>.*?)\)'),
            doc_html.find(
                '//*[@id="main_center_0_lblPriceEstimatedSecondary"]',
            ).text,
        ).group('us_est'),
        'image_link': doc_html.find('//*[@id="imgLotImage"]').attrib['src'],
    }

df = pd.DataFrame(data=art_data, index=[0])
print(df)
