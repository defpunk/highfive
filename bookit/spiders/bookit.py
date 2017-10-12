import scrapy


class BookIt(scrapy.Spider):
    name = 'bookit'
    start_urls = ['https://hm.highfive.nl/login/osterley-health-and-fitness?lang=en']
    download_delay = 1.5

    def parse(self, response):
        print "USER_NAME" + self.settings.get('USER_NAME')
        print "PASSWORD" + self.settings.get('PASSWORD')
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'ctl00$cp1$password': self.settings.get('PASSWORD'), 'ctl00$cp1$userid': self.settings.get('USER_NAME')},
            callback=self.parse_results
        )

    def parse_results(self, response):

        for row in response.css("tr.tablesubrow"):
            classname = row.xpath("@class").extract_first()
            if 'tablesubrow' == classname:
                cells = row.xpath(".//td")
                time = cells[0].xpath(".//text()").extract_first()[2:]
                type = cells[1].xpath(".//text()").extract_first()
                if time == self.settings.get('CLASS_TIME') and type == self.settings.get('CLASS_NAME'):
                    print "matched " + time + " " + type
                    bookable = cells[3].xpath("@class").extract_first() == "reserveerknop"
                    if bookable:
                        relpath = cells[3].xpath(".//a/@href").extract_first()[2:]
                        path = "https://hm.highfive.nl/hmuser" + relpath
                        yield response.follow(path, callback=self.parse_booked)

    def parse_booked(self, response):
        print response
