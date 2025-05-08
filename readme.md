# Assignment3

## Directory Structure

```
assignment3/
├── server.py
├── clients.py
├── test-workload/
│   ├── client_1.txt
│   ├── client_2.txt
│   └── ...
└── README.md

ps: client.py and txts are rubbish now
```

## Running the Server

Start the server on the default host (`localhost`) and port (`51234`):

```bash
python server.py
```

If you want to change the port, you should edit the *server.py* and *clients.py*

The server will listen for incoming connections, process requests, and print a summary of the tuple space every 10 seconds.

## Running the Client

The client script automatically processes all request files in `test-workload/`. Simply run:

```bash
python clients.py
```

## License

This project is released under the MIT License. Feel free to use and modify.

