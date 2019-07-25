# Notes

## Quick note on Interfaces & Abstraction
--------------------------------------
it is possible to abstract the tracker classes to one 'interface', but it would not add value to this challenge, so it was not done
to represent this understanding, class methods were named and coded similarly
each tracker is built so that they can stand alone from process_log.py
such that they can be set up to read from a continuous log stream

## Feat 1
------
list desc. order top 10 most active hosts/ip addr that have accessed the site

this is a straight up counting, track a hash table of all hosts/ip addresses that have accessed
assume there are no 'close matches' for hosts/ip address, it is strictly unique if the string for hostname/ip address is different

time complexity: O(n), n = log entries (aka. lines in file)
space complexity: O(n), n = 

we can do a defraud later
defraud simply by doing a 'warning', this host may be on the receiving end of a DoS


## Feat 2
------
Identify the top 10 resources on the site that consume the most bandwidth.
Bandwidth consumption can be extrapolated from bytes sent over the network and the frequency by which they were accessed.

this is a frequency * bytes sent, the key is the request string e.g. "GET /something.gif", as we're evaluated the expensive resource used



## Feat 3
------
List in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period.

this is a time logger in a sense. this one is tough, as its any 60-min window...
i believe the best you can do is continuously track the traffic, log the highest time you've seen, track top 10, and eliminate from the top 10 as it is exceeded

note: assignment assumes the timezone
could use microseconds for more accuracy


## Feat 4
------
Your final task is to detect patterns of three consecutive failed login attempts over 20 seconds in order to 
block all further attempts to reach the site from the same IP address for the next 5 minutes.
Each attempt that would have been blocked should be written to a log file named blocked.txt.

to make this feature more elegantly presented, the class instance of its tracker consumes each log regardless its request type and
keeps the blocked logs for extraction later via its class methods

### Note on an ignored case
-----------------------
in feature 4 is what if there's currently 2 failed attempts within the blocked time period, right at the end, then when it unblocks, we have another
failed attempt within those 20 seconds, do we block? right now, we just reset the count and record that as one failed attempt


## security measures
-----------------
masking sensitive information
detect DoS
detect fraud
detect robotic authentication attacks

how would you make this more secure? and prevent workarounds by time, ip, dos, etc.???
there's no direct way here to detect DDoS, however, based on the features provided here.
but there is a way to use our logs here to trigger blocking when the bandwidth has exceeded an upper bound limit
as well as detect potential malicious IPs 'teaming up' in a DDoS and proceed to block them all out

## testing
-------
did not approach this in a test-driven style, which I don't currently practice
however, if I were to write these tests up, it would be sensible to have
unit tests for each class, test each method for the good, bad, ugly, and edge cases
and complete them with process tests, where we provide valid and invalid log files of mixed sizes to test