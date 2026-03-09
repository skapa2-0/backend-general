import time
import logging

import jwt
import requests
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.models import Organisation, UserProfile

logger = logging.getLogger(__name__)

_jwks_cache = {
    'keys': None,
    'fetched_at': 0,
}
JWKS_CACHE_TTL = 3600


def _get_jwks():
    now = time.time()
    if _jwks_cache['keys'] and (now - _jwks_cache['fetched_at']) < JWKS_CACHE_TTL:
        return _jwks_cache['keys']

    try:
        response = requests.get(settings.CLERK_JWKS_URL, timeout=10)
        response.raise_for_status()
        jwks = response.json()
        _jwks_cache['keys'] = jwks.get('keys', [])
        _jwks_cache['fetched_at'] = now
        return _jwks_cache['keys']
    except requests.RequestException as exc:
        logger.error('Failed to fetch JWKS: %s', exc)
        if _jwks_cache['keys']:
            return _jwks_cache['keys']
        raise AuthenticationFailed('Unable to fetch authentication keys.') from exc


def _get_signing_key(token):
    keys = _get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.DecodeError as exc:
        raise AuthenticationFailed('Invalid token header.') from exc

    kid = unverified_header.get('kid')
    for key_data in keys:
        if key_data.get('kid') == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key_data)

    # Key not found – force refresh once
    _jwks_cache['fetched_at'] = 0
    keys = _get_jwks()
    for key_data in keys:
        if key_data.get('kid') == kid:
            return jwt.algorithms.RSAAlgorithm.from_jwk(key_data)

    raise AuthenticationFailed('Signing key not found.')


class ClerkJWTAuthentication(BaseAuthentication):
    """Validate Clerk-issued JWTs via JWKS and return the corresponding UserProfile."""

    keyword = 'Bearer'

    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header.startswith(f'{self.keyword} '):
            return None

        token = auth_header[len(self.keyword) + 1:]
        if not token:
            return None

        public_key = _get_signing_key(token)

        try:
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                issuer=settings.CLERK_ISSUER,
                options={
                    'verify_exp': True,
                    'verify_iss': True,
                    'verify_aud': False,
                },
            )
        except jwt.ExpiredSignatureError as exc:
            raise AuthenticationFailed('Token has expired.') from exc
        except jwt.InvalidIssuerError as exc:
            raise AuthenticationFailed('Invalid token issuer.') from exc
        except jwt.InvalidTokenError as exc:
            raise AuthenticationFailed('Invalid token.') from exc

        user_profile = self._get_or_create_user(payload)
        return (user_profile, payload)

    @staticmethod
    def _get_or_create_user(payload):
        clerk_user_id = payload.get('sub')
        if not clerk_user_id:
            raise AuthenticationFailed('Token missing subject claim.')

        email = payload.get('email', '')
        name_parts = [
            payload.get('first_name', ''),
            payload.get('last_name', ''),
        ]
        name = ' '.join(p for p in name_parts if p).strip()
        org_id = payload.get('org_id')

        organisation = None
        if org_id:
            organisation, _ = Organisation.objects.get_or_create(
                clerk_org_id=org_id,
                defaults={
                    'name': payload.get('org_name', org_id),
                    'slug': payload.get('org_slug', org_id),
                },
            )

        user_profile, created = UserProfile.objects.get_or_create(
            clerk_user_id=clerk_user_id,
            defaults={
                'email': email,
                'name': name,
                'organisation': organisation,
                'role': payload.get('org_role', UserProfile.Role.MEMBER),
            },
        )

        if not created:
            changed = False
            if email and user_profile.email != email:
                user_profile.email = email
                changed = True
            if name and user_profile.name != name:
                user_profile.name = name
                changed = True
            if organisation and user_profile.organisation_id != organisation.id:
                user_profile.organisation = organisation
                changed = True
            if changed:
                user_profile.save()

        return user_profile
