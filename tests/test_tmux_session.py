from os.path import join, exists
import pytest
import time

from termautomator.tmux_session import TmuxSession


def test_store_file(tmpdir):
    with TmuxSession(name='test_store_file', cwd=tmpdir) as tmux:
        tmux.send_line("echo 42 > foo")
        assert_file_appears(join(tmpdir, 'foo'))


@pytest.fixture(scope='session')
def tmpdir(tmpdir_factory):
    tmpdir = tmpdir_factory.mktemp('data')
    return tmpdir.strpath


def assert_file_appears(file_path, timeout_sec=1):
    end_time = time.time() + timeout_sec
    sleep_timeout = 0.01
    while True:
        if time.time() > end_time or exists(file_path):
            assert exists(file_path), "File '{}' should appear within {}s.".format(file_path, timeout_sec)
            break
        time.sleep(sleep_timeout)
        sleep_timeout *= 2
