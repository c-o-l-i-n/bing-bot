import yfinance as yf
import math
from send_message import send_message
import fix_path


def millify(n):
    millnames = ['', ' thousand', ' million', ' billion', ' trillion']

    n = float(n)
    millidx = max(0, min(len(millnames)-1,
                         int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def bezos():
    amazon = yf.Ticker('AMZN')
    last_2_days_prices = tuple(
        dict(amazon.history(period="2d")['Close']).values())

    net_worth_difference = (
        last_2_days_prices[1] - last_2_days_prices[0]) * 54_000_000

    send_message(
        f'jeff bezos is ${millify(abs(net_worth_difference))} {"richer" if net_worth_difference >= 0 else "poorer"} today than he was yesterday')


if __name__ == '__main__':
    bezos()
