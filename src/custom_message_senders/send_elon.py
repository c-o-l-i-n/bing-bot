import logging
import requests
from bs4 import BeautifulSoup as bs
from send_message import send_message


def send_elon() -> None:
    # scrape web data
    logging.info('Scraping Elon Musk net worth data from Forbes')
    webpage = requests.get('https://api.allorigins.win/raw?url=https://www.forbes.com/profile/elon-musk/')
    webcontent = webpage.content
    htmlcontent = bs(webcontent, 'html.parser')

    # get amount of net worth change
    net_worth_change_text = htmlcontent.find(
        'div', {'class': 'profile-info__item-diff'}).text
    print(net_worth_change_text)
    space_index = net_worth_change_text.find(' ')
    net_worth_change = net_worth_change_text[1:space_index - 1]

    amount_map = {
        'k': 'thousand',
        'm': 'million',
        'b': 'billion'
    }

    amount_text = amount_map[net_worth_change_text[space_index - 1].lower()]

    # see if increased or decreased
    net_worth_increased = htmlcontent.find(
        'div', {'class': 'profile-info__item-flag--up'}) != None

    # assemble message text
    message_text = f'elon musk is ${net_worth_change} {amount_text} {"richer" if net_worth_increased else "poorer"} today than he was yesterday'

    # send message
    send_message(message_text)


if __name__ == '__main__':
    send_elon()
