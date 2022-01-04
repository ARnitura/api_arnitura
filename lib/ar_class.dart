import 'package:ar_flutter_plugin/ar_flutter_plugin.dart';
import 'package:ar_flutter_plugin/datatypes/config_planedetection.dart';
import 'package:ar_flutter_plugin/datatypes/node_types.dart';
import 'package:ar_flutter_plugin/datatypes/hittest_result_types.dart';
import 'package:ar_flutter_plugin/models/ar_node.dart';
import 'package:ar_flutter_plugin/models/ar_hittest_result.dart';
import 'package:vector_math/vector_math_64.dart';
import 'package:ar_flutter_plugin/managers/ar_location_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_session_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_object_manager.dart';
import 'package:ar_flutter_plugin/managers/ar_anchor_manager.dart';
import 'package:ar_flutter_plugin/models/ar_anchor.dart';
import 'package:flutter/material.dart';
import 'dart:developer';

class ArWidget extends StatefulWidget {
  ArWidget({Key? key}) : super(key: key);

  @override
  _ArWidgetState createState() => _ArWidgetState();
}

class _ArWidgetState extends State<ArWidget> {
  late ARSessionManager arSessionManager;
  late ARObjectManager arObjectManager;
  late ARAnchorManager arAnchorManager;

  var nodes = [];
  var anchors = [];

  @override
  void dispose() {
    super.dispose();
    arSessionManager.dispose();
  } // Метод при выходе из приложения

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: const Text('AR-экран'),
        ),
        body: Container(
            child: Stack(children: [
          ARView(
            onARViewCreated: onARViewCreated,
            planeDetectionConfig: PlaneDetectionConfig.horizontalAndVertical,
          ),
          Align(
            alignment: FractionalOffset.bottomCenter,
            child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton(
                      onPressed: onRemoveEverything,
                      child: const Text("Удалить модели")),
                ]),
          )
        ])));
  } // Виджет с частью дизайна

  void onARViewCreated(
      ARSessionManager arSessionManager,
      ARObjectManager arObjectManager,
      ARAnchorManager arAnchorManager,
      ARLocationManager arLocationManager) {
    this.arSessionManager = arSessionManager;
    this.arObjectManager = arObjectManager;
    this.arAnchorManager = arAnchorManager;
    // Определение переменных Сессии
    this.arSessionManager.onInitialize(
          showFeaturePoints: false,
          showPlanes: true,
          customPlaneTexturePath: "Images/triangle.png",
          showWorldOrigin: true,
          handlePans: true,
          handleRotation: true,
        );
    this.arObjectManager.onInitialize();
    // Инициализация
    this.arSessionManager.onPlaneOrPointTap = onPlaneOrPointTapped;
    this.arObjectManager.onPanStart = onPanStarted;
    this.arObjectManager.onPanChange = onPanChanged;
    this.arObjectManager.onPanEnd = onPanEnded;
    this.arObjectManager.onRotationStart = onRotationStarted;
    this.arObjectManager.onRotationChange = onRotationChanged;
    this.arObjectManager.onRotationEnd = onRotationEnded;
    // Назначение методов
  }

  Future<void> onRemoveEverything() async {
    for (var node in nodes) {
      arObjectManager.removeNode(node);
    }
    for (var anchor in anchors) {
      arAnchorManager.removeAnchor(anchor);
      log('delete');
    }
    anchors = [];
  }

  Future<void> onPlaneOrPointTapped(
      List<ARHitTestResult> hitTestResults) async {
    var singleHitTestResult = hitTestResults.firstWhere(
        (hitTestResult) => hitTestResult.type == ARHitTestResultType.plane);
    var newAnchor =
        ARPlaneAnchor(transformation: singleHitTestResult.worldTransform);
    ARNode newNode;
    await arAnchorManager.addAnchor(newAnchor).then((value) async {
      newNode = ARNode(
          type: NodeType.webGLB,
          uri: "https://apikreslo.herokuapp.com/",
          scale: Vector3(1, 1, 1),
          position: Vector3(0.0, 0.0, 0.0),
          rotation: Vector4(1.0, 0.0, 0.0, 0.0));
      await arObjectManager
          .addNode(newNode, planeAnchor: newAnchor)
          .then((value) => {nodes.add(newNode)});
    });
  }

  onPanStarted(String nodeName) {
    log("Started panning node " + nodeName);
  }

  onPanChanged(String nodeName) {
    log("Continued panning node " + nodeName);
  }

  onPanEnded(String nodeName, Matrix4 newTransform) {
    log("Ended panning node " + nodeName);
    // final pannedNode =
    //     this.nodes.firstWhere((element) => element.name == nodeName); // Отредоктированная нода

    /*
    * Uncomment the following command if you want to keep the transformations of the Flutter representations of the nodes up to date
    * (e.g. if you intend to share the nodes through the cloud)
    */
    //pannedNode.transform = newTransform;
  }

  onRotationStarted(String nodeName) {
    log("Started rotating node " + nodeName);
  }

  onRotationChanged(String nodeName) {
    print("Continued rotating node " + nodeName);
  }

  onRotationEnded(String nodeName, Matrix4 newTransform) {
    log("Ended rotating node " + nodeName);
    // final rotatedNode =
    //     this.nodes.firstWhere((element) => element.name == nodeName); // Повернутая нода

    /*
    * Uncomment the following command if you want to keep the transformations of the Flutter representations of the nodes up to date
    * (e.g. if you intend to share the nodes through the cloud)
    */
    //rotatedNode.transform = newTransform;
  }
}
