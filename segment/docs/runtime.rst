Runtimes
========

City Peaks
----------

Africa bounding box: Longitude -20, 55. Latitude -40, 40.
That's 75 * 80 = 6000 long-lat units. Using `/usr/bin/time` to do
timing, we find, for the given long-lat, these times and these numbers
of city peaks found.

 * longitude 0-2, latitude 30-32, 4: 10s, found 6
 * longitude 0-4, latitude 30-32, 8: 26s, found 10
 * longitude 0-2, latitude 28-32, 8: 19s, found 14
 * longitude 0-4, latitude 28-32, 16: 54s, found 23
 * longitude -4-4, latitude 28-32, 32: 62s, found 33
 * longitude -4-4, latitude 26-34, 64: 128s, found 69

So let's say it's 2s per long-lat unit. 6000s is 2 hours.
