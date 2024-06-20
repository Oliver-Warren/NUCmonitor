# NUC Power Monitor

## Overview

Many AC powered NUCs do not have on-board power consumption monitoring capabilities. Scripts in this repo aim to deliver a solution in the form of a predictive model for the system-level power consumption, trained using the following features:

* CPU socket average power consumption. The file /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj (found on Ubuntu systems with Intel CPUs that support RAPL) is read twice, each read separated by a second, and average power consumption over the one second interval is calculated as the difference between the two values.
* CPU load. Obtained using from the file /proc/loadavg, the model uses three stats: average load over one minute, five minutes and fifteen minutes.
* CPU temp. Read using !TODO-update! thermal zone file.
* RX and TX datarates per interface. Calculated by successive reads to /proc/net/dev one second apart, datarate is provided by comparing the values for transmitted bytes in each direction on each interface.

These features are selected in order to provide the model with adequete information regarding the activity of the most power-intensive system components (for a NUC configured as a SoftAP): the CPU and network interfaces. Modelling targets are obtained by use of a PDU or other power source that is able to measure system-level power consumption, and datapoints are gathered for a large selection of CPU and interface loads, driven using the stress-ng and iperf commands. The result is a dataset relating the above features to instantaneous system power consumption, on which a model can be trained to predict system-level power consumption.

## Methods
Deployment of the solution involves three stages:

1. Data generation. Driving a range of cases related to different CPU and network interface loads, and recording system-level power consumption.
2. Train and test model. Select and apply an appropriate modelling framework, validate predictions.
3. Deploy model on the NUC. Trained models can then be stored on the NUC and used to estimate power consumption for uses such as Real-time Intelligent Control.

### Data generation
1. Interface loading. Interface loading is achieved by hosting an iperf server on the DUT, and running the script provided under /NUCmonitor/clientSide/monitoringTool_test.py on an alternative network device to create a range of iperf traffic, including duplex and parallel connections.
2. CPU loading. CPU loading is achieved using the stress-ng tools for Linux systems.
3. Recording. While either or both of the interface and CPU loading processes are underway. The DUT must monitor and record datapoints containing all above model features, as well as recording system-power consumption either using a PDU or by manual observation and entry using data available for a battery (current method). Features are calculated and saved using methods defined in the file NUCmonitor/dutSide/monitoringTool.py, specifically the function 'monitor()'. Also included in this library are individual methods for performing each of the required reads, and to output statistics as a json portable object.

### Modelling
1. Model selection. Models should be as simple as possible, so that when they are deployed on the NUC they do not draw significant resources and are able to run as a low-intensity background service. The quantitative nature of the features would lend itself well to regression or a KNN classifier (although the use of a classifier will restricts the models output to power consumption that are present in the dataset, and would only be effective if the system power data is sufficiently low-res). A more complicated approach could employ a Linear Dynamical System, which is able to use sequential data to make predictions, but may be too complex to efficiently deploy on the NUC.
2. Training. Training and testing uses an 80/20 test train split with cross-validation in the training set. This technique is typical for this kind of modelling, but can be tuned as required.

### Deployment
Once a satisfactory model is produced, it must be encapsulated in software as a portable service to be run on the NUC. Wherever possible, PCA should be applied to reduce the dimensionality and memory required by the supporting data, minimising the footprint of the model and its use of NUC resources.
   
## Risks
* Portability. The gathering of statistics is highly dependent on the systems componnents and OS. This solution may not be portable to non-Ubuntu OSs, and CPU power consumption monitoring based on RAPL will not work on: a) systems using Intel CPUs that don't support RAPL; b) systems using non-Intel CPUs.
* Overfitting. This process aims to generate a dataset representating CPU and interface loads typical for a NUC operating as a software enabled access point. Data does not account for cases with power consumption caused by external devices. The model is likely to underestimate system power consumption, if the NUC is providing significant power to other external such as HAT interfaces.
