# bme590hrm

## Standard Features
* Sphinx documentation: https://termao6.github.io/bme590hrm/
* Unit tests
* PEP-8 styling
* Exception handling for invalid files and empty number values in csv

## Extra Features
* checks if heart rate data is out of normal range (hr > 100 or < 60) - sends message saying to the data is not normal
* handles empty number fields in csv by duplicating previous values so that the voltage values approximately correspond with time values
* reduces noise by having a running average filter
* set up Travis CI

## Notes
* User is responsible for having csv files of correct format: two columns of (time, voltage)
  * The program will run so long as the csv contains at least two columns of data
  * Calculate_values will return a message saying that the data is not normal, however
* Peak detection does not work correctly on all test cases, especially ones of irregular heart beats
* Metrics for all test data are stored in the /results folder
