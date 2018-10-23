import csv


def main():
    # print("Main")
    parse_data('test_data/test_data1.csv')


def parse_data(file):
    # print("reading")
    time_data = [];
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    time_data.append((float(row[0]), float(row[1])))
                except ValueError:
                    print("could not convert data to a float")
    except OSError:
        print("cannot open")
    else:
        print(time_data)
        return time_data


def calculate_values(data):
    print("Calculating")


if __name__ == "__main__":
    main()
