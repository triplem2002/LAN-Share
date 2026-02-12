***LAN Share Simple File Host***



**Getting Started**



Double click run.bat or start.sh to start the server. Alternatively open a terminal and call python server.py.

This will generate a config.ini, and a folder called Files. The server will host all files placed into the Files folder automatically.
Access the webpage at http://\[your local IP address]:port.

Look up how to identify your system's local IP address based on the operating system that you're using. The URL should look something like this:

http://192.168.1.2:8000



**Configuration**



To change server settings edit the config.ini file in any text editor.

hosted\_directory : \[The path of the folder you would like to host. This must be an absolute path.]
default\_block\_size : \[Chunk size for range downloads (used for streaming video)]



**Changing the port**



Set the port in config.ini. Then modify the run.bat start command with the new port.

