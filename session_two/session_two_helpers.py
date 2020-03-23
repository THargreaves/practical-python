# -*- coding: utf-8 -*-
"""
Helper functions for the main challenge of session two.

This module implements two helper functions which can be used as part of a
solution to the main challenge of session two. The docstrings of the functions
explain how they should be used. You can either copy the helper functions
directly into your Jupyter/Colab notebook (don't forget the import statements)
or you can import this module (ask me about this if you are interested).

@author: Tim Hargreaves
"""


import re
import requests
from bs4 import BeautifulSoup


def get_celeb_twitters(verbose=True):
    """
    Collect various celebrities' twitter URLs from profilerehab.com.

    Scrapes the contents of profilerehab.com to aquire the twitter URLs of
    several hundred celebrities. The results are returned as a dictionary of
    URLs.

    Warning: If you run this script locally at AZ, you will need to use the
    guest network to avoid having to setup proxy details.

    Args:
        verbose (bool): If `True`, print updates on scraping progress.

    Returns:
        twitter_urls (str): A dictionary of twitter URLs in which the keys are
                the celebrity names and the values are the corresponding URLs.

    Raises:
        TypeError: If `verbose` is not Boolean
    """
    if not isinstance(verbose, bool):
        raise TypeError("verbose must be Boolean")

    # get links to category pages
    res = requests.get('http://profilerehab.com/twitter-help/' +
                       'celebrity_twitter_list')
    soup = BeautifulSoup(res.text, features='lxml')
    content = soup.body.find('div', {'class': 'content'})
    a_tags = content.find_all('a')[:9]
    cat_links = {t.text: t['href'] for t in a_tags}

    twitter_urls = {}
    for cat, l in cat_links.items():
        if verbose:
            print(f"Collecting Twitter Profiles for {cat[:-23]}")
        res = requests.get(l)
        soup = BeautifulSoup(res.text, features='lxml')
        entry = soup.body.find('div', {'id': 'entry'})
        para = entry.find_all('p')
        found = 0
        for p in para:
            if p.find('a', recursive=False) and \
                    p.find('strong', recursive=False):
                # remove possessive form and question marks
                name = re.sub(r'[\?(?:\'s)]*$', '', p.strong.text.strip())
                twitter_urls[name] = p.a['href']
                found += 1
        if verbose:
            print(f"Found {found} Profiles")
    if verbose:
        print(f"\nTotal Profiles Found: {len(twitter_urls)}")

    return twitter_urls


def get_follower_count(url):
    """
    Collect the follower count from a twitter URL.

    Scrapes the a Twitter profile page to find the follower count. If no count
    can be found (e.g. not a valid profile page, profile is deleted, follower
    count is hidden) then `None` is returned.

    Warning: If you run this script locally at AZ, you will need to use the
    guest network to avoid having to setup proxy details.

    Args:
        url (str): The URL of a Twitter profile to get the follower count from.

    Returns:
        follower_count (int/NoneType): The follower count of the profile if
                one is found, otherwise `None`.

    Raises:
        TypeError: If `url` is not a string
    """
    if not isinstance(url, str):
        raise TypeError("url must be a string")

    res = requests.get(url)
    soup = BeautifulSoup(res.text, features='lxml')
    f = soup.find('li', {'class': "ProfileNav-item--followers"})
    if not f:
        return None
    title = f.find('a')['title']
    count = int(title.split()[0].replace(',', ''))
    return count
