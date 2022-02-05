import os
import yaml
import string


def load_yaml(f: str) -> dict:
    with open(os.path.join(os.getcwd(), f), "r") as fh:
        return yaml.safe_load(fh)


def format_timedelta(tdelta, fmt):
    # https://stackoverflow.com/a/17847006/4180176

    periods = {'D': 86400, 'H': 3600, 'M': 60, 'S': 1}

    f = string.Formatter()
    d = {}
    k = list(map(lambda x: x[1], list(f.parse(fmt))))
    rem = int(tdelta.total_seconds())

    for i in ('D', 'H', 'M', 'S'):
        if i in k and i in periods.keys():
            d[i], rem = divmod(rem, periods[i])

    return f.format(fmt, **d)