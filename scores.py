import scrapy
import json
from datetime import datetime, timedelta

class ScoresSpider(scrapy.Spider):
    name = 'Scores'
    start_urls = ['https://www.placardefutebol.com.br/brasileirao-serie-a']

    def parse(self, response):
        elements = response.css('a.match__md')
        data = []
        for game in elements:
            teams = game.css('div.text::text').getall()
            scores = game.css('b::text').getall()
            
            item = {
                'teamA': teams[0],
                'teamB': teams[1],
                'scoreA': int(scores[0]) if len(scores) > 1 else None,
                'scoreB': int(scores[1]) if len(scores) > 1 else None,
             
            }
            data.append(item)

        print(data)

        with open('scores.json', 'w') as file:
            json.dump(data, file)

        self.log('JSON file created.')
