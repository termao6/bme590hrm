import csv
import json


def main():
    for data_file_num in range(1, 33):
        print(data_file_num)
        file_path = 'test_data/test_data' + str(data_file_num) + '.csv'
        save_path = 'results/test_data' + str(data_file_num) + '.json'
        data = parse_data(file_path)
        (metrics, message) = calculate_values(data[0], data[1])
        save_json(metrics, save_path)


def parse_data(file):
    """
    Parses data from file and gives cleaned (noise reduced)
    version of times, voltages

    Parameters:
        :param file: (string) path to csv file to be parsed

    Returns:
        :return: avg_times [float]: list of running avg times
            corresponding with voltages
        :return: avg_voltage [float]: list of running avg voltages
            corresponding w/ times
        :return: all_times [float]: list of all times in csv file
        :return: all_voltages [float]: list of all voltages in csv file
    """
    # print("reading")
    time = []
    time_data = []
    times_avg = []
    run_avg = []
    ctr = 0
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    time.append(float(row[0]))
                except ValueError:
                    print("could not convert time to a float")
                    time.append(time[ctr-1])
                try:
                    time_data.append(float(row[1]))
                except ValueError:
                    print("could not convert time to a float")
                    time_data.append(time_data[ctr-1])
                if ctr >= 4:
                    times_avg.append(time[ctr-2])
                    run_avg.append((time_data[ctr] +
                                   time_data[ctr-1] + time_data[ctr-2] +
                                   time_data[ctr-3] + time_data[ctr-4])/5)
                ctr = ctr + 1
            # fill in unaveraged values of times_avg to get all times
            times_avg.insert(0, time[1])
            times_avg.insert(0, time[0])
            times_avg.insert(len(times_avg), time[len(time)-2])
            times_avg.insert(len(times_avg), time[len(time)-1])
            # fill in unaveraged values of time_data to get all voltages
            run_avg.insert(0, time_data[1])
            run_avg.insert(0, time_data[0])
            run_avg.insert(len(run_avg), time_data[len(time_data)-2])
            run_avg.insert(len(run_avg), time_data[len(time_data)-1])
    except IOError as e:
        print(e)
        raise
    else:
        # print((time, run_avg))
        return times_avg, run_avg, time, time_data


def calculate_values(times, values):
    """
    Calculates metrics:
        mean_hr_bpm, voltage_extremes (max, min), duration of data,
        num_beats, beats [times]
    :param times: [float] array of times corresponding with voltage values
    :param values: [float] array of voltage values corresponding with times
    :return: metrics dictionary, message (stating if metrics are weird)
    """
    peak_times = find_peaks(times, values)
    metrics = {
        "mean_hr_bpm": round(len(peak_times)/max(times)*60),
        "voltage_extremes": (round(max(values), 3), round(min(values), 3)),
        "duration": max(times),
        "num_beats": len(peak_times),
        "beats": peak_times
    }

    message = ""
    if metrics.get("mean_hr_bpm") > 160 or metrics.get("mean_hr_bpm") < 40:
        message = "Heart rate out of normal range - recheck data"
    print(metrics)
    return metrics, message


def find_peaks(times, values):
    """"
    Simple Peak Detection - finds the local max of series of consecutive
    values above a certain threshold, calculated relative to the global max
    Helper method to calculate_values

    Parameters:
        :param times: [float] list of times corresponding with values
        :param values: [float] list of voltage values corresponding with times

    Returns:
        :return: peak_times [float] list of times corresponding to local maxima
            (voltage peaks)
    """
    local_subset = 500
    peak_thresh = max(values[0:local_subset]) - \
                (max(values[0:local_subset]) - min(values[0:local_subset]))*.5
    peak_times = []
    peak_vals = []
    depolar = False
    for i in range(2, len(values)):
        if i % local_subset == 0 and i+local_subset < len(values):
            peak_thresh = max(values[i:i+local_subset]) - \
                          (max(values[i:i+local_subset]) -
                           min(values[i:i+local_subset]))*.5
        if values[i] > peak_thresh:
            if (values[i-1] > values[i]) and \
                    values[i-1] > values[i-2] and not depolar:
                peak_times.append(times[i-1])
                peak_vals.append(values[i-1])
                depolar = True
        else:
            depolar = False

    # print(peak_times)
    # print(peak_vals)
    return peak_times


def save_json(data, save_path):
    with open(save_path, 'w') as fp:
        json.dump(data, fp)


if __name__ == "__main__":
    main()
