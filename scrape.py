import os
import requests
from datetime import datetime

# import of third-party libraries
from bs4 import BeautifulSoup
from slackclient import SlackClient
from dateutil.relativedelta import relativedelta


def send_slack_message(text, channel, attachments=None):
    """
    send a message, using Slack

    use environment variable 'SLACK_BOT_TOKEN' to specifie which workspace to be used
    :param text: the message to be send to the user / channel
    :param channel: the id of channel or the user
    :param attachments: (optional) allows further formatting
    """
    if text and channel:
        # instantiate Slack client
        slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

        slack_client.api_call("chat.postMessage", channel=channel, text=text, attachments=attachments)


def compose_message_for_slack(book_data):
    """
    compose an english message, based on the book_data object and apply slack specific styling
    :param book_data: dictionary with details about the free packt book
    :return: you get the 'text' and the 'attachments' returned
    """
    text = ":tada: A new Packt book is available for free!",

    attachments = [{
        "fallback": "A new Packt book is available for free!",
        "color": '#FD6A02',
        "title": book_data["title"],
        "title_link": "https://www.packtpub.com/packt/offers/free-learning?utm_source=Pybonacci&utm_medium=referral&utm_campaign=FreeLearning2017CharityReferrals",
        "text": book_data["description"] + ".\n \n" + time_left_to_download_the_book(ends=book_data["countdown"]),
        "thumb_url": book_data["image_url"]
    }]

    return text, attachments


def time_left_to_download_the_book(ends, now=None):
    """
    calculates the remaining time before the free ebook offer expires.
    If no current date (now) is provided, we automatically assume it's datetime.today()

    :param ends: datetime object when the offer expires
    :param now: (optional) datetime object to be used as start
    :return: String, sentence that explains how much time there's left
    """
    if not now:
        now = datetime.today()
    try:
        diff = relativedelta(ends, now)
    except ValueError:
        print 'error while calculating the time delta'
        return None

    result = "You have %d days, %d hours, %d minutes and %d seconds left before this offer expires." % (
    diff.days, diff.hours, diff.minutes, diff.seconds)

    if diff.days == 0:
        result = "You have %d hours, %d minutes and %d seconds left before this offer expires." % (
        diff.hours, diff.minutes, diff.seconds)

    return result

def fetch_book_data():
    """
    query the pack website for free books
    :return:
    """
    url = "https://www.packtpub.com/packt/offers/free-learning"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    result = requests.get(url, headers=headers)

    if result.status_code == 200:
        soup = BeautifulSoup(result.content, "html5lib")
    else:
        print 'Stopped processing due to a status code different to 200: {}'.format(result.status_code)
        print(result.content.decode())

    return soup


def parse_book_data(soup_data, verbose=False):
    """
    processes beautioul soup object "soup_data" and extracts relavant information
        -title
        - description
        - image_url
        - countdown

    :param soup_data: beautifoul soup object used to parse the data from
    :param verbose: (optional) set to true to see debug information
    :return: book_data dictionary with book details
    """
    book_data = {
        "title": None,
        "description": None,
        "image_url": None,
        "countdown": None,
    }

    deal_of_the_day_container = soup_data.find('div', {"id": "deal-of-the-day"})

    if deal_of_the_day_container:
        book_data["title"] = soup.find('div', {"class": "dotd-title"}).text.strip()
        image_container = soup.find('div', {"class": "dotd-main-book-image"})

        if image_container:
            image_url = image_container.find_all('img', {"class": "bookimage"})
            book_data["image_url"] = image_url[0]['src']

        summary_container = soup.find('div', {"class": "dotd-main-book-summary"})
        if summary_container:
            book_data["description"] = summary_container.find_all('div')[2].text.strip()

            countdown = summary_container.find('div', {"class": "eighteen-days-countdown-bar"})
            countdown = countdown.span["data-countdown-to"]
            book_data["countdown"] = datetime.fromtimestamp(float(countdown))

    if verbose:
        #log('Here come's the text')
        # def log():
        #   if verbose: print irgendwas
        print 'title: {}'.format(book_data["title"])
        print 'description: {}'.format(book_data["description"])
        print 'image_url: {}'.format(book_data["image_url"])
        print 'countdown: {}'.format(book_data["countdown"])

    return book_data


if __name__ == '__main__':
    # fetch data from website as soup object
    soup = fetch_book_data()
    # second, parse the data, extract relevant book attributes and return dictionary
    book_data = parse_book_data(soup)

    # prepare message
    text, attachments = compose_message_for_slack(book_data)

    # userid (thomas) = "D1P1LGJR5" / channelid (freepacktbook= "CEH4K4RDF"
    send_slack_message(text=text, channel="CEH4K4RDF", attachments=attachments)