import logging
import os
from subprocess import PIPE, Popen


class TmuxSession(object):
    def __init__(self, name, cwd):
        self._name = name
        self._cwd = cwd

    @property
    def name(self):
        return self._name

    @property
    def cwd(self):
        return self._cwd

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        try:
            env = os.environ.copy()
            env.pop('TMUX', None)
            _check_popen('tmux', 'new-session', '-d', '-s', self.name, cwd=self.cwd, env=env)
        except Exception as _:
            self.stop()
            raise

    def stop(self):
        _check_popen('tmux', 'kill-session', '-t', self.name)

    def send_line(self, line):
        _check_popen('tmux', 'send-keys', 't', self.name, line, 'C-m')


def _check_popen(*args, **kwargs):
    _kwargs = {'args': list(args)}
    _kwargs.update(kwargs)
    _kwargs.update({'stdout': PIPE, 'stderr': PIPE})
    popen = Popen(**_kwargs)
    stdout, stderr = popen.communicate()
    if popen.returncode != 0:
        raise RuntimeError('Command failed. ' + _log_command(_kwargs, popen, stdout, stderr))
    else:
        logging.debug("Executed command: %s", ' '.join(_kwargs['args']))
    return stdout, stderr, popen


def _log_command(kwargs, popen, stdout, stderr):
    return "Command [{cmd}] returned {return_code}. Working directory '{cwd}'. " \
           "Stdout: '{stdout}'. Stderr: '{stderr}'.".format(cmd=' '.join(kwargs['args']), return_code=popen.returncode,
                                                            cwd=kwargs.get('cwd', os.getcwd()), stdout=stdout,
                                                            stderr=stderr)
