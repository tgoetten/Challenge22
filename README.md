Code Challenge 22 - Packt Free Ebook Web Scraper
* https://pybit.es/codechallenge22.html

# The Challenge
The challenge is to make a script that scrapes the free learning link every day for meta data about the book (title, description, cover, promo time left).

Then have the script share this info together with an affiliation link to your favorite channel: email, Twitter, Facebook, reddit, slack, etc.


# Prerequisits
Get the virtual environment running
  mkvirtualenv -p /usr/bin/python2.7 challenge22

Activate virtualenv
  workon challenge22

Install dependencies
  pip install -r requirements.txt

Export the "Bot User OAuth Access Token"
  export SLACK_BOT_TOKEN='your bot user access token here'

Make sure the bot has at least the following security permissions
* https://api.slack.com/apps/AEHGKML7M/oauth?success=1
  bot
  channels:read
  chat:write:bot
  chat:write:user

# Using Scrapy
Title
>>> response.xpath('//*[@id="deal-of-the-day"]/div/div/div[2]/div[2]/h2/text()').extract()
