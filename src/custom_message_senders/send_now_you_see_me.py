from send_message import send_message
from datetime import date


def send_now_you_see_me() -> None:
    send_message(f"ya know mark, today would have been day {(date.today() - date(2020, 2, 13)).days + 1} of watching Now You See Me if you weren't a quitter")


if __name__ == '__main__':
    send_now_you_see_me()