#!  usr/bin/env/python

import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt

################################################################################

TAU1 = 4.e-9                 # in nanoseconds
TAU2 = 15.e-9                # in nanoseconds
A = 10.                      # in ???
B = -10.                     # in ???
TEND = 200.e-9               # in nanoseconds
DELTAT = 40.e-9              # in nanoseconds
FS = 80.e6                   # in megahertz
ORDER = 4

################################################################################

def PMTpulse(t):
    return A*np.exp(-t/TAU1)+B*np.exp(-t/TAU2)

def f2(t2,deltaT,tStep):
    tmp = PMTpulse(t2)[int(np.ceil(deltaT/tStep)):]

    return np.append(np.zeros(int(np.ceil(deltaT/tStep))),tmp)

# find cutoff freq for bw filter to cause -10dB drop by fs/2
def cutoff(fs, order):
    return (0.5)**(10./(6*order))*fs/2
#    return .45*fs
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

################################################################################

t = np.linspace(0,TEND,(TEND*FS)+1) # 2 microsecond array in TSTEP ns steps
t2 = t - DELTAT
pulse1 = PMTpulse(t)
pulse2 = f2(t2,DELTAT,1./FS)
data = pulse1+pulse2
cutoff = cutoff(FS,ORDER)
b, a = butter_lowpass(cutoff, FS, ORDER)

y = butter_lowpass_filter(data, cutoff, FS, ORDER)

w, h = freqz(b, a, worN=8000)
plt.subplot(2, 1, 1)
plt.plot(0.5*FS*w/np.pi, np.abs(h), 'b')
plt.plot(cutoff, 0.5*np.sqrt(2), 'ko')
plt.axvline(cutoff, color='k')
plt.xlim(0, 0.5*FS)
plt.title("Lowpass Filter Frequency Response")
plt.xlabel('Frequency [Hz]')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(t, data, 'b-', label='signal')
plt.plot(t, y, 'g-', linewidth=2, label='filtered signal')
plt.xlabel('Time [sec]')
plt.grid()
plt.legend(loc = 4, framealpha=0.5)

plt.subplots_adjust(hspace=0.35)
plt.savefig('test.png')
