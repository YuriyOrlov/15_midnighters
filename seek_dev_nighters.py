import requests
from multiprocessing import Pool
from itertools import chain
import pytz
import datetime


def get_pages(num_of_pages):
    url = 'https://devman.org/api/challenges/solution_attempts/?'
    payload = [{'page': num} for num in num_of_pages]
    pages = [requests.get(url, params=item).json() for item in payload]
    return [page['records'] for page in pages]


def parallel_computing(func, iterable, num_of_parallel_processes=8):
    pool = Pool(num_of_parallel_processes)
    return pool.map(func, iterable)


def get_tz_and_datetime_obj(timezone, timestamp):
    if timestamp:
        client_tz = pytz.timezone(timezone)
        return (datetime.datetime.fromtimestamp(timestamp, client_tz)).time()


def time_is_in_range(start, end, user_time):
    if start <= end:
        return start <= user_time <= end
    else:
        return start <= user_time or user_time <= end


def get_midnighter(item):
    start = datetime.time(0, 00)
    end = datetime.time(6, 00)
    user_time = get_tz_and_datetime_obj(item['timezone'], item['timestamp'])
    return time_is_in_range(start, end, user_time) if user_time else None


def count_users():
    number_of_pages = list(range(1, 11))
    lists_of_records = get_pages(number_of_pages)
    concatenated_list = list(chain.from_iterable(lists_of_records))
    checked_users = parallel_computing(get_midnighter, concatenated_list)
    return len([user for user in checked_users if bool(user)])


if __name__ == '__main__':
    print('There are {} night owls on the DEVMAN web site.'.format(count_users()))
