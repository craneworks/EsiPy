# -*- encoding: utf-8 -*-
# pylint: skip-file
from __future__ import absolute_import

import datetime
import httmock


def make_expire_time_str():
    """ Generate a date string for the Expires header
    RFC 7231 format (always GMT datetime)
    """
    date = datetime.datetime.utcnow()
    date += datetime.timedelta(days=1)
    return date.strftime('%a, %d %b %Y %H:%M:%S GMT')


def make_expired_time_str():
    """ Generate an expired date string for the Expires header
    RFC 7231 format (always GMT datetime).
    """
    date = datetime.datetime.utcnow()
    date -= datetime.timedelta(days=1)
    return date.strftime('%a, %d %b %Y %H:%M:%S GMT')


@httmock.urlmatch(
    scheme="https",
    netloc=r"login\.eveonline\.com$",
    path=r"^/oauth/token$"
)
def oauth_token(url, request):
    """ Mock endpoint to get token (auth / refresh) """
    if 'fail_test' in request.body:
        return httmock.response(
            status_code=400,
            content={'message': 'Failed successfuly'}
        )

    if 'no_refresh' in request.body:
        return httmock.response(
            status_code=200,
            content={
                'access_token': 'access_token',
                'expires_in': 1200,
            }
        )

    return httmock.response(
        status_code=200,
        content={
            'access_token': 'access_token',
            'expires_in': 1200,
            'refresh_token': 'refresh_token'
        }
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/verify/$"
)
def oauth_verify(url, request):
    return httmock.response(
        status_code=200,
        content={
            'CharacterID': 123456789,
            'CharacterName': 'EsiPy Tester',
            'CharacterOwnerHash': 'YetAnotherHash'
        }
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/verify/$"
)
def oauth_verify_fail(url, request):
    return httmock.response(
        status_code=400,
        content={'message': 'Failed successfuly'}
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/incursions/$"
)
def public_incursion(url, request):
    """ Mock endpoint for incursion.
    Public endpoint
    """
    return httmock.response(
        headers={'Expires': make_expire_time_str()},
        status_code=200,
        content=[
            {
                "type": "Incursion",
                "state": "mobilizing",
                "staging_solar_system_id": 30003893,
                "constellation_id": 20000568,
                "infested_solar_systems": [
                    30003888,
                ],
                "has_boss": True,
                "faction_id": 500019,
                "influence": 1
            }
        ]
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/incursions/$"
)
def public_incursion_no_expires(url, request):
    """ Mock endpoint for incursion.
    Public endpoint without cache
    """
    return httmock.response(
        status_code=200,
        content=[
            {
                "type": "Incursion",
                "state": "mobilizing",
                "staging_solar_system_id": 30003893,
                "constellation_id": 20000568,
                "infested_solar_systems": [
                    30003888,
                ],
                "has_boss": True,
                "faction_id": 500019,
                "influence": 1
            }
        ]
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/incursions/$"
)
def public_incursion_no_expires_second(url, request):
    """ Mock endpoint for incursion.
    Public endpoint without cache
    """
    return httmock.response(
        status_code=200,
        content=[
            {
                "type": "Incursion",
                "state": "established",
                "staging_solar_system_id": 30003893,
                "constellation_id": 20000568,
                "infested_solar_systems": [
                    30003888,
                ],
                "has_boss": True,
                "faction_id": 500019,
                "influence": 1
            }
        ]
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/characters/(\d+)/location/$"
)
def auth_character_location(url, request):
    """ Mock endpoint for character location.
    Authed endpoint that check for auth
    """
    return httmock.response(
        headers={'Expires': make_expire_time_str()},
        status_code=200,
        content={
            "station_id": 60004756,
            "solar_system_id": 30002543
        }
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/incursions/$"
)
def public_incursion_warning(url, request):
    """ Mock endpoint for incursion.
    Public endpoint without cache
    """
    return httmock.response(
        status_code=200,
        headers={"Warning": "199 - This endpoint has been updated."},
        content=[
            {
                "type": "Incursion",
                "state": "established",
                "staging_solar_system_id": 30003893,
                "constellation_id": 20000568,
                "infested_solar_systems": [
                    30003888,
                ],
                "has_boss": True,
                "faction_id": 500019,
                "influence": 1
            }
        ]
    )


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/incursions/$"
)
def public_incursion_server_error(url, request):
    """ Mock endpoint for incursion.
    Public endpoint without cache
    """
    public_incursion_server_error.count += 1
    return httmock.response(
        status_code=500,
        content={
            "error": "broke",
            "count": public_incursion_server_error.count
        }
    )


public_incursion_server_error.count = 0


@httmock.urlmatch(
    scheme="https",
    netloc=r"esi\.evetech\.net$",
    path=r"^/latest/incursions/$"
)
def public_incursion_expired(url, request):
    """ Mock endpoint for incursion.
    Public endpoint returning Expires value in the past
    """
    return httmock.response(
        headers={'Expires': make_expired_time_str()},
        status_code=200,
        content=[
            {
                "type": "Incursion",
                "state": "mobilizing",
                "staging_solar_system_id": 30003893,
                "constellation_id": 20000568,
                "infested_solar_systems": [
                    30003888,
                ],
                "has_boss": True,
                "faction_id": 500019,
                "influence": 1
            }
        ]
    )


_all_auth_mock_ = [
    oauth_token,
    oauth_verify,
    auth_character_location,
]
