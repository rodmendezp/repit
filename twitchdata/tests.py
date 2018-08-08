from rest_framework.test import APITestCase
from rest_framework import status
from .models import *
from .views import *


# Base class for testing rest api for a single model
# Right now it does not support nested models
# For now that I am not able to not run RestAPITestCase tests it will run N extra test
# TODO: Check how to not run base class
# TODO: Add suppport for nested models
class RestAPITestCase(APITestCase):
    def __init__(self, methodName='runTest'):
        self.model = None
        self.serializer = None
        self.view_list = None
        self.view_detail = None
        self.data = None
        self.modified_data = None
        self.url = None
        super().__init__(methodName)

    def setUp(self):
        if self.__class__ is not RestAPITestCase:
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

    def add_object(self):
        return self.client.post(self.url, self.data, format='json')

    def remove_last_object(self):
        obj = self.model.objects.last()
        return self.client.delete(self.url + str(obj.id))

    def test_add_object(self, prev_count=0):
        if self.__class__ is RestAPITestCase:
            return
        response = self.add_object()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.model.objects.count(), prev_count + 1)

    def test_get_detail_object(self):
        if self.__class__ is RestAPITestCase:
            return
        self.test_add_object()
        self.assertEqual(self.model.objects.count(), 1)
        obj = self.model.objects.last()
        response = self.client.get(self.url + str(obj.id))
        self.assertEqual(response.data, self.data)

    def test_get_list_objects(self):
        if self.__class__ is RestAPITestCase:
            return
        self.test_add_object()
        self.test_add_object(self.model.objects.count())
        response = self.client.get(self.url)
        self.assertEqual(len(response.data), 2)

    def test_delete_object(self):
        if self.__class__ is RestAPITestCase:
            return
        self.test_add_object()
        response = self.remove_last_object()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.model.objects.count(), 0)

    def test_update_object(self):
        if self.__class__ is RestAPITestCase:
            return
        self.test_add_object()
        obj = self.model.objects.last()
        response = self.client.put(self.url + str(obj.id), self.modified_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.modified_data)


class TwitchUserRestAPITest(RestAPITestCase):
    def setUp(self):
        self.model = TwitchUser
        self.serializer = TwitchUserSerializer
        self.view_list = TwitchUserList
        self.view_detail = TwitchUserDetail
        self.data = {
            'twid': 1728499,
            'name': 'raidrix',
        }
        self.modified_data = {
            'twid': 1728499,
            'name': 'no_raidrix'
        }
        self.url = '/twitchdata/twitch_user/'
        super().setUp()


class GameRestAPITest(RestAPITestCase):
    def setUp(self):
        self.model = Game
        self.serializer = GameSerializer
        self.view_list = GameList
        self.view_detail = GameDetail
        self.data = {
            'twid': 12345,
            'name': 'PUBG'
        }
        self.modified_data = {
            'twid': 12345,
            'name': 'no_PUBG'
        }
        self.url = '/twitchdata/game/'
        super().setUp()


class ChannelRestAPITest(RestAPITestCase):
    def setUp(self):
        self.model = Channel
        self.serializer = ChannelSerializer
        self.view_list = ChannelList
        self.view_detail = ChannelDetail
        self.data = {
            'twid': 12345,
        }
        self.modified_data = {
            'twid': 54321,
        }
        self.url = '/twitchdata/channel/'
        super().setUp()
