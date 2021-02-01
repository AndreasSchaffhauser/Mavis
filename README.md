# Mavis
Mavis is anti-malware software for Invoke PS-Image. Mavis enables the possiblity to detect both modes (mode-1 and mode-2) in images altered with Invoke PS-Image. Invoke PS-Image is a tool that injects malicious Powershell scripts into images using LSB steganography. Invoke PS-Image offers two modes:
- Mode-1: no cover image is needed. The resulting image is created by the bytes of the malicious PowerShell script. All three color channels are used. In each byte of a channel (R,G,B), one byte of the malicious PowerShell is injected.
- Mode-2: a cover image is needed. Every byte of the malicious PowerShell script is injected in the blue and the green channel. The 4 MSB are injected in the blue, the 4 LSB are injected in the green channel.

 
