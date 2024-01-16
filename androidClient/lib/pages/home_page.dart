import 'dart:async';
import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';
import 'package:socket_io_client/socket_io_client.dart' as IO;
import 'package:voicetypingapp/theme/theme_provider.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  IO.Socket? socket;
  final TextEditingController _controller = TextEditingController();
  final TextEditingController _ipController =
      TextEditingController(text: '192.168.31.209');
  bool isConnected = false;
  Timer? timer;

  @override
  void initState() {
    super.initState();
    connectSocket();
  }

  Future<void> connectSocket() async {
    socket = IO
        .io('http://${_ipController.text}:3000/send_message', <String, dynamic>{
      'transports': ['websocket'],
    });
    socket?.onConnect((_) async {
      print('Connected');
      setState(() {
        isConnected = true;
      });
      timer?.cancel(); // Cancel the timer when connected
    });
    socket?.onDisconnect((_) {
      print('Disconnected');
      setState(() {
        isConnected = false;
      });
      // Start a timer that tries to reconnect every 5 seconds
      timer = Timer.periodic(
          const Duration(seconds: 5), (Timer t) => connectSocket());
    });
  }

  void _showActionSheet(BuildContext context) {
    showCupertinoModalPopup<void>(
      context: context,
      builder: (BuildContext context) => CupertinoActionSheet(
        title: const Text('Settings'),
        message: const Text('Toggle Dark/Light Mode'),
        actions: <CupertinoActionSheetAction>[
          CupertinoActionSheetAction(
            child: CupertinoSwitch(
              value: Provider.of<ThemeProvider>(context).isDarkMode,
              onChanged: (value) =>
                  Provider.of<ThemeProvider>(context, listen: false)
                      .toggleTheme(),
            ),
            onPressed: () {},
          ),
          CupertinoActionSheetAction(
            child: Text(isConnected ? 'Connected' : 'Disconnected'),
            onPressed: () {},
          ),
          CupertinoActionSheetAction(
            child: CupertinoTextField(
              controller: _ipController,
              placeholder: 'Enter server IP',
            ),
            onPressed: () {},
          ),
        ],
        cancelButton: CupertinoActionSheetAction(
          isDefaultAction: true,
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('Cancel'),
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: const Text('Voice Typing App'),
        leading: CupertinoButton(
          child: const Icon(CupertinoIcons.settings),
          onPressed: () => _showActionSheet(context),
        ),
      ),
      child: SafeArea(
        child: Center(
          child: CupertinoTextField(
            controller: _controller,
            onSubmitted: (String text) async {
              socket?.emit('message', text);
              _controller.clear();
            },
          ),
        ),
      ),
    );
  }

  @override
  void dispose() {
    socket?.dispose();
    timer?.cancel(); // Cancel the timer when the widget is disposed
    super.dispose();
  }
}
