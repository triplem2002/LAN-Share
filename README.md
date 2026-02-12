##### **LAN Share Simple File Host**



###### **Getting Started**



**Installation:** Install Python3.X.



**Running the App:** 

* Open Terminal, CMD, or PowerShell on the application folder and run: \[python3 server.py] or \[python server.py]. Use run.bat for convenience on Windows.
* This will generate a config.ini, and a folder called Files. The server will host all files placed into the Files folder automatically.
  

**Access the webpage:** 

* The server hosts a client on a webpage at: http://192.168.XXX.XXX:XXXXX
* Look up how to identify your system's local IP address based on the operating system that you're using. The default port is 8000.
* The URL should look something like this: http://192.168.1.X:8000
* Open the URL from any web browser connected on your local network. Make sure network discovery is on. This will only work on private (home) networks.



###### **Configuration**



* To change server settings edit the config.ini file in any text editor.
* hosted\_directory : \[The path of the folder you would like to host. This must be an absolute path.]
* default\_block\_size : \[Chunk size for range downloads (used for streaming video)]



###### **Changing the port**



Set the port in config.ini.

