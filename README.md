# Mavis
Mavis is anti-malware software for Invoke PS-Image. Mavis enables the possiblity to detect both modes (mode-1 and mode-2) in images altered with Invoke PS-Image. Invoke PS-Image is a tool that injects malicious Powershell scripts into images using LSB steganography. Invoke PS-Image offers two modes:
- Mode-1: no cover image is needed. The resulting image is created by the bytes of the malicious PowerShell script. All three color channels are used. In each byte of a channel (R,G,B), one byte of the malicious PowerShell is injected.
- Mode-2: a cover image is needed. Every byte of the malicious PowerShell script is injected in the blue and the green channel. The 4 MSB are injected in the blue, the 4 LSB are injected in the green channel.

## Usage of Mavis
Mavis can be used on files or on complete directories containing benign/malicious images. With the -f flag you can specify a file. With the -d flag you can specify a directory. If you want to write the resumée of the investigations to a csv-file, you can specifiy that with the -c Flag. If not, the output of every file is written to the shell.

```
python mavis.py --help
Usage: mavis.py [options]

Options:
  -h, --help            show this help message and exit
  -f FILE, --file=FILE  Specify the file (PNG-format) that you want to check
  -d DIRECTORY, --directory=DIRECTORY
                        Specify the directory which contains files (PNG-
                        format) that you want to check
  -c CSV, --csv=CSV     Write the output log to a csv file: default is to
                        wrote on the shell
```
## Dataset
The dataset what we used for our research pruposes contains 45,000 malicious images, which contain 4,641 deobfuscated malicious PowerShell Scripts and 4,018 obfuscated malicious PowerShell Scripts in different resolutions. Every resolution cluster, namely 256x256, 512x512 and 1024x1024 includes 15,000 images (5,000 clean, 5,000 deobfuscated and 5,000 obfuscated) containing the scripts. Every image occures in all three forms.

Additionally to the 45k malicious images, there are 4,641 mode-1 deobfuscated images and 4,018 mode-1 obfuscated images. 
 
You can download the dataset under: https://www.dropbox.com/s/1go9ic8mmske8e6/images.zip?dl=0

## Example for a malicious PNG-File
In the following you can see a PNG-File, which contains a malicious script injected via Invoke-PSImage.
<img src="malicious.png">

## Acknowledgements 
This work was supported by the Horizon 2020 Program through [SIMARGL](https://simargl.eu/) H2020-SU-ICT-01-2018, Grant Agreement No. 833042.
