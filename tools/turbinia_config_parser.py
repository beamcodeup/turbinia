# -*- coding: utf-8 -*-
# # Copyright 2016 Google Inc.
# #
# # Licensed under the Apache License, Version 2.0 (the "License");
# # you may not use this file except in compliance with the License.
# # You may obtain a copy of the License at
# #
# #      http://www.apache.org/licenses/LICENSE-2.0
# #
# # Unless required by applicable law or agreed to in writing, software
# # distributed under the License is distributed on an "AS IS" BASIS,
# # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# # See the License for the specific language governing permissions and
# # limitations under the License.


"""Turbinia Config Parser."""

from __future__ import unicode_literals
import imp
import itertools
import os
import sys

# This Turbinia config parser can be invoked by any scripts to get the config.
# Note that this will not look for config files anywhere, except for
# /etc/turbinia. If there's a need to run Turbinia based on the config file in
# a homedir, you will need to run manually Turbinia.

# Look for config files with these names
CONFIGFILES = ['turbinia.conf', 'turbinia_config.py']
CONFIGPATH = ['/etc/turbinia']


def main():
  if len(sys.argv) < 2:
    print '%s <key name>' % sys.argv[0]
    sys.exit(1)
  key = sys.argv[1]
  if key:
    config_file = None
    for dirname, filename in itertools.product(CONFIGPATH, CONFIGFILES):
      if os.path.exists(os.path.join(dirname, filename)):
        config_file = os.path.join(dirname, filename)
        break
    if config_file is None:
      sys.exit(2)
    config = imp.load_source('config', config_file)
    import config  # pylint: disable=g-import-not-at-top
    try:
      print getattr(config, key.upper())
    except AttributeError:
      print 'Key not found: %s' % key
      sys.exit(3)


if __name__ == '__main__':
  main()
