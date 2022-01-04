import 'package:flutter/material.dart';
import 'package:sentry_flutter/sentry_flutter.dart';
import 'first_screen.dart';

Future<void> main() async {
  await SentryFlutter.init(
    (options) {
      options.dsn =
          'https://c8c4539554e84fefb9819c2a44c31074@o402412.ingest.sentry.io/6132266';
      options.tracesSampleRate = 1.0;
    },
    appRunner: () => runApp(const MyApp()),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(home: (FScreen()));
  }
}
