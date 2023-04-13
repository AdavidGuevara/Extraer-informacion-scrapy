import scrapy
import datetime


class DaneScrapingSpider(scrapy.Spider):
    name = "dane_scraping"
    allowed_domains = ["www.dane.gov.co"]
    start_urls = ["http://www.dane.gov.co/index.php/indicadores-economicos"]
    custom_settings = {
        "FEED_URI": "indicadores_dane.csv",
        "FEED_FORMAT": "csv",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def parse(self, response):
        titulos = response.xpath('//h2[@style="text-align: center;"]')
        precios = response.xpath(
            '//div[@class="col-sm-4"]/table[@style="border-color: #cfcfcf; width: 100%;" and @border="1"]/tbody/tr/td'
        )

        titulos_list = list()
        for titulo in titulos:
            if titulo.xpath("./span/a/strong/text()").get():
                titulos_list.append(titulo.xpath("./span/a/strong/text()").get())
            else:
                titulos_list.append(titulo.xpath("./strong[1]/text()").get())

        precios_list = list()
        for precio in precios:
            if precio.xpath("./h1/span/text()").get():
                precios_list.append(precio.xpath("./h1/span/text()").get())
            elif precio.xpath("./h1/strong/a/text()").get():
                precios_list.append(precio.xpath("./h1/strong/a/text()").get())
            else:
                precios_list.append(precio.xpath("./h1/text()").get())

        for titulo, precio in zip(titulos_list, precios_list):
            yield {"titulo": titulo, "precio": precio, "fecha": datetime.date.today()}
