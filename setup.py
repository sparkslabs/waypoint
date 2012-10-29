#!/usr/bin/python

from distutils.core import setup    
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if is_package( dir ):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages

packages = find_packages(".")
package_names = packages.keys()

setup(name = "waypoint",
      version = "0.1.0",
      description = "waypoint",
     
      author = "Michael Sparks",
      author_email = "michael.sparks@bbc.co.uk",
      url = "http://www.bbc.co.uk/rd/",
      license ="Apache Software License",
      packages = package_names,
      package_dir = packages,
      scripts = [
                  'scripts/waypointservice',
                  'scripts/waypoint_aggregate_analyser',
                  'scripts/waypoint_collator',
                  'scripts/waypoint_reader',
                  'scripts/waypointservice',
                  'scripts/waypoint.mkdirs',
                ],
      data_files=[
                   ('/etc/init',         ['etc/init/waypointservice.conf']),
                   ('/etc/waypointservice', ["etc/waypointservice/config.json"])
                 ],

      long_description = """
Package for Waypoint related code.
      """
      )
