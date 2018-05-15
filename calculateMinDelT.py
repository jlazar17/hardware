#!  usr/bin/env/python

import numpy as np
import scipy.signal as sig

################################################################################

TAU1 = 4                 # in nanoseconds
TAU2 = 15                # in nanoseconds
A = 10                   # in ???
B = -10                  # in ???
TSTEP = 0.1              # in nanoseconds
TEND = 2000              # in nanoseconds
SAMPLERATE = 1e-3/DELTAT # in megahertz

################################################################################

def PMTpulse(t):
    return A*np.exp(t/tau1)+B*np.exp(t/tau2)

def f2(f1,deltaT,tStep):
    tmp = np.append(np.zeros(deltaT/tStep),f1)
    return tmp[:len(f1)]


################################################################################

t = np.linspace(0,TEND,(TEND/TSTEP)+1) # 2 microsecond array in TSTEP ns steps
pulse1 = PMTpulse(t)
pulse2 = f2(pulse1,DELTAT,TSTEP)
signal = pulse1+pulse2

a,b = sig.butter
