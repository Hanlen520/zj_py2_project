# -*- coding: utf-8 -*-
import unittest
import urllib2
import json

HOST="http://ott-api.fun.tv/market-api/tomato/monkey_test_main/v1"

class Response():
    def __init__(self, test, js):
        ret = json.loads(js)

        retCode = ret['retCode']
        test.assertEqual(retCode, 200)

        self.raw_rsp = ret
        self.cols = ret['columnInfos']

def post(test, param):
    p = json.dumps(param)
#     print(p)  # json to be post
    req = urllib2.Request(HOST, p)
    ret = urllib2.urlopen(req).read()
#     print(ret)  # response json
    return Response(test, ret)

special = (2144, 2164, 2201, 2173, 2160, 2153, 2078, 2192, 2182, 2183)  # show nominated APPs, not config
offical = (2157, 2166, 2095, 2)  # show all APPs
# show APPs depend on local APPs
promote = (2093, 2094, 2052, 2097, 2130, 2109, 2112, 2194, 2062, 2063, 2133, 2134, 2132, 2131, 2096, 2142, 2056, 2079, 2077, 2102, 2103, 2111)
restricted = (2159, 2202)  # only show limited APPs
# vieira = (2093, 2094)

tests = [
    {
        'doc': 'Test special channel, expect special packages',
        'channel': special,
        'extra_params': {'packageNames': ['net.myvst.v2']},
        'has_x_channel': False,
    },
    {
        'doc': 'Test offical channel, expect full packages',
        'channel': offical,
        'extra_params': {'packageNames': ['tv.fun.master']},
        'has_x_channel': False,
    },
    {
        'doc': 'Test promote channel, with normal package, expect restrict content',
        'channel': promote,
        'extra_params': {'packageNames': ['tv.fun.master']},
        'has_x_channel': False,
    },
    {
        'doc': 'Test promote channel, with cracked package, expect full content',
        'channel': promote,
        'extra_params': {'packageNames': ['net.myvst.v2']},
        'has_x_channel': True,
    },
    {
        'doc': 'Test promote channel, with mixed packages, expect full content',
        'channel': promote,
        'extra_params': {'packageNames': ['tv.fun.master', 'net.myvst.v2']},
        'has_x_channel': True,
    },
    {
        'doc': 'Test promote channel, with no package, expect restrict content',
        'channel': promote,
        'extra_params': {'packageNames': []},
        'has_x_channel': False
    }
#     {
#         'doc': 'my test',
#         'channel': vieira,
#         'extra_params': {'packageNames': ['net.myvst.v2']},
#         'has_x_channel': True
#     }
]

class TestChannel(unittest.TestCase):
    def test_channel(self):
        for t in tests:
            self.do_test(t)

    def do_test(self, test):
        if 'doc' in test:
            print "[***] " + test['doc']
        for channel in test['channel']:
            print '\t Test channel:' + str(channel)
            param = {'channel_id': channel}
            if 'extra_params' in test:
                extra_params = test['extra_params']
                for p in extra_params:
                    param[p] = extra_params[p]
                    
            rsp = post(self, param)
            has_x_channel = test['has_x_channel']
            real_x_channel = 'XChannelId'  in rsp.raw_rsp
            self.assertEqual(has_x_channel, real_x_channel)
                
if __name__ == '__main__':
    unittest.monkey_test_main()
    pass
