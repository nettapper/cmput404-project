# MIT License

# Copyright (c) 2017 Conner Dunn, Tian Zhi Wang, Kyle Carlstrom, Xin Yi Wang, Josh Deng

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from server.quickstart.models import Post, Author
from rest_framework import status
from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from testutils import createAuthor, createAuthorFriend, getBasicAuthHeader

class PostTests(APITestCase):
    """ This is the home of all of our tests relating to the post url """

    AUTHOR_USER_NAME = 'aName'
    AUTHOR_USER_PASS = 'password127'
    AUTHOR_USER_MAIL = 'aName@example.com'

    NOT_ACTIVE_USER_NAME = 'notActiveName'
    NOT_ACTIVE_USER_MAIL = 'notActiveName@example.com'
    NOT_ACTIVE_USER_PASS = 'password127'

    URL = 'http://127.0.0.1:8000/'

    def setUp(self):
        """ Set up is run before each test """
        self.not_active_author = createAuthor(self.NOT_ACTIVE_USER_NAME, self.NOT_ACTIVE_USER_MAIL, self.NOT_ACTIVE_USER_PASS, isActive=False)
        self.author = createAuthor(self.AUTHOR_USER_NAME, self.AUTHOR_USER_MAIL, self.AUTHOR_USER_PASS)

    def test_posturl_get_unauth_401(self):
        """ GETing the public posts w/o any auth will result in a 401 """
        url = reverse("post")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_posturl_get_basic_auth(self):
        """ GETing while loggin w/ Basic Auth should return a 2XX """
        url = reverse("post")
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))

    def test_posturl_get_unactivated_401(self):
        """ GETing the public posts w/o being active will result in a 401 """
        url = reverse("post")
        basicAuth = getBasicAuthHeader(self.NOT_ACTIVE_USER_NAME, self.NOT_ACTIVE_USER_PASS)
        response = self.client.get(url, AUTH_TYPE="Basic", HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_posturl_get_as_author_2XX(self):
        """ GETing the public posts when logged in as an author will result in a 2XX and data """
        url = reverse("post")
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) >= 0)

    def test_posturl_post_bad_4XX(self):
        """ POST an empty post expecting a 4XX (is_client_error) """
        url = reverse("post")
        obj = {}
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.post(url, obj, format='json', HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_client_error(response.status_code))
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def post_a_post_obj(self, title, visibility):
        url = reverse("post")
        obj = {
            "title": title,
            "content": "this is a post dude",
            "description": "im not sure how to describe my post",
            "contentType": "text/markdown",
            "author": "",
            "comments": [],
            "visibility": visibility,
            "visibleTo": []
        }
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.post(url, obj, format='json', HTTP_AUTHORIZATION=basicAuth)
        return response

    def test_posturl_post_good_2XX(self):
        """ POST a good post expecting a 2XX (is_success) """
        response = self.post_a_post_obj("testing a good post", "PUBLIC")
        self.assertTrue(status.is_success(response.status_code))

    def test_posturl_delete_405(self):
        """ DELETE should throw a client error as it shouldn't be allowed to delete everyting """
        url = reverse("post")
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.delete(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_posturl_put_405(self):
        """ PUT should throw a client error as it doesn't make sense to put at this endpoint """
        url = reverse("post")
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.put(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_posturl_get_only_returns_public(self):
        """ GET should only return posts that are public according to spec """
        vis = ["PUBLIC", "PRIVATE", "FOAF", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("testing a %s post" % v, v)
        url = reverse("post")
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) == 1)  # only the PUBLIC post should be returned
