# Laus deo
# fix LTSpice data
# LTSpice is a free opensource tool for simulating digital and analog circuit.
# The point is after save the result of simulation, the software automatically choose the sampleling frequency and it's not a constant.
# During my search it's an unsolved problem and I tried to fix it. 
# CAUTION: it's work for only 1 input and 1 output signals, but it's open source and you (as a developer) can modify it as you need. 
# Developer: P.Zahedi
# E-mail: p.zahedi@live.com

import numpy as np


# class FixLTSpiceData:

    # change inter polate between points and fix the sampeling steps
    # Liniear interpolation is used to interpolate between two points 
def interpolator(y2,t2,y1,t1):
    m=(y2-y1)/(t2-t1)
    T_new=np.linspace(t1,t2,num=t2-t1,endpoint=True)
    Y_new = m*(T_new - t1) +y1
    return Y_new

# Dwonsample data space into a smaller space. for ML tools, typically length of output signal is 300-500 points
def downsampler(FixedVector,length):
    Y=[0]*length # create a large vector to downsample the original space
    m=int(len(FixedVector)/length) 
    for i in range(length):
        Y[i]=FixedVector[i*m]

    return Y

def fixLTSpiceData(FileAddress,FinalLength):
    
    Time=[0]
    Data=[0]
    Target=[0]
    Time_new=[]
    Data_new=[]
    Target_new=[]

    Result=np.loadtxt(FileAddress,dtype=float)
    Time=np.reshape(Result[:,0],(len(Result),1))*10**+9
    Data=np.reshape(Result[:,1],(len(Result),1))
    Target=np.reshape(Result[:,3],(len(Result),1))

    # interpolate(fix) vectors
    for i in range(1,len(Time)):
        Time_new=[*Time_new[0:len(Time_new)-1],*(interpolator(Time[i],Time[i],Time[i-1],Time[i-1]))]
        Data_new=[*Data_new[0:len(Time_new)-1],*(interpolator(Data[i],Time[i],Data[i-1],Time[i-1]))]
        Target_new=[*Target_new[0:len(Target_new)-1],*(interpolator(Target[i],Time[i],Target[i-1],Time[i-1]))]
        print(str(100*i/len(Time))+"% passed interpolating")
    print("100.00%  passed interpolating ")

    # reshape and downsample fixed data
    Time_new =np.reshape(downsampler(np.array(Time_new)*10**-9,FinalLength),(FinalLength, ))
    print('Time vector downsampled')
    Data_new =np.reshape(downsampler(np.array(Data_new),FinalLength),(FinalLength, ))
    print('Data vector downsampled')
    Target_new=np.reshape(downsampler(np.array(Target_new),FinalLength),(FinalLength, ))
    print('Target vector downsampled')

    # return fixed and downsampled space
    FixedResult=np.transpose((Time_new,Data_new,Target_new))
    return FixedResult
