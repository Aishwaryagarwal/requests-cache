from os.path import isfile
from shutil import rmtree

from requests_cache.backends import FileDict
from tests.integration.test_backends import CACHE_NAME, BaseStorageTest


class TestFileDict(BaseStorageTest):
    storage_class = FileDict
    picklable = True

    @classmethod
    def teardown_class(cls):
        rmtree(CACHE_NAME, ignore_errors=True)

    def init_cache(self, index=0, **kwargs):
        cache = self.storage_class(f'{CACHE_NAME}_{index}', use_temp=True, **kwargs)
        cache.clear()
        return cache

    def test_paths(self):
        cache = self.storage_class(CACHE_NAME)
        for i in range(self.num_instances):
            cache[f'key_{i}'] = f'value_{i}'

        assert len(list(cache.paths())) == self.num_instances
        for path in cache.paths():
            assert isfile(path)
