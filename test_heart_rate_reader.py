import pytest
from heart_rate_reader import parse_data


# @pytest.mark.parametrize("test_file, expected", [
#     ('test_data/test_data1.csv', parsed_data1),
# ])


def test_parse_data():
    arr1 = parse_data('test_data/test_data1.csv')
    assert arr1[0][0] == .006
    assert arr1[1][0] == -.145


def test_wrong_file():
    with pytest.raises(IOError):
        parse_data('test_data/test_data.csv')


