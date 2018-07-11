from __future__ import absolute_import, print_function, division


def get_package_data():
    return {_ASTROPY_PACKAGE_NAME_ + '.tests': ['coveragerc', 'data/*.reg', 'data/*/*.hdr']}  # noqa
