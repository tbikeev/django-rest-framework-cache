from rest_framework import serializers

from .cache import cache
from .settings import api_settings
from .utils import get_cache_key


class CachedModelSerializer(serializers.ModelSerializer):
    _cache_timeout = api_settings.DEFAULT_CACHE_TIMEOUT

    def _get_cache_key(self, instance):
        request = self.context.get('request')
        protocol = request.scheme if request else 'http'
        return get_cache_key(instance, self.__class__, protocol)

    def to_representation(self, instance):
        """
        Checks if the representation of instance is cached and adds to cache
        if is not.
        """
        key = self._get_cache_key(instance)
        cached = cache.get(key)
        if cached:
            return cached

        result = super(CachedModelSerializer, self).to_representation(instance)
        cache.set(key, result, self._cache_timeout)
        return result
