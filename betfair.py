import scrapy
import json
from datetime import datetime, timedelta

class BetfairSpider(scrapy.Spider):
    name = 'betfair'
    start_urls = ['https://www.betfair.com/sport/football/brasileiro-s%C3%A9rie-a/13']

    def parse(self, response):
        ul_elements = response.css('ul.event-list > li')
        print(ul_elements)
        data = []
        current_year = datetime.now().year
        for ul in ul_elements:
            team = [t.strip() for t in ul.css('span.team-name::text').getall()]
            date = [p.strip() for p in ul.css('span.ui-countdown::text').getall()]
            start_date = self.fix_date(date, current_year)
            end_date = start_date + timedelta(hours=2)
            oddsA = float([p.strip() for p in ul.css('div.market-3-runners li.sel-0 span::text').getall()][0])
            oddsDraw = float([p.strip() for p in ul.css('div.market-3-runners li.sel-1 span::text').getall()][0])
            oddsB = float([p.strip() for p in ul.css('div.market-3-runners li.sel-2 span::text').getall()][0])
            # teamA = team[0]
            # teamB = team[1]
            # if team[0].split()[0] == 'Vasco':
            #     teamA = 'Vasco'
        
            # if team[1].split()[0] == 'Vasco':
            #     teamB = 'Vasco'
            item = {
                'teamA': team[0],
                'teamB': team[1],
                # 'test': date[0],
                'startDateTime': start_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
                'endDateTime': end_date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3],
                'oddsA': oddsA,
                'oddsDraw': oddsDraw,
                'oddsB': oddsB,
                'scoreA': None,
                'scoreB': None
            }
            print(data) 
            data.append(item)


        with open('betfair.json', 'w') as file:
            json.dump(data, file)

        self.log('JSON file created.')



    def fix_date(self, date, current_year):
        if not isinstance(date, list):
            return datetime.strptime(datetime.now().strftime("%d %b %H:%M %Y"), "%d %b %H:%M %Y")
        if date[0].strip().startswith('Amanhã'):
            tomorrow = datetime.now() + timedelta(days=1)
            date_fixed = date[0].replace('Amanhã', tomorrow.strftime('%d %b'))
            return datetime.strptime(f"{date_fixed} {current_year}", "%d %b %H:%M %Y")
        else:
            return datetime.strptime(f"{date[0]} {current_year}", "%d %b %H:%M %Y")