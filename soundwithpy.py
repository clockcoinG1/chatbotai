import sounddevice as sd
 sd.default.device = 'Built-in Output'
 sd.default.samplerate = 48000
 sd.default.channels = 2
print(sd.query_devices()) #default device ID = 2
 sd.rec(int(10*sd.default.samplerate)) #240,000 points (10 sec recording)
 sd.wait() #wait until done
 recording myrecording = sd.rec(int(10*sd.default.samplerate), dtype='float64', blocking=True)
 #blocking = True makes this wait until finished to return
 myrecording = 'null' #reset variable so that next round doesnt get overridden raise Exception('There should be an error here.')
  import numpy as np #handy math lib