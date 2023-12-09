### Cytovs - v0.1

## Purpose

Cytovs is a simple python GUI program that is used to process CSV data derived from Mass-Spectrometry (MS) through Cytoscape API in combination with cytoscape stringApp and AutoAnnotate.

## Requirements

Cytoscape 3.10 or greater: https://cytoscape.org/download.html

Cytoscape Apps:
- stringApp: https://apps.cytoscape.org/apps/stringapp
- AutoAnnotate: https://apps.cytoscape.org/apps/autoannotate

You must ensure that you have python installed on your system. If not, download and install Python: https://www.python.org/downloads/

Check the file 'requirements.txt' for python modules required by Cytovs.

```
pip install -r requirements.txt
```

Cytovs communicates with Cytoscape CyREST API through the py4cytoscape python module.

## Usage

Starts Cytoscape software and make sure you installed the stringApp and AutoAnnotate.

Download or clone the archive, and run as follows:

```
python cytovs.py
```
## Authors

Dr. Florian Malard (florian.malard@gmail.com)
Prof. Dr. Stéphanie Olivier-van Stichelen (solivier@mcw.edu)
