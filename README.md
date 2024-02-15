
# Generative-Design-Space-Exploration

Generative DSE aims at automatically exploring application-specific architecture solutions additionally to the decisions on the system synthesis.

The framework has been tested for 
- clingo version 5.7.0,
- clingo-dl version 1.4.1 and 
- Python version 3.10.10.

## Directory structure

### **encodings** 
- Contains the ASP encodings allowing the exploration of different architecture topologies while considering the different system synthesis steps.
- Directory is structured according to the system synthesis tasks (allocation, binding, routing, scheduling) and the preprocessing steps.

### **scripts** 
- Contains the project execution script called in the experiments for the paper.
- Contains scripts for the evaluation of experimental results.

### **src**
- Contains our framework for the DSE
- Based on https://github.com/wanko/dse

### **visualization**
 - Cotains encodings for system model visualization
 - Using the tool clingraph: see [clingraph publication](https://link.springer.com/chapter/10.1007/978-3-031-15707-3_31)
