
# ProjectSE

Quantum-resistant selective encryption using 2D-DWT.


## Installation

Install ProjectSE with pip

```bash
  pip install -r requirements.txt
```
For post quantum encryption, [liboqs-python](https://github.com/open-quantum-safe/liboqs-python) is used. This is the only library at the time of writing that can run on ARM devices (architecture for most edge devices).

The installation steps for this library could be found at [Install liboqs-python](https://github.com/open-quantum-safe/liboqs-python?tab=readme-ov-file#installation).


## Usage/Examples


[PostQuantumSelectiveEncryption.ipynb](https://github.com/Patriot-Lab/ProjectSE/blob/master/PostQuantumSelectiveEncryption.ipynb) contains a demo for the quantum-resistant selective encryption.

[pq_se_pi_run.py](https://github.com/Patriot-Lab/ProjectSE/blob/master/pq_se_pi_run.py) captures the time taken on a raspberry pi device to perform quantum-resistant (ML-KEM-1024) selective encryption for a collection of images with varying read buffer size.

[pq_se_ml_dsa_pi_run](https://github.com/Patriot-Lab/ProjectSE/blob/master/pq_se_ml_dsa_pi_run.py) captures the time taken for signature verification of images using ML-DSA on a raspberry pi device.

## Analysis

[LogParser.ipynb](https://github.com/Patriot-Lab/ProjectSE/blob/master/LogParser.ipynb) parses the raw log outputs from above scripts to csv files.

[BufferSizeOptimization.ipynb](https://github.com/Patriot-Lab/ProjectSE/blob/master/BufferSizeOptimization.ipynb) reads the csv files and generates plots to determin best performing buffer size. It also plots the time taken for each individual step of the proposed approach.

[SecurityAnalysis.ipynb](https://github.com/Patriot-Lab/ProjectSE/blob/master/SecurityAnalysis.ipynb) performs statistical and uniformity analysis of the encrypted data.




