from send_message import send_message
from datetime import date


def send_katie_paid() -> None:
    send_message(f"day {(date.today() - date(2021, 5, 10)).days} since mc started her job and not getting paid by osu")


if __name__ == '__main__':
    send_katie_paid()
