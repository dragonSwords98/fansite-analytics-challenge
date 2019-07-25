# Feature 1 - Track most active hosts and display when requested
#
# Any instances of this class will continually log all hosts inputted
# and will provide the top ten when requested.
# Also, it may not be practical to track the hosts forever, so there's a clear host option here.
#
# Assumptions: All hosts are considered 'active' and remain 'active' indefinitely.
# In a practical application, hosts can become inactive, or banned, which may overwrite this.
#
class ActiveHostsTracker():

  constructor(self):
    self.activeHosts = {}
    self.resetCountTopTen()

  def recordLog(self, host):
    self.resetCountTopTen()
    self.activeHosts[host] = self.activeHosts.setdefault(host, 0) + 1

  def countTopTen(self):
    sortActiveHosts = sorted(activeHosts.items(), key=lambda h: h[1], reverse=True)
    self.topTen = sortActiveHosts[0:9]
    self.latestCountMade = True

  def getTopTen(self):
    if not self.latestCountMade:
      self.countTopTen()
    return self.topTen # [(host,frequency),(h, f), ...]

  def resetCountTopTen(self):
    self.latestCountMade = False
    self.topTen = []

  def resetTracker(self):
    self.resetCountTopTen()
    self.activeHosts = self.activeHosts.fromkeys(self.activeHosts, 0)

# endClass


# Feature 2 - Track the resources consuming the most bandwidth
#
# Any instances of this class will continually log all resources inputted
# and will provide the top ten when requested.
# Also, it may not be practical to track the resources forever, so there's a clear option here.
#
class BandwidthTracker():

  constructor(self):
    self.resourcesConsumed = {}
    self.resetCountTopTen()

  def recordLog(self, url, byteSize):
    self.resourcesConsumed[url] = self.resourcesConsumed.setdefault(url, 0) + byteSize
    
  def countTopTen(self):
    # this is currently ignoring the frequency and doing a total bytes count..
    sortResourcesByBandwidth = sorted(resourcesConsumed.items(), key=lambda r: r[1], reverse=True)
    self.topTen = sortResourcesByBandwidth[0:9]
    self.latestCountMade = True

  def getTopTen(self):
    if not self.latestCountMade:
      self.countTopTen()
    return self.topTen # [(url,bytes),(u, b), ...]

  def resetCountTopTen(self):
    self.latestCountMade = False
    self.topTen = []

  def resetTracker(self):
    self.resetCountTopTen()
    self.resourcesConsumed = self.resourcesConsumed.fromkeys(self.resourcesConsumed, 0)

# endClass


# Feature 3 - Track the high traffic periods
#
# Any instances of this class will continually log and will provide top ten when requested.
# Continuously moves a 'bubble' window along as logs proceed
# Also, it may not be practical to track the traffic forever, so there's a clear option here.
#
class HighTrafficPeriodTracker():

  constructor(self):
    self.sixtyMinuteWindow = deque()
    self.startTime = date.min
    self.resetTracker()

  def recordLog(self, timestamp):
    ts = datetime.strptime(timestamp, "[%d/%b/%Y:%H:%M:%S -0400]")
    sixtyMinuteWindow.append(ts)

    # determine if timestamp has exceeded 60 minute period, exclusive of endtime
    if (ts >= startTime + timedelta(hour=1)):
      self.countTopTen(self.frequency, startTime)

      self.resetPeriodWindow(ts)

    # count the frequency after assessing window
    self.frequency += 1

  def countTopTen(self, frequency, ts):
    self.topTen.append((ts.strftime("%d/%b/%Y:%H:%M:%S -0400"),frequency))
    sortHighestTrafficPeriods = sorted(self.topTen.items(), key=lambda r: r[1], reverse=True)
    self.topTen = sortHighestTrafficPeriods[0:9]

  def getTopTen(self):
    return self.topTen # [(url,bytes),(u, b), ...]

  def resetPeriodWindow(self, endTime):
    # determine new startTime, which must be the 60 minute period, inclusive of endTime
    
    self.startTime = endTime - timedelta(hour=1) + timedelta(seconds=1)

    while (self.sixtyMinuteWindow[0] < startTime):
      self.sixtyMinuteWindow.popleft()
      self.frequency -= 1
  
  def resetCountTopTen(self):
    self.topTen = []

  def resetTracker(self):
    self.resetCountTopTen()
    self.sixtyMinuteWindow.clear()
    self.frequency = 0

# endClass

# Feature 4 - Track blocked activity from failed login attempts
#
# Any instances of this class will continually log and will provide all blocked requests when requested.
# Also, it may not be practical to track the activity forever, so there's a clear option here.
# Stays in blocked mode after processing and can also begin in block mode if it is taking over this work
# from another process
#
class BlockedLoginsTracker():
  constructor(self, initBlockMode=False, unblockTime=date.min):
    self.resetBlockedLogs()
    self.blockMode = initBlockMode
    self.unblockTime = unblockTime
    self.consecutiveFails = []

  def recordLog(self, timestamp, request, replyCode, line):
    ts = datetime.strptime(timestamp, "[%d/%b/%Y:%H:%M:%S -0400]")

    if self.blockMode:
      if (ts < self.unblockTime):
        self.blockedLogs.append(line)
      else:
        self.resetBlockMode()
        self.__checkLog(ts, replyCode)
    else:
      self.__checkLog(ts, replyCode)

  def __checkLog(self, ts, request, replyCode, line):
    if (request == "POST /login HTTP/1.0" && re.match("^(4[0-9][0-9])$", replyCode)):
      if (ts < self.consecutiveFails[0]):
        if len(self.consecutiveFails) >= 2:
          self.__initiateBlockMode(ts + timedelta(seconds=19))
        else:
          self.consecutiveFails.append(ts)
      else:
        self.consecutiveFails = self.consecutiveFails[1:] + [ts]
        
    elif (request == "POST /login HTTP/1.0" && re.match("^(2[0-9][0-9])$", replyCode)):
      self.consecutiveFails = []

  def __initiateBlockMode(self, unblockTime):
    self.blockMode = True
    self.unblockTime = unblockTime

  def __resetBlockMode(self):
    self.blockMode = False
    self.unblockTime = date.min

  def resetBlockedLogs(self):
    self.blockedLogs = []
