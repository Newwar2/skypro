import pytest
from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(test_my_list):
    assert filter_by_state(test_my_list) ==  [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ]

    assert filter_by_state(test_my_list,"CANCELED") == [
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

def test_sort_by_date(test_my_list):
    assert sort_by_date(test_my_list) == [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]
    assert sort_by_date(test_my_list, False) == [{'date': '2018-10-14T08:21:33.419441', 'id': 615064591, 'state': 'CANCELED'},
 {'date': '2019-07-03T18:35:29.512364', 'id': 41428829, 'state': 'EXECUTED'}]
