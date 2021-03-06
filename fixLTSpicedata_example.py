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

***********************
to use this softare type in terminal: 
python3.8 fixLTspice data.py <original file> <number of output point> 
'''

import numpy as np
import sys
import fixLTSpicedata as LTfixer

if __name__ == "__main__":
    # read sys args 
    FileAddress=sys.argv[1]
    DownsampleNum=int(sys.argv[2])
    FixedFileAddress='Fixed/'+sys.argv[1]

    # read data
    SampleData=np.loadtxt(FileAddress,dtype=float)
    
    # fix (inter polate and downsample the dataset file)
    FixedResult = LTfixer.UniformSteps(SampleData,DownsampleNum)
    
    # save fixed data
    LTfixer.SavedUniformedData(FixedFileAddress,FixedResult)
