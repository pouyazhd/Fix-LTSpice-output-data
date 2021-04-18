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

CAUTION: it's work for only 1 input and 1 output signals, but it's open source and you (as a developer) can modify it as you need.
but this problem will be fixed soon and work for dynamicly range of data

***********************
Developer: P.Zahedi
E-mail: p.zahedi@live.com
'''

import numpy as np
from scipy.interpolate import interp1d



     # interpolate 
def UniformSteps(SampleData,TimeSteps=200,kind='linear'):
    '''
    SampleData : array of none uniform distributed data of time, input and target.
    TimeSteps: number of output steps, default 200 row of data will generate.
    kind: interpolation kind. defulat is linear but it can be 'nearest' , 'cubic' or etc. (look at scypy documents).
    '''    
     
    #interpolate data
    input_interpolate=interp1d(SampleData[:,0],SampleData[:,1],kind=kind)
    output_interpolate=interp1d(SampleData[:,0],SampleData[:,2],kind=kind)

    #find border of Time vector and generate new time vector with fixed steps
    mintime=min(SampleData[:,0])
    maxtime=max(SampleData[:,0])
    newtime=np.linspace(mintime ,maxtime,num=TimeSteps,endpoint=False)
    
    return np.transpose([newtime,input_interpolate(newtime),output_interpolate(newtime)])


def SavedUniformedData(UniformedFileAddress,UniformedData,delimiter='\t'):
    ''' 
    UniformedFileAddress: name and address of uniformed  data to save it. .txt format
    UniformedData: array of data that has been uniformed in given steps.
    delimiter: delimiter of output file
    '''
    np.savetxt(UniformedFileAddress,UniformedData ,delimiter=delimiter)
    print('werite succesfull')
