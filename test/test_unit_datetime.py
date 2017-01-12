#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012-2017 Snowflake Computing Inc. All right reserved.
#
import time
from datetime import datetime

from snowflake.connector import sfdatetime


def test_basic_datetime_format():
    """
    Datetime format basic
    """
    # date
    value = datetime(2014, 11, 30)
    formatter = sfdatetime.SnowflakeDateTimeFormat(u'YYYY-MM-DD')
    assert formatter.format(value) == u'2014-11-30'

    # date time => date
    value = datetime(2014, 11, 30, 12, 31, 45)
    formatter = sfdatetime.SnowflakeDateTimeFormat(u'YYYY-MM-DD')
    assert formatter.format(value) == u'2014-11-30'

    # date time => date time
    value = datetime(2014, 11, 30, 12, 31, 45)
    formatter = sfdatetime.SnowflakeDateTimeFormat(
        u'YYYY-MM-DD"T"HH24:MI:SS')
    assert formatter.format(value) == u'2014-11-30T12:31:45'

    # date time => date time in microseconds with 4 precision
    value = datetime(2014, 11, 30, 12, 31, 45, microsecond=987654)
    formatter = sfdatetime.SnowflakeDateTimeFormat(
        u'YYYY-MM-DD"T"HH24:MI:SS.FF4')
    assert formatter.format(value) == u'2014-11-30T12:31:45.9876'

    # date time => date time in microseconds with full precision up to
    # microseconds
    value = datetime(2014, 11, 30, 12, 31, 45, microsecond=987654)
    formatter = sfdatetime.SnowflakeDateTimeFormat(
        u'YYYY-MM-DD"T"HH24:MI:SS.FF')
    assert formatter.format(value) == u'2014-11-30T12:31:45.987654'


def test_datetime_format_negative():
    u"""Datetime format negative"""
    value = datetime(2014, 11, 30, 12, 31, 45, microsecond=987654)
    formatter = sfdatetime.SnowflakeDateTimeFormat(
        u'YYYYYYMMMDDDDD"haha"hoho"hihi"H12HHH24MI')
    assert formatter.format(value) == u'20141411M3030DhahaHOHOhihiH1212H2431'


def test_struct_time_format():
    value = time.strptime("30 Sep 01 11:20:30", "%d %b %y %H:%M:%S")
    formatter = sfdatetime.SnowflakeDateTimeFormat(
        u'YYYY-MM-DD"T"HH24:MI:SS.FF')
    assert formatter.format(value) == '2001-09-30T11:20:30'

    value = sfdatetime.SnowflakeDateTime(
        time.strptime("30 Sep 01 11:20:30", "%d %b %y %H:%M:%S"), nanosecond=0
    )
    assert formatter.format(value) == '2001-09-30T11:20:30.000000'