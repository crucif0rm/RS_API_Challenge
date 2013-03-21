#!/usr/bin/env python
#
# This is to throttle API requests
import time


classs rate_throttle :
	def __init__ ( self, rate=2, period=1 ) :
		self.rate = rate
		self.period = period
		self.allowed = self.rate
		self.lastcheck=time.time()

	def check ( self ) :
		if self.rate < 0 :
			return True
		current = time.time()
		timepassed = current - self.lastcheck
		self.lastcheck = current
		self.allowed += timepassed * ( self.rate / self.period )
		if self.allowed > self.rate :
			self.allowed = self.rate
		if self.allowed < 1.0 :
			return False
		else :
			self.allowed -= 1.0
			return True
