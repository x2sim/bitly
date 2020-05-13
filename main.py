import sys
import requests
import os
from dotenv import load_dotenv
import argparse


def create_parser():
    parser = argparse.ArgumentParser(prog='bitlink',
        description = '''Программа делает ссылки короткими, либо указывает количество переходов по короткой ссылке''',
        epilog = '''(c) Александр Дубков 2020.'''
    )
    parser.add_argument('--link', '-l', help = 'Ссылка')
    return parser

def shorten_link(token, link):
    url = 'https://api-ssl.bitly.com/v4/shorten'
    json = {'long_url': link}
    headers = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.post(url, json=json, headers=headers)
    response.raise_for_status()
    short_link = response.json()['id']
    return short_link

def count_clicks(token, link):
    url = \
        'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(link)
    headers = {'Authorization': 'Bearer {}'.format(token)}
    payload = {'units': '-1'}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


if __name__ == '__main__':
    load_dotenv()
    TOKEN_FOR_BITLINK = os.getenv('BITLINK_TOKEN')
    parser = create_parser()
    arguments_of_argparse = parser.parse_args()
    url = arguments_of_argparse.link
    if url.startswith('bit.ly/'):
        try:
            total_clicks = count_clicks(TOKEN_FOR_BITLINK, url)
        except requests.exceptions.HTTPError:
            print("Ссылка не корректная")
        else:
            print("По вашей ссылке прошли {} раз(а)".format(total_clicks))
    else:
        try:
            short_link = shorten_link(TOKEN_FOR_BITLINK, url)       
        except requests.exceptions.HTTPError:
            print("Ссылка не корректная")
        else:
            print("Короткая ссылка: {}".format(short_link))
