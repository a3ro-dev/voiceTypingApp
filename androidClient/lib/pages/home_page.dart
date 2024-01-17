import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import 'package:url_launcher/url_launcher.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final TextEditingController _controller = TextEditingController();
  String filePath = '';
  int wordCount = 1;

  @override
  void initState() {
    super.initState();
    _controller.addListener(_onTextChanged);
    getFilePath();
  }

void _onTextChanged() {
  if (_controller.text.endsWith(' ') || _controller.text.isEmpty) {
    List<String> words = _controller.text.trim().split(' ');
    if (words.isNotEmpty) {
      writeToFile('$wordCount: ${words.last}');
      wordCount++;
    }
  }
}

  void getFilePath() async {
    Directory? directory = await getExternalStorageDirectory();
    String newPath = '';
    List<String> folders = directory?.path.split('/') ?? [];
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
      if (await file.exists()) {
        await file.delete();
      }
      await file.create();
    }
  }

  void writeToFile(String text) async {
    File file = File(filePath);
    await file.writeAsString('$text\n', mode: FileMode.append);
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: CupertinoNavigationBar(
        middle: Text('VoiceTyping', style: TextStyle(color: CupertinoColors.white)),
        backgroundColor: CupertinoColors.activeBlue,
        trailing: CupertinoButton(
          padding: EdgeInsets.zero,
          child: Icon(CupertinoIcons.info, color: CupertinoColors.white),
          onPressed: () async {
            const url = 'https://www.example.com';
            if (await canLaunch(url)) {
              await launch(url);
            } else {
              throw 'Could not launch $url';
            }
          },
        ),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Material(
            elevation: 8.0,
            borderRadius: BorderRadius.circular(8.0),
            child: CupertinoTextField(
              controller: _controller,
              padding: EdgeInsets.all(16.0),
              placeholder: 'Type here',
              decoration: BoxDecoration(
                color: CupertinoColors.white,
                borderRadius: BorderRadius.circular(8.0),
              ),
            ),
          ),
        ),
      ),
    );
  }
}