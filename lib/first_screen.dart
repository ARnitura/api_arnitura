import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:loading/indicator/ball_spin_fade_loader_indicator.dart';
import 'package:loading/loading.dart';
import 'dart:async';
import 'ar_class.dart';

class FScreen extends StatefulWidget {
  const FScreen({Key? key}) : super(key: key);

  @override
  _FScreenState createState() => _FScreenState();
}

class _FScreenState extends State<FScreen> {
  @override
  void initState() {
    super.initState();
    Timer(const Duration(seconds: 2), () {
      setState(() {
        Navigator.pushReplacement(
            context, MaterialPageRoute(builder: (context) => ArWidget()));
      });
    });
  } // Пока пользователь видит экран загрузки мы загружаем все что нужно

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
            const SizedBox(
              height: 250,
            ),
            Loading(
              indicator: BallSpinFadeLoaderIndicator(),
              size: 50,
              color: Color(0xFF4094D0),
            )
          ],
        ),
      ),
    ));
  }
}
