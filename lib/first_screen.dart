import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class FScreen extends StatefulWidget {
  const FScreen({Key? key}) : super(key: key);

  @override
  _FScreenState createState() => _FScreenState();
}

class _FScreenState extends State<FScreen> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Image.asset('assets/image/logo.png', width: 200),
            const SizedBox(width: 10, height: 10),
            const Text(
              'v2.0',
              style: TextStyle(color: Color(0xFFC4C4C4), fontSize: 20.8),
            ),
            CupertinoActivityIndicator(radius: 10)
          ],
        ),
      ),
    ));
  }
}
