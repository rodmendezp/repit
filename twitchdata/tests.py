from rest_framework.serializers import BaseSerializer
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
from django.utils import timezone
from .models import *
from .views import *


# Base class for testing rest api for a single model
# Right now it does not support nested models
# For now that I am not able to not run RestAPITestCase tests it will run N extra test
# TODO: Add test case to update using another id of nested model
# TODO: Add support for update deep nested models (grandsons, not only children)
# TODO: Test adding multiple objects at once
# TODO: Test unique fields
class BaseTestCase:
    class RestAPITestCase(APITestCase):
        def __init__(self, methodName='No test'):
            self.model = None
            self.serializer = None
            self.view_list = None
            self.view_detail = None
            self.data = None
            self.modified_data = None
            self.nested = False
            self.url = None
            super().__init__(methodName)

        def setUp(self):
            if self.__class__ is not BaseTestCase.RestAPITestCase:
                self.assertEqual(self.check_info(), True)
            super().setUp()

        def check_info(self):
            not_defined = None
            if not self.model:
                not_defined = 'Model'
            if not self.serializer:
                not_defined = 'Serializer'
            if not self.view_list:
                not_defined = 'List View'
            if not self.view_detail:
                not_defined = 'Detail View'
            if not self.data:
                not_defined = 'Data'
            if not self.modified_data:
                not_defined = 'Modified Data'
            if not self.url:
                not_defined = 'URL'
            if not_defined:
                print('%s for TestCase %s is not defined' % (not_defined, self.__class__))
                return False
            return True

        def add_object(self, data):
            return self.client.post(self.url, data, format='json')

        def remove_last_object(self):
            obj = self.model.objects.last()
            return self.client.delete(self.url + str(obj.id))

        def get_object(self, pk):
            return self.client.get(self.url + str(pk))

        def deep_remove_ids(self, data):
            has_id = False
            for key, value in data.items():
                if isinstance(value, dict):
                    self.deep_remove_ids(value)
                if key == 'id':
                    has_id = True
            if has_id:
                del data['id']

        def test_add_object(self, prev_count=0):
            response = self.add_object(self.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(self.model.objects.count(), prev_count + 1)

        def test_get_detail_object(self):
            self.test_add_object()
            self.assertEqual(self.model.objects.count(), 1)
            obj = self.model.objects.last()
            response = self.client.get(self.url + str(obj.id))
            self.deep_remove_ids(response.data)
            self.assertEqual(response.data, self.data)

        def test_get_list_objects(self):
            self.test_add_object()
            self.test_add_object(self.model.objects.count())
            response = self.client.get(self.url)
            self.assertEqual(len(response.data), 2)

        def test_delete_object(self):
            self.test_add_object()
            response = self.remove_last_object()
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            self.assertEqual(self.model.objects.count(), 0)

        def test_update_object(self):
            self.test_add_object()
            obj = self.model.objects.last()
            response = self.client.put(self.url + str(obj.id), self.modified_data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.deep_remove_ids(response.data)
            self.assertEqual(response.data, self.modified_data)

        # It will add data and modified data to the database
        # Will change the nested object of data to the nested object of modified_data
        def test_update_nested_id(self):
            if not self.nested:
                return
            self.add_object(self.data)
            self.add_object(self.modified_data)
            instance = self.model.objects.first()
            # Get nested model field
            nested_serializer = dict(self.serializer._declared_fields).popitem()[1]
            nested_model = nested_serializer.Meta.model
            nested_name = nested_model._meta.verbose_name
            # Get last nested object added (should be the one from modified_data)
            nested_instance = nested_model.objects.first()
            nested_modified_instance = nested_model.objects.last()
            self.assertEqual(nested_instance.id + 1, nested_modified_instance.id)
            for field in nested_serializer._writable_fields:
                if isinstance(field, BaseSerializer):
                    continue
                self.assertEqual(self.modified_data[nested_name][field.source], nested_modified_instance.__dict__[field.source])
            # change nested field in data to id of nested object of modified data
            data_modified_nested_id = self.data
            data_modified_nested_id[nested_name] = {'id': nested_modified_instance.id}
            # assign the proper id to the other nested fields
            for key, nested_field in dict(self.serializer._declared_fields).items():
                if key == nested_name:
                    continue
                data_modified_nested_id[key] = {'id': instance.__dict__[key + '_id']}
            response = self.client.put(self.url + str(instance.id), data_modified_nested_id, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)


        # def test_add_multiple_objects(self):
        #     data = [self.data, self.modified_data]
        #     response = self.client.post(self.url, data, format='json')
        #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #     self.assertEqual(self.model.objects.count(), 2)


# class TwitchUserRestAPITest(BaseTestCase.RestAPITestCase):
#     def setUp(self):
#         self.model = TwitchUser
#         self.serializer = TwitchUserSerializer
#         self.view_list = TwitchUserList
#         self.view_detail = TwitchUserDetail
#         self.data = {
#             'twid': 123456,
#             'name': 'raidrix',
#         }
#         self.modified_data = {
#             'twid': 654321,
#             'name': 'no_raidrix'
#         }
#         self.url = '/twitchdata/twitch_user/'
#         super().setUp()


# class ChannelRestAPITest(BaseTestCase.RestAPITestCase):
#     def setUp(self):
#         self.model = Channel
#         self.serializer = ChannelSerializer
#         self.view_list = ChannelList
#         self.view_detail = ChannelDetail
#         self.data = {
#             'twid': 12345,
#         }
#         self.modified_data = {
#             'twid': 54321,
#         }
#         self.url = '/twitchdata/channel/'
#         super().setUp()


# class StreamerRestAPITest(BaseTestCase.RestAPITestCase):
#     def setUp(self):
#         self.model = Streamer
#         self.serializer = StreamerSerializer
#         self.view_list = StreamerList
#         self.view_detail = StreamerDetail
#         self.data = {
#             'twitch_user': {
#                 'twid': 12345,
#                 'name': 'raidrix',
#             },
#             'channel': {
#                 'twid': 12345,
#             }
#         }
#         self.modified_data = {
#             'twitch_user': {
#                 'twid': 54321,
#                 'name': 'no_raidrix',
#             },
#             'channel': {
#                 'twid': 54321,
#             },
#         }
#         self.nested = True
#         self.url = '/twitchdata/streamer/'
#         super().setUp()


class VideoRestAPITest(BaseTestCase.RestAPITestCase):
    def setUp(self):
        self.model = Video
        self.serializer = VideoSerializer
        self.view_list = VideoList
        self.view_detail = VideoDetail
        self.data = {
            'twid': 12345,
            'streamer': {
                'twitch_user': {
                    'twid': 12345,
                    'name': 'raidrix',
                },
                'channel': {
                    'twid': 12345,
                },
            },
            'game': {
                'twid': 12345,
                'name': 'PUBG'
            },
            'recorded': datetime.now(),
            'length': str(datetime.now().time()),
        }
        self.modified_data = {
            'twid': 54321,
            'streamer': {
                'twitch_user': {
                    'twid': 54321,
                    'name': 'no_raidrix',
                },
                'channel': {
                    'twid': 54321,
                }
            },
            'game': {
                'twid': 54321,
                'name': 'no_PUBG',
            },
            'recorded': timezone.now(),
            'length': timezone.now().time(),
        }
        self.nested = True
        self.url = '/twitchdata/video/'
        super().setUp()


# class GameRestAPITest(BaseTestCase.RestAPITestCase):
#     def setUp(self):
#         self.model = Game
#         self.serializer = GameSerializer
#         self.view_list = GameList
#         self.view_detail = GameDetail
#         self.data = {
#             'twid': 12345,
#             'name': 'PUBG'
#         }
#         self.modified_data = {
#             'twid': 12345,
#             'name': 'no_PUBG'
#         }
#         self.url = '/twitchdata/game/'
#         super().setUp()
