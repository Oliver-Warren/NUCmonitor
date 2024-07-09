# NUC Power Monitor

## Overview

Many AC powered NUCs do not have on-board power consumption monitoring capabilities. Scripts in this repo aim to deliver a solution in the form of a predictive model for the system-level power consumption, trained using the following features, available on Intel NUC systems running Ubunutu Server 22 or later:

* CPU socket average power consumption. The file /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj (found on Ubuntu systems with Intel CPUs that support RAPL) is read twice, each read separated by a second, and average power consumption over the one second interval is calculated as the difference between the two values.
* CPU load. Obtained using from the file /proc/loadavg, the model uses three stats: average load over one minute, five minutes and fifteen minutes.
* CPU temp. Read using !TODO-update! thermal zone file.
* RX and TX datarates per interface. Calculated by successive reads to /proc/net/dev one second apart, datarate is provided by comparing the values for transmitted bytes in each direction on each interface.

Targets for the model originate from APC smart meter readings corresponding to a range of CPU and interface stress scenarios. These scenarios are driven from a separate machine with network access to the NUC, abusing PyTests ability to iterate over a cartesian product of parameter values.

## Methods
Deployment of the solution involves three stages:

1. Data generation. Driving a range of cases related to different CPU and network interface loads, and recording system-level power consumption.
2. Train and test model. Select and apply an appropriate modelling framework, validate predictions.
3. Deploy model on the NUC. Trained models can then be stored on the NUC and used to estimate power consumption for uses such as Real-time Intelligent Control.

### Data generation
The NUC is stress tested by abusing pytest on a remote machine, calling stress-ng and iperf over a range of different parameters.

1. Interface loading. Interface loading is achieved by hosting an iperf server on the DUT, and running the script provided under /NUCmonitor/clientSide/monitoringTool_test.py on an alternative network device to create a range of iperf traffic, including duplex and parallel connections.
2. CPU loading. CPU loading is achieved using the stress-ng tools for Linux systems.
3. Recording. While either or both of the interface and CPU loading processes are underway. The NUC collects and record datapoints containing all above model features, as well as recording system-power consumption using a metered PDU (by SSH). Features are calculated and saved using methods defined in the file NUCmonitor/dutSide/monitoringTool.py, specifically the function 'monitor()'. Also included in this library are individual methods for performing each of the required reads, and to output statistics as a json portable object.

### Modelling
1. Model selection. Models should be as simple as possible, so that when they are deployed on the NUC they do not draw significant resources and are able to run as a low-intensity background service. The file model.py contains scripts that test a variety of SciKit Learn package models and report the most appropriate. Hyperparamater tuning and CV is not implemented at the time of writing. Tests found that simple Linear Regression performs well for this task, also a nice balance between accuracy and simplicity.
2. Training. Training and testing uses an 80/20 test train split. This technique is typical for this kind of modelling, but can be tuned as required.

### Deployment
Once the Linear Regression model is trained, its enclosing Python object is "pickled" and then transferred to the NUC via Git. The NUC then "unpickles" the model object and can use it for estimating its power consumption using live data in real-time.

### Results
The deployed model is shown to be effective, and can be verfied by using the testNUC.py file, setting the modelOn option of the NUC object to true. Running this script prints the features, predicted power and actual metered power to the terminal, allowing verification via manually observing the difference between power consumption recorded by the metered PDU, and that estimated by the deployed model.
   
## Risks
* Portability. The gathering of statistics is highly dependent on the systems componnents and OS. This solution may not be portable to non-Ubuntu OSs, and CPU power consumption monitoring based on RAPL will not work on: a) systems using Intel CPUs that don't support RAPL; b) systems using non-Intel CPUs.
* Overfitting. This process aims to generate a dataset representating CPU and interface loads typical for a NUC operating as a software enabled access point. Data does not account for cases with power consumption caused by external devices. The model is likely to underestimate system power consumption, if the NUC is providing significant power to other external such as HAT interfaces.
