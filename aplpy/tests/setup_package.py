def get_package_data():
    return {
        _ASTROPY_PACKAGE_NAME_ + '.tests': ['coveragerc', 'data/*/*.hdr', 'baseline_images/*.png']}
