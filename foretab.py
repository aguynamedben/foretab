#!/usr/bin/python

# -*- coding: utf-8 -*-
#
# foretab.py
#
# Copyright 2009 Ben Standefer. All rights reserved.
# Author: Ben Standefer <benstandefer@gmail.com>
#

from datetime import datetime, timedelta

def parse_field(entry_type, text):
    full_ranges = {
        'm': range(60),
        'h': range(24),
        'dom': range(1, 32),
        'mon': range(1, 13),
        'dow': range(7),
    }
    range_exception_messages = {
        'm': 'Each minute value must be between 0 and 59',
        'h': 'Each hour value must be between 0 and 23',
        'dom': 'Each dom value must be between 1 and 31',
        'mon': 'Each mon value must be between 1 and 12',
        'dow': 'Each dow value must be between 0 and 6',
    }
    if text == '*':
        return full_ranges[entry_type]
    else:
        values_set = set()
        comma_separated_list = text.split(',')
        for comma_separated_string in comma_separated_list:
            if '-' in comma_separated_string:
                pass
                if comma_separated_string.count('-') > 1:
                    raise Exception('You can only have 1 hyphen (-) per range field')
                (range_low, range_high) = comma_separated_string.split('-')
                range_low, range_high = int(range_low), int(range_high)
                if range_low > range_high:
                    raise Exception('Range low must be lower than range high')
                if range_low not in full_ranges[entry_type] or range_high not in full_ranges[entry_type]:
                    raise Exception(range_exception_messages[entry_type])
                i = range_low
                while i <= range_high:
                    values_set.add(i)
                    i += 1
            else:
                value = int(comma_separated_string)
                if value not in full_ranges[entry_type]:
                    raise Exception(range_exception_messages[entry_type])
                values_set.add(value)

        values_list = list(values_set)
        values_list.sort()

        return values_list


def get_dates_for_entry(entry, start_date='2010-02-17', end_date='2010-02-25'):
    dates = []

    (m, h, dom, mon, dow) = entry

    positives = {
        'm': parse_field('m', h),
        'h': parse_field('h', h),
        'dom': parse_field('dom', dom),
        'mon': parse_field('mon', mon),
        'dow': parse_field('dow', dow),
    }

    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    index_date = start_date

    while index_date <= end_date:
        if index_date.month in positives['mon']:
            if dom == '*' and dow == '*':
                # both day fields are wildcard, everyday
                for hour in positives['h']:
                    for minute in positives['m']:
                        dates.append(datetime(index_date.year, index_date.month, index_date.day, hour, minute))
            elif dom == '*' and dow != '*':
                # dow is dominant day field
                if index_date.weekday() in positives['dow']:
                    for hour in positives['h']:
                        for minute in positives['m']:
                            dates.append(datetime(index_date.year, index_date.month, index_date.day, hour, minute))
            elif dom != '*' and dow == '*':
                # dom is dominant day field
                if index_date.day in positives['dom']:
                    for hour in positives['h']:
                        for minute in positives['m']:
                            dates.append(datetime(index_date.year, index_date.month, index_date.day, hour, minute))
            else:
                # both day fields are restricted, check for either occurance
                if index_date.day in positives['dom'] or index_date.weekday() in positives['dow']:
                    for hour in positives['h']:
                        for minute in positives['m']:
                            dates.append(datetime(index_date.year, index_date.month, index_date.day, hour, minute))
        index_date += timedelta(days=1) 
    return dates
