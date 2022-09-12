import pytest
from utilities.inputcontrol import is_positive_integer


@pytest.mark.parametrize("value, expected_value", [(5, True), ('10', True), (-2, False), ('3.4', False)])
def test_is_positive_integer(value, expected_value):
    assert is_positive_integer(value) == expected_value
