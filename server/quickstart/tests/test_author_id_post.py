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
from server.quickstart.models import Post, Author, FollowingRelationship
from rest_framework import status
from rest_framework.test import APITestCase
from requests.auth import HTTPBasicAuth
from testutils import createAuthor, createAuthorFriend, getBasicAuthHeader, createNode

class AuthorPostTest(APITestCase):
    """ This is the home of all of our tests relating to the author/:id/posts url """

    AUTHOR_USER_NAME = 'author'
    AUTHOR_USER_PASS = 'password127'
    AUTHOR_USER_MAIL = 'author@example.com'

    FRIEND_USER_NAME = 'friend'
    FRIEND_USER_PASS = 'password127'
    FRIEND_USER_MAIL = 'friend@example.com'

    FOAF_USER_NAME = 'foaf'
    FOAF_USER_PASS = 'password127'
    FOAF_USER_MAIL = 'foaf@example.com'

    STRANGER_USER_NAME = 'stranger'
    STRANGER_USER_PASS = 'password127'
    STRANGER_USER_MAIL = 'stranger@example.com'

    NOT_ACTIVE_USER_NAME = 'notative'
    NOT_ACTIVE_USER_PASS = 'password127'
    NOT_ACTIVE_USER_MAIL = 'notative@example.com'

    URL = 'http://127.0.0.1:8000/'

    NODE_USER_NAME = 'aNode'
    NODE_USER_MAIL = 'nodeuser@example.com'
    NODE_USER_PASS = 'password127'
    NODE_USER_URL = 'http://127.0.0.1:9999'  # just randomly choosing a port, no server actually running here

    def setUp(self):
        """ Set up is run before each test """
        self.not_active_author = createAuthor(self.NOT_ACTIVE_USER_NAME, self.NOT_ACTIVE_USER_MAIL, self.NOT_ACTIVE_USER_PASS, isActive=False)
        self.stranger_author = createAuthor(self.STRANGER_USER_NAME, self.STRANGER_USER_MAIL, self.STRANGER_USER_PASS)
        self.author = createAuthor(self.AUTHOR_USER_NAME, self.AUTHOR_USER_MAIL, self.AUTHOR_USER_PASS)
        self.friend_author = createAuthorFriend(self.FRIEND_USER_NAME, self.FRIEND_USER_MAIL, self.FRIEND_USER_PASS, self.author)
        self.foaf_author = createAuthorFriend(self.FOAF_USER_NAME, self.FOAF_USER_MAIL, self.FOAF_USER_PASS, self.friend_author)
        self.node_user = createNode(self.NODE_USER_NAME, self.NODE_USER_MAIL, self.NODE_USER_PASS, self.NODE_USER_URL)

    def test_authoridposturl_get_unauth_401(self):
        """ GETing the posts available to an author w/ my author id w/o any auth will result in a 401 """
        url = reverse("authorIdPosts", args=[self.author.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authoridposturl_get_unactivated_401(self):
        """ GETing the posts available to an an author w/ unactivated user w/o any auth will result in a 401 """
        url = reverse("authorIdPosts", args=[self.author.pk])
        basicAuth = getBasicAuthHeader(self.NOT_ACTIVE_USER_NAME, self.NOT_ACTIVE_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authoridposturl_get_basic_auth(self):
        """ GETing the posts by author while loggin w/ Basic Auth as author should return a 2XX """
        url = reverse("authorIdPosts", args=[self.author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))

    def test_authoridposturl_delete_405(self):
        """ DELETE should throw a client error as it shouldn't be allowed to delete everything for another author """
        url = reverse("authorIdPosts", args=[self.author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.delete(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authoridposturl_put_405(self):
        """ PUT should throw a client error as it doesn't make sense to put at this endpoint """
        url = reverse("authorIdPosts", args=[self.author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.put(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_authoridposturl_post_405(self):
        """ PUT should throw a client error as it doesn't make sense to put at this endpoint """
        url = reverse("authorIdPosts", args=[self.author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.post(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def post_a_post_obj(self, title, visibility, us, pw):
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
        basicAuth = getBasicAuthHeader(us, pw)
        response = self.client.post(url, obj, format='json', HTTP_AUTHORIZATION=basicAuth)
        return response

    def test_authoridposturl_get_your_posts(self):
        """ Should be able to get all my posts when accessing the url with my id """
        vis = ["PUBLIC", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("%s post" % v, v, self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        url = reverse("authorIdPosts", args=[self.author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) == 3)  # should get all posts made by me

    def test_authoridposturl_get_stranger_posts(self):
        """ GETing stranger posts by id should return the approprite number of posts """
        vis = ["PUBLIC", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("%s post" % v, v, self.STRANGER_USER_NAME, self.STRANGER_USER_PASS)
        url = reverse("authorIdPosts", args=[self.stranger_author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) == 2)  # should get PUBLIC and SERVERONLY

    def test_authoridposturl_get_friend_posts(self):
        """ GETing friend posts by id should return the approprite number of posts """
        vis = ["PUBLIC", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("%s post" % v, v, self.FRIEND_USER_NAME, self.FRIEND_USER_PASS)
        url = reverse("authorIdPosts", args=[self.friend_author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) == 3)  # should get PUBLIC, SERVERONLY, FRIENDS

    def test_authoridposturl_get_foaf_posts(self):
        """ GETing friend of a friend posts by id should return the approprite number of posts """
        vis = ["PUBLIC", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("%s post" % v, v, self.FOAF_USER_NAME, self.FOAF_USER_PASS)
        url = reverse("authorIdPosts", args=[self.foaf_author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) == 2)  # should get PUBLIC, SERVERONLY

    def test_authoridposturl_get_author_posts_format_is_paginated(self):
        """ The format : is paginated, if from a remote node (aka has a default count and page size) """
        vis = ["PUBLIC", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("%s post" % v, v, self.FOAF_USER_NAME, self.FOAF_USER_PASS)
        url = reverse("authorIdPosts", args=[self.foaf_author.pk])
        basicAuth = getBasicAuthHeader(self.NODE_USER_NAME, self.NODE_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(response.data["count"] > 0)  # the default count should always be > 0, if no prop KeyError
        self.assertTrue(response.data["size"] > 0)  # the default size should always be > 0, if no prop KeyError

    def test_authoridposturl_get_author_posts_format_posts(self):
        """ The format : posts should be returned as an array, and in this case with three posts """
        vis = ["PUBLIC", "FRIENDS", "SERVERONLY"]
        for v in vis:
            self.post_a_post_obj("%s post" % v, v, self.FOAF_USER_NAME, self.FOAF_USER_PASS)
        url = reverse("authorIdPosts", args=[self.foaf_author.pk])
        basicAuth = getBasicAuthHeader(self.AUTHOR_USER_NAME, self.AUTHOR_USER_PASS)
        response = self.client.get(url, HTTP_AUTHORIZATION=basicAuth)
        self.assertTrue(status.is_success(response.status_code))
        self.assertTrue(len(response.data) == 2)  # should get PUBLIC, SERVERONLY
