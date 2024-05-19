### Cytovs - v0.1

If you use *cytovs* in your work, please cite:

Malard F, Wulff-Fuentes E, Berendt R, Didier G and Olivier-Van Stichelen S. **Studying the O-GlcNAcome of human placentas using banked tissue samples**. *Glycobiology*, 34(4), (2024).

## Purpose

Cytovs is a simple python GUI program that is used to process CSV data derived from Mass-Spectrometry (MS) through Cytoscape API in combination with cytoscape stringApp and AutoAnnotate.

![cytovs](cytovs.png)

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

If you are a MacOS 14 user, you may have problem with tkinter (GUI), see https://stackoverflow.com/questions/73056296/tkinter-on-mac-shows-up-as-a-black-screen to solve the issue.

## Usage

Starts Cytoscape software and make sure you installed the stringApp and AutoAnnotate.

Download or clone the archive, and run as follows:

```
python cytovs.py
```
