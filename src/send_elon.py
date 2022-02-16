import requests
from bs4 import BeautifulSoup as bs
from send_message import send_message


def elon():
    # scrape web data
    webpage = requests.get('https://www.forbes.com/profile/elon-musk/')
    webcontent = webpage.content
    htmlcontent = bs(webcontent, 'html.parser')

    # get amount of net worth change
    net_worth_change_text = htmlcontent.find(
        'div', {'class': 'profile-info__item-diff'}).text
    pipe_index = net_worth_change_text.find('|')
    net_worth_change = net_worth_change_text[1:pipe_index - 3]

    amount_map = {
        'k': 'thousand',
        'm': 'million',
        'b': 'billion'
    }

    amount_text = amount_map[net_worth_change_text[pipe_index - 2].lower()]

    # see if increased or decreased
    net_worth_increased = htmlcontent.find(
        'div', {'class': 'profile-info__item-flag--up'}) != None

    # assemble message text
    message_text = f'elon musk is ${net_worth_change} {amount_text} {"richer" if net_worth_increased else "poorer"} today than he was yesterday'

    # send message
    send_message(message_text)


if __name__ == '__main__':
    elon()
