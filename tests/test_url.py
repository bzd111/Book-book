import pytest

from config import ROOT_PATH
from utils import filter_url


@pytest.fixture
def remove_json():
    fpath = ROOT_PATH / 'url.json'
    if fpath.exists():
        fpath.unlink()


def test_filter_url_empty(remove_json):
    diff = filter_url('url.json', ['www.gogogozxc.xyz'])
    assert diff == ['www.gogogozxc.xyz']


def test_filter_url_exist():
    diff = filter_url('url.json', ['www.gogogozxc.xyz'])
    assert diff == []
