# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2015
# Author: Cleber Rosa <cleber@redhat.com>


import abc


class Plugin(object):

    """
    Base for all plugins
    """


class CLI(Plugin):

    """
    Base plugin interface for adding options (non-commands) to the command line

    Plugins that want to add extra options to the core command line application
    or to sub commands should use the 'avocado.plugins.cli' namespace.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        super(CLI, self).__init__()

    @abc.abstractmethod
    def configure(self, parser):
        """
        Configures the command line parser with options specific to this plugin
        """

    @abc.abstractmethod
    def run(self, args):
        """
        Execute any action the plugin intends.

        Example of action may include activating a special features upon
        finding that the requested command line options were set by the user.

        Note: this plugin class is not intended for adding new commands, for
        that please use `CLICmd`.
        """


class CLICmd(Plugin):

    """
    Base plugin interface for adding new commands to the command line app

    Plugins that want to add extensions to the run command should use the
    'avocado.plugins.cli.cmd' namespace.
    """
    __metaclass__ = abc.ABCMeta
    name = None
    description = None

    def __init__(self):
        super(CLICmd, self).__init__()

    def configure(self, parser):
        """
        Lets the extension add command line options and do early configuration

        By default it will register its `name` as the command name and give
        its `description` as the help message.
        """
        help_msg = self.description
        if help_msg is None:
            help_msg = 'Runs the %s command' % self.name

        parser = parser.subcommands.add_parser(self.name,
                                               help=help_msg)
        return parser

    @abc.abstractmethod
    def run(self, args):
        """
        Entry point for actually running the command
        """
