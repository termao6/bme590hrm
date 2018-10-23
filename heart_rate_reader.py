import csv


def main():
    # print("Main")
    data = parse_data('test_data/test_data1.csv')
    print(data)
    calculate_values(data)

def parse_data(file):
    # print("reading")
    time = [];
    time_data = [];
    run_avg = [];
    ctr = 0;
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    time.append(float(row[0]))
                    time_data.append(float(row[1]))
                    if ctr >= 4:
                        run_avg.append((time_data[ctr]
                                       + time_data[ctr-1] + time_data[ctr-2]
                                       + time_data[ctr-3] + time_data[ctr-4])/5)
                    ctr = ctr + 1
                except ValueError:
                    print("could not convert data to a float")
    except OSError:
        print("cannot open")
    else:
        # print((time, run_avg))
        return time, run_avg


def calculate_values(data):
    print("Calculating")
    vMax = max(data[1])
    print(vMax)


if __name__ == "__main__":
    main()
