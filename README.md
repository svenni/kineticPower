# kineticPower

A simple tool I wrote a few years ago to take the `.fit` file created by my Garmin Edge 500 while riding on my Kurt Kinetic Road Machine trainer. It takes the speed values and calculates the watts based on the power curve of the trainer, it then adds those watts to a new fit file that I could then upload to something like Strava.

It uses a python module called [fit](https://pypi.org/project/fit/) which is not being maintained so this script only works on python2.7

## Usage

`python kineticPower.py in_file.fit [out_file.fit]`