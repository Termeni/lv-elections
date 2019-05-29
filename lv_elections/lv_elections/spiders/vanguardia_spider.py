import scrapy

class VanguardiaSpider(scrapy.Spider):
    name = "vanguardia"

    def start_requests(self):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        urls = [
            'https://www.lavanguardia.com/elecciones/elecciones-europeas-2019/cataluna'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=headers, callback=self.parseCat)

    def parseCat(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results_tables = response.css("table.table tbody")
        global_results = results_tables[0].css("td::text").getall()
        dict_results = dict(zip(global_results[::2], global_results[1::2]))
        votes = results_tables[2].css("td::text").getall()
        dict_votes = dict(zip(votes[1::6], votes[2::6]))
        dict_results['level'] = 'CA'
        dict_results['name'] = response.url.split('/')[-1]
        dict_results['votes'] = dict_votes
        yield dict_results
        for next_page in response.css("ul.column-list a::attr('href')").getall():
            yield scrapy.Request(next_page, headers=headers, callback=self.parseProvincia)

    def parseProvincia(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results_tables = response.css("table.table tbody")
        global_results = results_tables[0].css("td::text").getall()
        dict_results = dict(zip(global_results[::2], global_results[1::2]))
        votes = results_tables[2].css("td::text").getall()
        dict_votes = dict(zip(votes[1::6], votes[2::6]))
        dict_results['level'] = 'provincia'
        dict_results['name'] = response.url.split('/')[-1]
        dict_results['votes'] = dict_votes
        yield dict_results
        for next_page in response.css("ul.column-list a::attr('href')").getall():
            yield scrapy.Request(next_page, headers=headers, callback=self.parseMunicipi)

    def parseMunicipi(self, response):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}
        results_tables = response.css("table.table tbody")
        global_results = results_tables[0].css("td::text").getall()
        dict_results = dict(zip(global_results[::2], global_results[1::2]))
        votes = results_tables[2].css("td::text").getall()
        dict_votes = dict(zip(votes[1::6], votes[2::6]))
        dict_results['level'] = 'municipi'
        dict_results['name'] = response.url.split('/')[-1]
        dict_results['votes'] = dict_votes
        yield dict_results
