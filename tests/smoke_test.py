#!/usr/bin/env python3

import bottle
import ptt_api

def test_index():
    try:
        ptt_api.index()
    except bottle.HTTPResponse:
        assert True
        return

    assert False

def test_robotstxt():
    ptt_api.robotstxt()
