from __future__ import absolute_import, print_function, unicode_literals

import datetime
import subprocess

from distutils.core import Command
from setuptools.command.egg_info import egg_info


class assets(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            subprocess.check_call(['npm', 'run', 'build'])
        except (OSError, subprocess.CalledProcessError) as e:
            print('Error compiling assets: ' + str(e))
            raise SystemExit(1)


class egg_info_datetime(egg_info):

    def tags(self):
        version = ''
        if self.tag_build:
            version += self.tag_build
        if self.tag_svn_revision:
            rev = self.get_svn_revision()
            if rev:     # is 0 if it's not an svn working copy
                version += '-r%s' % rev
        if self.tag_date:
            now = datetime.datetime.now()
            version += now.strftime("-%Y%m%d%H%M")
        return version


def add_subcommand(command, extra_sub_commands):
    # Sadly, as commands are old-style classes, `type()` can not be used to
    # construct these.
    class CompileAnd(command):
        sub_commands = command.sub_commands + extra_sub_commands
    CompileAnd.__name__ = command.__name__
    return CompileAnd
