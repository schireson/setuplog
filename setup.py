import sys

from setuptools import find_packages, setup

if sys.version_info[0] == 3:
    dev_reqs = 'deps/dev-requirements.txt'
else:
    dev_reqs = 'deps/dev-requirements-py2.txt'


def parse_requirements(filename):
    with open(filename) as f:
        lineiter = (line.strip() for line in f)
        return [
            line.replace(' \\', '').strip()
            for line in lineiter
            if (
                line and
                not line.startswith("#") and
                not line.startswith("-e") and
                not line.startswith("--")
            )
        ]


INSTALL_REQUIREMENTS = parse_requirements('deps/requirements.in')

SETUP_REQUIREMENTS = [
    'pytest-runner',
]

setup(
    name='schireson-logger',
    url='https://bitbucket.org/schireson/schireson-logger',
    author='Ashley Weaver',
    author_email='ashley@schireson.com',
    version='1.0.6',
    packages=find_packages(where='src', exclude=['tests']),
    package_dir={'': 'src'},
    include_package_data=True,
    python_requires=">2.6, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*, <4",
    install_requires=INSTALL_REQUIREMENTS,
    setup_requires=SETUP_REQUIREMENTS,
    test_suite='tests',
    zip_safe=False,
    extras_require={
        'develop': parse_requirements(dev_reqs),
    }
)
