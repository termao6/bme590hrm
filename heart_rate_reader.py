import csv


def main():
    # print("Main")
    data = parse_data('test_data/test_data1.csv')
    # print(data)
    calculate_values(data[0], data[1], data[2], data[3])


def parse_data(file):
    """
    Parses data from file and gives cleaned (noise reduced) version of times, voltages

    Parameters:
        file (string): path to csv file to be parsed

    Returns:
        avg_times [float]: list of running avg times corresponding with voltages
        avg_voltage [float]: list of running avg voltages corresponding w/ times
        all_times [float]: list of all times in csv file
        all_voltages [float]: list of all voltages in csv file
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
                    time_data.append(float(row[1]))
                    if ctr >= 4:
                        times_avg.append(time[ctr-2])
                        run_avg.append((time_data[ctr] +
                                       time_data[ctr-1] + time_data[ctr-2] +
                                       time_data[ctr-3] + time_data[ctr-4])/5)
                    ctr = ctr + 1
                except ValueError:
                    print("could not convert data to a float")
    except IOError as e:
        print(e)
    else:
        # print((time, run_avg))
        return times_avg, run_avg, time, time_data


def calculate_values(times, values, times_all, values_all):
    print("Calculating")
    (peak_times, peak_values) = find_peaks(times, values)

    metrics = {
        "mean_hr_bpm": round(len(peak_times)/max(times_all)*60),
        "voltage_extremes": (round(max(values),3), round(min(values),3)),
        "duration": max(times_all),
        "num_beats": len(peak_times),
        "beats": peak_times
    }

    print(metrics)


def find_peaks(times, values):
    vMax = max(values)
    thresh = vMax - abs(vMax - min(values))*.25
    print(vMax)
    print(thresh)
    peak_times = []
    peak_vals = []
    calc_peak_times = []
    calc_peak_vals = []
    for i in range (1, len(values)):
        if values[i] > thresh:
            calc_peak_vals.append(values[i])
            calc_peak_times.append(times[i])
        elif (values[i-1] > thresh) and (values[i] <= thresh):
            # just after peak
            ind = calc_peak_vals.index(max(calc_peak_vals))
            peak_times.append(round(calc_peak_times[ind], 3))
            peak_vals.append(round(calc_peak_vals[ind], 3))
            # reset lists to empty
            calc_peak_times = []
            calc_peak_vals = []

    print(peak_times, peak_vals)
    return peak_times, peak_vals


if __name__ == "__main__":
    main()
