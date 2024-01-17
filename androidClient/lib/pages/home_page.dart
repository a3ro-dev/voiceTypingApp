import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomePage(),
      theme: ThemeData.light(),
      darkTheme: ThemeData.dark(),
      themeMode: ThemeMode.system, // Default mode
    );
  }
}

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _controller = TextEditingController();
  String filePath = '';
  bool isDarkMode = false;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onTextChanged);
    getFilePath();
  }

  void _onTextChanged() {
    List<String> words = _controller.text.split(' ');
    if (words.length % 3 == 0) {
      writeToFile(_controller.text);
    }
  }

  void getFilePath() async {
    Directory? directory = await getExternalStorageDirectory();
    String newPath = '';
    List<String> folders = directory!.path.split('/');
    for (int x = 1; x < folders.length; x++) {
      String folder = folders[x];
      if (folder != 'Android') {
        newPath += '/' + folder;
      } else {
        break;
      }
    }
    newPath = newPath + '/Documents/voicetypingdata';
    directory = Directory(newPath);
    if (!await directory.exists()) {
      await directory.create(recursive: true);
    }
    if (await directory.exists()) {
      filePath = directory.path + '/voicetypingdata.txt';
      File file = File(filePath);
      if (!await file.exists()) {
        await file.create();
      }
    }
  }

  void writeToFile(String text) async {
    File file = File(filePath);
    await file.writeAsString('$text\n');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CupertinoNavigationBar(
        middle: const Text('VoiceTyping'),
        trailing: CupertinoSwitch(
          value: isDarkMode,
          onChanged: (value) {
            setState(() {
              isDarkMode = value;
              (isDarkMode)
                  ? SystemChrome.setSystemUIOverlayStyle(
                      SystemUiOverlayStyle.dark)
                  : SystemChrome.setSystemUIOverlayStyle(
                      SystemUiOverlayStyle.light);
            });
          },
        ),
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(8.0),
          child: TextField(
            controller: _controller,
            decoration: const InputDecoration(
              border: OutlineInputBorder(),
              labelText: 'Type here',
            ),
          ),
        ),
      ),
    );
  }
}