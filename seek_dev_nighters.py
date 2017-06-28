import requests
from multiprocessing import Pool
from itertools import chain
import pytz
import datetime


def acquire_urls():
    url = 'https://devman.org/api/challenges/solution_attempts/?page=1'
    parsed_page = requests.get(url).json()
    number_of_pages = parsed_page['number_of_pages']
    return ['{}{}'.format(url, number) for number in range(1, number_of_pages)]


def get_page(url):
    page = requests.get(url).json()
    return page['records']


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
    time_comparison = time_is_in_range(start, end, user_time) if user_time else None
    return time_comparison if bool(time_comparison) else None
    # return time_comparison if time_comparison is True else None


def count_users():
    urls = acquire_urls()
    print(urls)
    lists_of_records = parallel_computing(get_page, urls)
    concatenated_list = list(chain.from_iterable(lists_of_records))
    checked_users = parallel_computing(get_midnighter, concatenated_list)
    return len([user for user in checked_users if user is True])


if __name__ == '__main__':
    print('There are {} night owls on the DEVMAN web site.'.format(count_users()))
