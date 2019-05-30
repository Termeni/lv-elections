import scrapy

class VanguardiaSpider(scrapy.Spider):
    name = "vanguardia"

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        urls = [
            'https://www.lavanguardia.com/elecciones/elecciones-europeas-2019'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse(self, response):
        depth = response.request.meta['depth']
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results_tables = response.css("table.table tbody")
        global_results = results_tables[0].css("td::text").getall()

        dict_results = dict(zip(global_results[::2], global_results[1::2]))

        votes = results_tables[2].css("td::text").getall()
        dict_votes = dict(zip(votes[1::6], votes[2::6]))

        url_tokens = response.url.split('/')
        dict_results['level'] = depth
        dict_results['name'] = url_tokens[-1]
        dict_results['parent'] = url_tokens[-2]
        dict_results['votes'] = dict_votes

        yield dict_results
        if depth < 3:
            for next_page in response.css("ul.column-list a::attr('href')").getall():
                yield scrapy.Request(next_page, headers=headers, callback=self.parse)
