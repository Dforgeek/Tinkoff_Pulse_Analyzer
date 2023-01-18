import datetime


def month_number(month: str) -> int:
    months = {
        'янв': 1,
        'фев': 2,
        'мар': 3,
        'апр': 4,
        'мая': 5,
        'июн': 6,
        'июл': 7,
        'авг': 8,
        'сен': 9,
        'окт': 10,
        'ноя': 11,
        'дек': 12
    }
    return months[month[0:3]]


def string_to_date(date_str: str) -> datetime:
    post_date = date_str.split()
    now = datetime.datetime.now()
    hour = int(post_date[-1].split(":")[0])
    minute = int(post_date[-1].split(":")[1])

    if len(post_date) == 5:
        date = datetime.datetime(int(post_date[2]), month_number(post_date[1]), int(post_date[0]), hour, minute)
    elif post_date[0] == "Вчера":
        date = datetime.datetime(now.year, now.month, now.day - 1, hour, minute)
    else:
        date = datetime.datetime.now()
    return date

