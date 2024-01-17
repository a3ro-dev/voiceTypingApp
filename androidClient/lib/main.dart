import 'package:flutter/material.dart';
import 'package:voicetypingapp/pages/home_page.dart';
import 'package:voicetypingapp/theme/theme_provider.dart';
import 'package:provider/provider.dart';

void main() async {
  runApp(ChangeNotifierProvider(
    create: (context) => ThemeProvider(),
    child: const MyApp(),
  ));
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Voice Typing App',
      debugShowCheckedModeBanner: false,
      home: HomePage(),
      theme: Provider.of<ThemeProvider>(context).themeData,
    );
  }
}
