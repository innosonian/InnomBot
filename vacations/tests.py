from collections import OrderedDict

from django.test import TestCase
from . import views


class User():
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class Vacation:
    def __init__(self, user=None, start_date=None, end_date=None, message=None, created_at=None, deleted_at=None):
        self.user = user
        self.start_date = start_date
        self.end_date = end_date
        self.message = message
        self.created_at = created_at
        self.deleted_at = deleted_at


class AnimalTestCase(TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_hello(self):
        data = [OrderedDict([('id', 3), ('created_at', '2022-11-25T07:02:40Z'), ('start_date', '2022-11-25T07:02:43Z'),
                             ('end_date', '2022-11-25T07:02:45Z'), ('message', 'dd'),
                             ('deleted_at', '2022-11-25T07:02:50Z'),
                             ('user', 'U04ARD6H3PU')]),
                OrderedDict(
                    [('id', 4), ('created_at', '2022-11-25T07:02:58Z'), ('start_date', '2022-11-25T07:03:02Z'),
                     ('end_date', '2022-11-26T07:03:05Z'), ('message', 'ddd'), ('deleted_at', '2022-11-25T07:03:10Z'),
                     ('user', 'U04ARD6H3PU')]),
                OrderedDict(
                    [('id', 5), ('created_at', '2022-11-28T01:58:44Z'), ('start_date', '2022-11-28T01:58:51Z'),
                     ('end_date', '2023-01-01T01:59:04Z'), ('message', 'ㅇㅇㅇ'), ('deleted_at', '2022-11-28T01:59:10Z'),
                     ('user', 'U04ARD6H3PU')]),
                OrderedDict(
                    [('id', 6), ('created_at', '2022-11-28T03:07:20Z'), ('start_date', '2022-12-01T03:07:30Z'),
                     ('end_date', '2022-12-01T03:07:39Z'), ('message', 'dd'), ('deleted_at', '2022-11-28T03:07:42Z'),
                     ('user', 'U04ARD6H3PU')])]

        vacation_api = views.VacationAPI()
        user = User(1, "Ria")
        result = vacation_api.generate_from_data(data, user)
        expected = {"response_type": "in_channel",
                    'attachments':
                        [{'color': '#2eb886',
                          'blocks':
                                [{'type': 'section',
                                  'text': {'text': '*Ria* 님의 휴가 사용 내역: 총 *4* 건, 사용 일수: 총 *39* 일',
                                           'type': 'mrkdwn'},
                                  },
                                 {'type': 'divider'},
                                 {'type': 'section',
                                  'accessory': {'type': 'button',
                                                'text': {'type': 'plain_text',
                                                         'text': '사용완료'}
                                                },
                                  'text': {'type': 'mrkdwn',
                                           'text': '2022-11-25(금) - 1day'}
                                  },
                                  {'type': 'section',
                                   'accessory': {'type': 'button',
                                                 'text': {'type': 'plain_text',
                                                          'text': '사용완료'}
                                                 },
                                   'text': {'type': 'mrkdwn',
                                            'text': '2022-11-25(금) ~ 2022-11-26(토) - 2days'}
                                   },
                                   {'type': 'section',
                                    'accessory': {'type': 'button',
                                                  'text': {'type': 'plain_text',
                                                           'text': '사용완료'}
                                                  },
                                    'text': {'type': 'mrkdwn',
                                             'text': '2022-11-28(월) ~ 2023-01-01(일) - 35days'}
                                    },
                                    {'type': 'section',
                                     'accessory': {'type': 'button',
                                                   'text': {'type': 'plain_text',
                                                            'text': '사용대기'},
                                                   'style': 'primary'
                                                   },
                                     'text': {'type': 'mrkdwn',
                                              'text': '2022-12-01(목) - 1day'}
                                     }
                                    ],
                                }
                         ],
                    }

        self.assertEquals(expected, result)






