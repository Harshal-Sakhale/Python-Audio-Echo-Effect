import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import wave

# 8-bit mono wave file as input

#execfile('/home/root2/.pythonrc') # Tab completion in interactive mode

# Closes the window right after plt.show()
# unless '>python -i' is used to run this file
#matplotlib.interactive(True) 



filename=sys.argv[1];
w=wave.open(filename,'rb');
ofile=open(filename.replace('wav','raw'), 'wb');


NS=w.getnframes()
FS=w.getframerate()
SW=w.getsampwidth()
NC=w.getnchannels()


wo=wave.open(filename.replace('.wav','_ed.wav'), 'wb');

wo.setsampwidth(SW) # Asssume 1 8-bit mono
wo.setnframes(NS)
wo.setnchannels(NC) # Asssume 1 8-bit mono
wo.setframerate(FS)


Y=[]
# wavread
for i in range(NS):
	Y.append(ord(w.readframes(1))) # assuming 8-bit mono (single channel)
	
print("Ysize = %d" % (len(Y)))
print("NS=%d FS=%d SW=%d" % (NS,FS,SW))
#exit(0)




#FS=11025

# Number of samples
#NS=FS*5 # 5 second duration of audio file

A=np.logspace(1,0,FS)/10

plt.plot(A)

plt.figure()

xn=np.linspace(1,FS,FS,dtype=int)

xr=round(FS/3)

B=np.float64(xn % xr == 0  )
plt.plot(B)
plt.figure()

C=A*B
plt.plot(C)


buff=np.zeros((FS),dtype=int) # One second buffer

print("buff shape=", buff.shape)
print("C shape=", C.shape)
print(Y[0])
print(C*Y[0])
#exit(0)

Y2=[]
for i in range(NS):
	buff = buff + (C*Y[i])


	if buff[0] > 255 :
		Y2.append(255)
	else:
		Y2.append(buff[0])
	
	ofile.write(np.uint8(Y2[i]))

	buff=np.append(buff[1:],0) # Shift buffer forward, append 0


wo.writeframes(np.uint8(Y2))

plt.show()




# END
ofile.close()
w.close()
wo.close()
