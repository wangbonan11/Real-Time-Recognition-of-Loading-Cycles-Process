# Real-Time-Recognition-of-Loading-Cycles-Process
## 1.Objective
An algorithm is developed to recognize and understand the shovel loading operation automatically. The start time and end time of each shovel loading operation are determined by automatic recognition of the shovel cycle operation process (digging, loading swing, dump, empty bucket return) based on the real-time collection of shovel working parameters.
## 2.Basic Structure of the Algorithm
### 2.1Data acquisition
* Read the original data file
* Select the primary property parameter
### 2.2Data preprocessing
* Time data in standard format is converted into time stamps
* Abnormal time value preprocessing
* Abnormal positioning data preprocessing
* Non-continuous processing of swing Angle data
* Calculate the power of the motor from the voltage and current of the motor
### 2.3Data mining
* The working time and standby time of the shovel were obtained by time data analysis
* Build a function that recognizes the shovel cycle
### 2.4Data output
* DTW algorithm detects and classifies the preliminary recognition results
* Statistics and output effective shoveling cycles
* Visualization of recognition results of shovel loading cycle
## NOTE:
Version: Python 3.7.0
