import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:shared_preferences/shared_preferences.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  IO.Socket? socket;
  bool isConnected = false;
  bool isConnecting = false;
  bool isPaused = false;
  String serverIp = '';
  List<String> serverList = [];
  String selectedServer = '';

  @override
  void initState() {
    super.initState();
    loadServerList();
  }

  Future<void> loadServerList() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    serverList = prefs.getStringList('serverList') ?? [];
    if (serverList.isNotEmpty) {
      selectedServer = serverList.first;
    }
  }

  Future<void> saveServerList() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    await prefs.setStringList('serverList', serverList);
  }

  void connect() async {
    setState(() {
      isConnecting = true;
    });

    socket = IO.io('http://$selectedServer:3000', <String, dynamic>{
      'transports': ['websocket'],
    });
    socket?.onConnect((_) {
      setState(() {
        isConnected = true;
        isConnecting = false;
      });
    });
    socket?.onDisconnect((_) {
      setState(() {
        isConnected = false;
      });
    });
    socket?.onError((data) {
      setState(() {
        isConnecting = false;
      });
      showDialog(
        context: context,
        builder: (context) => CupertinoAlertDialog(
          title: const Text('Connection Error'),
          content: Text('Error: $data'),
          actions: <Widget>[
            CupertinoDialogAction(
              child: const Text('OK'),
              onPressed: () {
                Navigator.of(context).pop();
              },
            ),
          ],
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar(
        middle: Text('Voice Typing App'),
      ),
      child: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              if (serverList.isNotEmpty)
                CupertinoPicker(
                  itemExtent: 32.0,
                  onSelectedItemChanged: (index) {
                    selectedServer = serverList[index];
                  },
                  children: serverList.map((server) => Text(server)).toList(),
                ),
              CupertinoButton.filled(
                child: const Text('Connect'),
                onPressed: () async {
                  await showDialog(
                    context: context,
                    builder: (context) => CupertinoAlertDialog(
                      title: const Text('Enter Server IP'),
                      content: CupertinoTextField(
                        onChanged: (text) {
                          serverIp = text;
                        },
                      ),
                      actions: <Widget>[
                        CupertinoDialogAction(
                          child: const Text('Cancel'),
                          onPressed: () {
                            Navigator.of(context).pop();
                          },
                        ),
                        CupertinoDialogAction(
                          child: const Text('Connect'),
                          onPressed: () {
                            if (!serverList.contains(serverIp)) {
                              serverList.add(serverIp);
                              saveServerList();
                            }
                            selectedServer = serverIp;
                            connect();
                            Navigator.of(context).pop();
                          },
                        ),
                      ],
                    ),
                  );
                },
              ),
              if (isConnecting) const CupertinoActivityIndicator(),
              if (isConnected)
                Column(
                  children: <Widget>[
                    CupertinoTextField(
                      onChanged: (text) {
                        if (!isPaused) {
                          socket?.emit('message', text);
                        }
                      },
                    ),
                    CupertinoButton.filled(
                      child: Text(isPaused ? 'Resume' : 'Pause'),
                      onPressed: () {
                        setState(() {
                          isPaused = !isPaused;
                        });
                      },
                    ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
