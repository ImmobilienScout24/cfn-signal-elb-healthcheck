from pybuilder.core import use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")
use_plugin("copy_resources")
use_plugin("python.pycharm")


name = "cfn-signal-elb-healthcheck"
default_task = ['clean', 'publish']
version = 0.1


@init
def set_properties(project):
    project.build_depends_on('mock')
    project.depends_on('docopt')
    project.depends_on('boto')

    project.set_property('copy_resources_target', '$dir_dist')
    project.get_property('copy_resources_glob').append('setup.cfg')

    project.set_property('verbose', True)


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os
    project.set_property('teamcity_output', True)
    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['clean', 'install_build_dependencies', 'publish']
    project.set_property('install_dependencies_index_url', os.environ.get('PYPIPROXY_URL'))
    project.set_property('install_dependencies_use_mirrors', False)
    project.rpm_release = os.environ.get('RPM_RELEASE', 0)
