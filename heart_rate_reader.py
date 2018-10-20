import csv


def main():
    print("Main")
    read_file('test_data/test_data1.csv')


def read_file(file):
    print("reading")
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
    print(time_data)


if __name__ == "__main__":
    main()
