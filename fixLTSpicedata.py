'''
Laus deo
fix LTSpice data
LTSpice is a free opensource tool for simulating digital and analog circuit.
The point is after save the result of simulation, the software automatically choose the sampleling frequency and it's not a constant.
During my search it's an unsolved problem and I tried to fix it. 

***********************
in data file :  
          Time: SampleData[:,0] 1st column
          Data: SampleData[:,1] 2nd column
        Target: SampleData[:,2] 3rd column 

***********************
Developer: P.Zahedi
E-mail: p.zahedi@live.com
'''

import numpy as np
from scipy.interpolate import interp1d



    # change inter polate between points and uniform the sampeling steps
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

    # uniform data more accurate 
def UniformStepsMeticulous(SampleData,TimeSteps=200):
    '''
    This function will produce a very large vector of Data, has alot of calculation but time steps are equivalent
    SampleData : array of none uniform distributed data of time, input and target.
    TimeSteps: number of output steps, default 200 row of data will generate.    
    '''
    SampleData[:,0]=SampleData[:,0]*10**+9
    UniformedData=[0]*np.shape(SampleData)[1]

    # interpolate (uniform) vectors
    for j in range(len(UniformedData)):
        for i in range(1,len(SampleData[:,0])):
            
            # interpolate and uniform data 
            UniformedData[j]=[*UniformedData[0:len(UniformedData)-1],*(interpolator(SampleData[:,j][i],SampleData[:,0][i],SampleData[:,j][i-1],SampleData[:,0][i-1]))]

            #downsample the large vector with given time steps
            if j==0:
                UniformedData[j] =np.reshape(downsampler(np.array(UniformedData[j])*10**-9,TimeSteps),(TimeSteps, ))       
            else:
                UniformedData[j] =np.reshape(downsampler(np.array(UniformedData[j]),TimeSteps),(TimeSteps, ))       

            print(str(100*i/len(SampleData[:,0]))+"% passed interpolating")
    print("100.00%  passed interpolating ")

    
    # return fixed and downsampled space
    return np.transpose(UniformedData)




    # interpolate 
def UniformSteps(SampleData,TimeSteps=200,kind='linear'):
    '''
    SampleData : array of none uniform distributed data of time, input and target.
    TimeSteps: number of output steps, default 200 row of data will generate.
    kind: interpolation kind. defulat is linear but it can be 'nearest' , 'cubic' or etc. (look at scypy documents).
    '''    
    
    UniformedData=[0]*np.shape(SampleData)[1]
    
    #find border of Time vector and generate new time vector with fixed steps
    mintime=min(SampleData[:,0])
    maxtime=max(SampleData[:,0])
    UniformedData[0]=np.linspace(mintime ,maxtime,num=TimeSteps,endpoint=False) # new time steps

    #interpolate data
    for i in range(1,len(UniformedData)):
        interpolatedfunction=interp1d(SampleData[:,0],SampleData[:,i],kind=kind)
        UniformedData[i]=interpolatedfunction(UniformedData[0])

      
    return np.transpose(UniformedData)


def SaveUniformedData(FileSaveAddress,UniformedData,delimiter='\t'):
    ''' 
    FileSaveAddress: name and address of uniformed  data to save it with .txt format.
    UniformedData: array of data that has been uniformed in given steps.
    delimiter: delimiter of output file
    '''
    np.savetxt(FileSaveAddress,UniformedData ,delimiter=delimiter)
    print('werite succesfull')
