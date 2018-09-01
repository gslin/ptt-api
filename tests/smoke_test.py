#!/usr/bin/env python3

import bottle
import ptt_api

class smoke_test:
    def test_index(self):
        try:
            ptt_api.index()
        except bottle.HTTPResponse:
            assert True
            return

        assert False

    def test_robotstxt(self):
        ptt_api.robotstxt()
