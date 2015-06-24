#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import join
import urlparse
import urllib
import httplib
import logging

import authomatic
from authomatic.exceptions import FetchError


def custom_fetch(self, url, method='GET', params=None, headers=None, body='', max_redirects=5, content_parser=None):  # NOQA
    params = params or {}
    params.update(self.access_params)

    headers = headers or {}
    headers.update(self.access_headers)

    scheme, host, path, query, fragment = urlparse.urlsplit(url)
    query = urllib.urlencode(params)

    if method in ('POST', 'PUT', 'PATCH'):
        if not body:
            # Put querystring to body
            body = query
            query = None
            headers.update({'Content-Type': 'application/x-www-form-urlencoded'})

    request_path = urlparse.urlunsplit((None, None, path, query, None))

    self._log(logging.DEBUG, u' \u251C\u2500 host: {0}'.format(host))
    self._log(logging.DEBUG, u' \u251C\u2500 path: {0}'.format(request_path))
    self._log(logging.DEBUG, u' \u251C\u2500 method: {0}'.format(method))
    self._log(logging.DEBUG, u' \u251C\u2500 body: {0}'.format(body))
    self._log(logging.DEBUG, u' \u251C\u2500 params: {0}'.format(params))
    self._log(logging.DEBUG, u' \u2514\u2500 headers: {0}'.format(headers))

    # Connect
    proxy = os.environ.get('http_proxy', None)

    if proxy is None:
        if scheme.lower() == 'https':
            connection = httplib.HTTPSConnection(host)
        else:
            connection = httplib.HTTPConnection(host)
    else:
        proxy_scheme, proxy_host, proxy_path, _, _ = urlparse.urlsplit(proxy)
        proxy_host, proxy_port = proxy_host.split(':')

        self._log(logging.INFO, u'Using proxy on %s://%s:%s' % (proxy_scheme, proxy_host, proxy_port))

        if proxy_scheme.lower() == 'https':
            connection = httplib.HTTPSConnection(proxy_host, proxy_port)
        else:
            connection = httplib.HTTPConnection(proxy_host, proxy_port)

        request_path = "%s://%s" % (scheme, (join(host.rstrip('/'), request_path.lstrip('/'))))

    try:
        connection.request(method, request_path, body, headers)
    except Exception as e:
        raise FetchError(
            'Could not connect!',
            original_message=e.message,
            url=request_path
        )

    response = connection.getresponse()
    location = response.getheader('Location')

    if response.status in (300, 301, 302, 303, 307) and location:
        if location == url:
            raise FetchError(
                'Url redirects to itself!',
                url=location,
                status=response.status
            )

        elif max_redirects > 0:
            remaining_redirects = max_redirects - 1

            self._log(logging.DEBUG, 'Redirecting to {0}'.format(url))
            self._log(logging.DEBUG, 'Remaining redirects: {0}'.format(remaining_redirects))

            # Call this method again.
            response = self._fetch(
                url=location,
                params=params,
                method=method,
                headers=headers,
                max_redirects=remaining_redirects
            )

        else:
            raise FetchError(
                'Max redirects reached!',
                url=location,
                status=response.status
            )
    else:
        self._log(logging.DEBUG, u'Got response:')
        self._log(logging.DEBUG, u' \u251C\u2500 url: {0}'.format(url))
        self._log(logging.DEBUG, u' \u251C\u2500 status: {0}'.format(response.status))
        self._log(logging.DEBUG, u' \u2514\u2500 headers: {0}'.format(response.getheaders()))

    return authomatic.core.Response(response, content_parser)
