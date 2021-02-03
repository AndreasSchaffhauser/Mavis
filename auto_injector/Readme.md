# MS-AutoInjector
The Malicious Script AutoInjecter (MS-AutoInjecter) is a tool for building up a database of images containing hidden malicious content. It injects malicious PowerShell Scripts into images using the moduele Invoke-PSImage tool. Outgoing from a clean image dataset in the resolution 1024x1024, 512x512 and 256x256, it creates a directory structure with images of different resolutions.

## Prerequisites
In the following subsections you can see the additional software, which uses the automatization process. 

### IStego100K
Clean images for the injection process can be downloaded via the repository https://github.com/YangzlTHU/IStego100k. They offer 100,000k clean cover images in a resolution of 1024x1024 for the creation of the database.

### Invoke-PSImage
The tool is reachable under the repository https://github.com/peewpw/Invoke-PSImage. It offers to core functionality for the injection. The script encodes a PowerShell script in the pixels of a PNG file and generates a oneline to execute.

### ImageResizer
The ImageResizer for Windows is a tool to rescale in an easy manner. The tool can be downloaded and installed via the following link: https://www.bricelam.net/ImageResizer/. You can use it, if you change to the directory with the image files, right-click on all images you want to rescale and click "Rescale images..." on the context menu.

### ImageMagick
This tool can be used to convert a clean JPG-File to a PNG-File. The tool is necessary to execute the MS-AutoInjecter tool. It can be downloaded under https://imagemagick.org/script/download.php. If you have a 64-bit Windows Version, download a version with dynamic link libraries (dll in filename).  

## Software Execution
For the execution of the MS-AutoInjecter a specific directory structure is needed:

	|
	|
	|	-----------------------
	|---| 256x256 (directory) |
	|	-----------------------
	|
	|	-----------------------
	|---| 512x512 (directory) |
	|	-----------------------
	|
	|	-------------------------
	|---| 1024x1024 (directory) |
	|	-------------------------	         --------------------------
	|								 --------| obfuscated (directory) |
	|	-------------------------	 |       --------------------------
	|---|  scripts (directory)  |----|		  
	|	-------------------------	 |		 ----------------------------
	|						  		 --------| deobfuscated (directory) |
	|	----------------					 ----------------------------
	|---|  inject.ps1  |
	|	----------------
	|
	|	------------------------
	|---|  Invoke-PSImage.ps1  |
		------------------------

- The directories 256x256, 512x512, 1024x1024 are containing the cover images, which shall be used for the injection.
- The directory scripts contains two subdirectories called obfuscated and deobfuscated. These two subdirectories contain obfuscated and deobfuscated malicious PowerShell Scripts. There are 4018 obfuscated and 4641 deobfuscated scripts present for the injection process.

During the execution a file called execution_log is written. It contains all the executed commands and serves as a possibility to understand if everything works in a correct manner.

## Mode-1 Injection
The mode-1 injection uses all malicious scripts (obfuscated & deobfuscated), which are placed in the scripts directory. For every malicious script of these scripts an image with Invoke-PSImage is produced by injecting the malicious script and using the malicious script as input for the production of the cover image.  

## Mode-2 Injection
The mode-2 injection uses the cover images, which are placed in the directories 256x256, 512x512 and 1024x1024. Then as many malicious scripts are then injected into the images as is determined by the cluster_number variable. The cluster_number amount will be applied to all 12 resulting subdirectories under the images directory.
