from django.core.cache import cache, caches
from django.core.cache.backends.dummy import DummyCache

from .settings import api_settings
from .exceptions import ImproperlyConfigured
from .utils import is_test_environment

def init_dummy_cache():
    return DummyCache(host='localhost', params={})


try:
    cache_backend = api_settings.DEFAULT_CACHE_BACKEND
    if cache_backend != "default":
        cache = caches[cache_backend]
    if is_test_environment:
        cache = init_dummy_cache()
except KeyError:
    raise ImproperlyConfigured("'{}' is a invalid CACHE_BACKEND".format(
        api_settings.DEFAUL_CACHE_BACKEND))
