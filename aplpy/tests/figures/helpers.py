# Licensed under a 3-clause BSD style license - see LICENSE.rst

from functools import wraps

import pytest

__all__ = ['figure_test']


def figure_test(*args, **kwargs):
    """
    A decorator that defines a figure test.
    """

    tolerance = kwargs.pop("tolerance", 0)
    style = kwargs.pop("style", {})
    savefig_kwargs = kwargs.pop("savefig_kwargs", {'adjust_bbox': False})
    savefig_kwargs["metadata"] = {"Software": None}

    def decorator(test_function):
        @pytest.mark.remote_data
        @pytest.mark.mpl_image_compare(
            tolerance=tolerance, style=style, savefig_kwargs=savefig_kwargs, **kwargs
        )
        @wraps(test_function)
        def test_wrapper(*args, **kwargs):
            return test_function(*args, **kwargs)

        return test_wrapper

    # If the decorator was used without any arguments, the only positional
    # argument will be the test to decorate so we do the following:
    if len(args) == 1:
        return decorator(*args)

    return decorator
