**LAN Share Simple File Host**



*Getting Started*


&nbsp;  Make sure to have Python 3 installed.

&nbsp;	Double click run.bat to start the server. This will generate a config.ini, and a folder called Files. The server will host all files placed into the Files folder automatically.
	Access the webpage at http://[your local IP address]:port.

&nbsp;	Look up how to identify your system's local IP address based on the operating system that you're using. The URL should look something like this:

&nbsp;	http://192.168.1.2:8000



*Configuration*



&nbsp;	To change server settings edit the config.ini file in any text editor.

&nbsp;	hosted\_directory : \[The path of the folder you would like to host. This must be an absolute path.]
	default\_block\_size : \[Chunk size for range downloads (used for streaming video)]



*Changing the port*



&nbsp;	Set the port in config.ini. Then modify the run.bat start command with the new port.

