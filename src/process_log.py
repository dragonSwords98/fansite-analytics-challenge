## FANSITE-ANALYTICS-CHALLENGE
## by: Bryan Ling

from collections import deque
from datetime import date, time, datetime, timedelta
from trackers import ActiveHostsTracker, BandwidthTracker, HighTrafficPeriodTracker, BlockedLoginsTracker


activeHostsTracker = new ActiveHostsTracker()
bandwidthTracker = new BandwidthTracker()
highTrafficPeriodTracker = new HighTrafficPeriodTracker()
blockedLoginsTracker = new BlockedLoginsTracker()

# Parse Log File
f = open("log.txt", "r")
line = file.readline();
while line != "":
  lineArray = line.split(" ")

  # data format, can turn into class
  host = lineArray[0]
  timestamp = lineArray[3]
  
  request = lineArray[4].split(" ")
  httpMethod = request[0]
  url = request[1]
  hostHeader = request[2]

  replyCode = lineArray[5]
  byteSize = lineArray[6]

  # Feature 1
  activeHostsTracker.recordLog(host)

  # Feature 2
  bandwidthTracker.recordLog(url, byteSize)

  # Feature 3
  highTrafficPeriodTracker.recordLog(timestamp)

  # Feature 4
  blockedLoginsTracker.recordLog(timestamp, request, replyCode, line)


# Extract Feature 1 to File
hostsFile = open("log_output/hosts.txt", "w")
topTenActiveHosts = activeHostsTracker.getTopTen()
for host in topTenActiveHosts:
  print >>hostsFile, ",".join(host)
hostsFile.close()

# Extract Feature 2 to File
resourcesFile = open("log_output/resources.txt", "w")
topTenResourcesConsumed = bandwidthTracker.getTopTen()
for resource in topTenResourcesConsumed:
  print >>resourcesFile, resouce[0]
resourcesFile.close()

# Extract Feature 3 to File
hoursFile = open("log_output/hours.txt", "w")
topTenTrafficPeriods = highTrafficPeriodTracker.getTopTen()
for period in topTenTrafficPeriods:
  print >>hoursFile, ",".join(period)
hoursFile.close()

# Extract Feature 4 to File
blockedFile = open("log_output/blocked.txt", "w")
blockedRequests = blockedLoginsTracker.getBlockedLogins()
for request in blockedRequests:
  print >>blockedFile, request
blockedFile.close()

