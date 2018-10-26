import pytest
import os
from heart_rate_reader import parse_data
from heart_rate_reader import find_peaks
from heart_rate_reader import calculate_values
from heart_rate_reader import save_json

# @pytest.mark.parametrize("test_file, expected", [
#     ('test_data/test_data1.csv', parsed_data1),
# ])


def test_parse_data():
    arr1 = parse_data('test_data/test_data1.csv')
    assert arr1[0][0] == .000
    assert arr1[1][0] == -.145


def test_wrong_file():
    with pytest.raises(IOError):
        parse_data('test_data/test_data.csv')


def test_find_peaks():
    arr1 = parse_data('test_data/test_data1.csv')
    peak_times = find_peaks(arr1[0], arr1[1])
    assert peak_times[0] == .214
    assert peak_times[len(peak_times)-1] == 27.772


def test_calculate_values():
    arr1 = parse_data('test_data/test_data1.csv')
    (metrics, message) = calculate_values(arr1[0], arr1[1])
    assert metrics.get("mean_hr_bpm") == 76
    assert metrics.get("voltage_extremes")[0] == .95
    assert metrics.get("duration") == 27.775
    assert metrics.get("num_beats") == 35
    assert message == ""


def test_calculate_random_values():
    (metrics, message) = calculate_values(
        [0, 1, 2, 3, 4, 5, 6],
        [0, 0, 0, 0, 0, 0, 0])
    assert message != ""


def test_save_json():
    data_file_num = 1
    file_path = 'test_data/test_data' + str(data_file_num) + '.csv'
    save_path = 'results/test_data' + str(data_file_num) + '.json'
    data = parse_data(file_path)
    (metrics, message) = calculate_values(data[0], data[1])
    save_json(metrics, save_path)
    assert os.path.exists('results/test_data1.json')
