import QtQml.Models
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Dialogs
import QtQuick.Layouts
import QtQuick.Window
import QtWebEngine

ApplicationWindow {
    id: mainWindow
    width: 700
    height: 700
    visible: true

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: mainInterface

        pushEnter: Transition {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: 50 }
            NumberAnimation { property: "scale"; from: 0.8; to: 1; duration: 50 }
        }
        pushExit: Transition {
            NumberAnimation { property: "opacity"; from: 1; to: 0; duration: 50 }
            NumberAnimation { property: "scale"; from: 1; to: 0.8; duration: 50 }
        }
    }

    Component {
        id: mainInterface
        Item {
            Image {
                id: backgroundMilkyWayImage
                source: "../resources/pictures/MilkyWay.png"
                anchors.fill: parent
                anchors.centerIn: parent
                scale: Qt.KeepAspectRatio
                transformOrigin: Item.Center
            }

            Text {
                id: title
                text: "Exosky App"
                color: "White"
                font.bold: true
                font.pixelSize: 20
                anchors.top: parent.top
                anchors.horizontalCenter: parent.horizontalCenter
            }
            
            Button {
                id: button
                text: "Let's explore!"
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onClicked: {
                    stackView.push(constellationInterface)
                }
            }
        }
    }

    Component {
        id: constellationInterface
        Item {
            Image {
                id: backgroundStarImage
                source: "../resources/pictures/universe_evolutionary.png"
                anchors.fill: parent
                anchors.centerIn: parent
                scale: Qt.KeepAspectRatio
                transformOrigin: Item.Center
            }

            ColumnLayout {
                anchors.centerIn: parent

                Rectangle {
                    id: constellationIntroduction
                    color: "#64000000"
                    width: 700
                    height: 80
                    Layout.alignment: Qt.AlignHCenter


                    Text {
                        id: constellationText
                        text: "Thousands of years ago, our ancestors looked up the nightsky and studied stars. " +
                              "Their locations are observed and drawn, creating a map of stars and forming constellations. " +
                              "How are constellations depicted in our galaxy, the Milky Way?"
                        color: "white"
                        font.pixelSize: 16
                        anchors.centerIn: parent
                        width: parent.width
                        height: parent.height
                        wrapMode: Text.WordWrap
                    }
                }

                Button {
                    id: overlayConstellationButton
                    text: "See constellation."
                    Layout.alignment: Qt.AlignHCenter
                    onClicked: {
                        constellationImage.visible = !constellationImage.visible
                    }
                }

                Item {
                    Layout.alignment: Qt.AlignHCenter
                    width: 700
                    height: 350

                    Image {
                        id: starMapImage
                        source: "../resources/pictures/star_map.png"
                        fillMode: Image.PreserveAspectFit
                        anchors.fill: parent
                    }

                    Image {
                        id: constellationImage
                        source: "../resources/pictures/constellation_star_map.png"
                        fillMode: Image.PreserveAspectFit
                        anchors.fill: parent
                        visible: false
                    }
                }
            }
            

            Button {
                id: backMainButton
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(mainInterface)
                }
            }

            Button {
                id: continueExoButton
                text: "Continue"
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                onClicked: {
                    stackView.push(introduceExoplanetInterface)
                }
            }
        }
    }

    Component {
        id: introduceExoplanetInterface
        Item {
            Image {
                id: k218bImage
                source: "../resources/pictures/k2-18b_.png"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 20

                Rectangle {
                    id: constellationIntroduction
                    color: "#50000000"
                    width: 700
                    height: 150
                    Layout.alignment: Qt.AlignHCenter


                    Text {
                        id: constellationText
                        text: "Those constellations are from Earth's point of view. " +
                              "\nFrom observations, scientists can pinpoint the exact location of an astronomical object, using concepts such as Right Ascension (RA), Declination (Dec), and Parallax as coordinates. " +
                              "\nImagine that we space-travel to an exoplanet. How would the location of stars change with respected to Earth? " +
                              "\nLet's explore the exoplanets originated from TOI-700, Trappist-1 and Ross 128 b."
                        color: "white"
                        font.pixelSize: 16
                        anchors.centerIn: parent
                        width: parent.width
                        height: parent.height
                        wrapMode: Text.WordWrap
                    }
                }

                Row {
                    spacing: 50
                    Button {
                        id: toi700Button
                        text: "View infos about TOI-700 d."
                        onClicked: {
                            stackView.push(toi700dInterface)
                        }
                    }

                    Button {
                        id: ross128bButton
                        text: "View infos about Ross 128 b."
                        onClicked: {
                            stackView.push(ross128bInterface)
                        }
                    }

                    Button {
                        id: trappist1eButton
                        text: "View infos about Trappist-1 e."
                        onClicked: {
                            stackView.push(trappist1eInterface)
                        }
                    }

                }
            }

            Button {
                id: backConstellationButton
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(constellationInterface)
                }
            }

            Button {
                id: continueEarthNightSkyButton
                text: "To the nightsky"
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                onClicked: {
                    stackView.push(nightSkyInterface)
                }
            }
        }
    }
    
    Component {
        id: toi700dInterface

        Item {
            Image {
                id: toi700dImage
                source: "../resources/pictures/toi-700d_location_edit_1.png"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            Rectangle {
                id: toi700dOverview
                color: "#64000000"
                width: 250
                height: 180
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                Text {
                    id: toi700dText
                    text: "Location: 101.4 light-years away from Earth. " +
                          "\nConstellation: Dorado." +
                          "\nStar system: red dwarf TOI-700. " +
                          "\nRight ascension: 06h28m22.97s. " +
                          "\nDeclination: -65d34m43.01s. " +
                          "\nOrbital period: 37 Earth days at 0.163 AU to its host star. "
                    color: "white"
                    font.pixelSize: 16
                    anchors.centerIn: parent
                    width: parent.width
                    height: parent.height
                    wrapMode: Text.WordWrap
                }
            }

            Button {
                id: backExoConsteButton
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(introduceExoplanetInterface)
                }
            }
        }
    }

    Component {
        id: ross128bInterface

        Item {
            Image {
                id: ross128bImage
                source: "../resources/pictures/ross-128b_location_edit_1.png"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            Rectangle {
                id: ross128bOverview
                color: "#64000000"
                width: 250
                height: 180
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                Text {
                    id: ross128bText
                    text: "Location: 11 light-years away from Earth. " +
                          "\nConstellation: Virgo." +
                          "\nStar system: red dwarf ROSS 128. " +
                          "\nRight ascension: 11h47m45.02s. " +
                          "\nDeclination: +00d47m57.44s. " +
                          "\nOrbital period: 9.9 Earth days at 0.0496 AU to its host star. "
                    color: "white"
                    font.pixelSize: 16
                    anchors.centerIn: parent
                    width: parent.width
                    height: parent.height
                    wrapMode: Text.WordWrap
                }
            }

            Button {
                id: backExoConsteButton1
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(introduceExoplanetInterface)
                }
            }
        }
    }

    Component {
        id: trappist1eInterface

        Item {
            Image {
                id: trappist1eImage
                source: "../resources/pictures/trappist-1e_location_edit_1.png"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            Rectangle {
                id: trappist1eOverview
                color: "#64000000"
                width: 290
                height: 210
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                Text {
                    id: trappist1eText
                    text: "Location: 39 light-years away from Earth. " +
                          "\nConstellation: Aquarius." +
                          "\nStar system: ultracool dwarf star TRAPPIST-1 contains 7 potential Earth-sized exoplanets. " +
                          "\nRight ascension: 06h28m22.97s. " +
                          "\nDeclination: -65d34m43.01s. " +
                          "\nOrbital period: 6.1 Earth days at 0.029 AU to its host star. "
                    color: "white"
                    font.pixelSize: 16
                    anchors.centerIn: parent
                    width: parent.width
                    height: parent.height
                    wrapMode: Text.WordWrap
                }
            }

            Button {
                id: backExoConsteButton2
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(introduceExoplanetInterface)
                }
            }
        }
    }
    Component {
        id: nightSkyInterface

        Item {

            Image {
                id: artisticViewImage
                source: "../resources/pictures/ross_128b_artistic_simulation.png"
                anchors.fill: parent
                fillMode: Image.PreserveAspectCrop
            }

            Label {
                id: mainNightSkyLabelnoTrans
                text: "Night Sky without Coordinate Transformation & brightness perspective adjustment"
                color: "#000080"
                font.bold: true
                font.pixelSize: 17
                anchors.top: parent.top
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 10
            }

            Row {
                id: rowselectPlanet
                anchors.top: mainNightSkyLabelnoTrans.bottom
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 10
                spacing: 10

                Label {
                    id: viewStarLabel
                    text: qsTr("View stars from")
                    color: "#000080"
                    font.bold: true
                    font.pixelSize: 15
                }

                ComboBox {
                    id: comboBoxSelectPlanets
                    model: ["TOI-700 d", "Ross 128 b", "TRAPPIST-1 e"]
                    width: 150
                    height: 40
                    Layout.fillWidth: true
                }

                CheckBox {
                    id: checkBoxfromEarthPOV
                    text: qsTr("View from Earth POV instead?")
                    checked: false
                }
            }

            Label {
                id: labelStarData
                anchors.top: rowselectPlanet.bottom
                anchors.topMargin: 0
                anchors.left: parent.left
                anchors.leftMargin: 10
                text: qsTr("With")
                font.pixelSize: 15
                font.bold: true
                color: "#000080"
            }

            Row {
                id: rowInputStarData
                anchors.top: labelStarData.bottom
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 10
                spacing: 20

                Column {
                    Label {
                        id: fovLabel
                        text: qsTr("FOV")
                        font.pixelSize: 15
                        color: "white"
                    }
                    TextField {
                        id: fovTextField
                        placeholderText: qsTr("..in degree")
                        height: 40
                        selectByMouse: true
                        text: "30"
                        validator: DoubleValidator {
                            bottom: 0
                        }
                    }
                }
                Column {
                    Label {
                        id: starSizeLabel
                        text: qsTr("Star size")
                        font.pixelSize: 15
                        color: "white"
                    }
                    TextField {
                        id: starSizeTextField
                        placeholderText: qsTr("..in pixel")
                        height: 40
                        selectByMouse: true
                        text: "200"
                        validator: IntValidator {
                            bottom: 0
                        }
                    }
                }
                Column {
                    Label {
                        id: starMagLabel
                        text: qsTr("Star Magnitude Limit")
                        font.pixelSize: 15
                        color: "white"
                    }
                    TextField {
                        id: starMagTextField
                        placeholderText: qsTr("..in pixel")
                        height: 40
                        selectByMouse: true
                        text: "10"
                        validator: IntValidator {
                            bottom: 0
                        }
                    }
                }
                Button {
                    id: viewNightSky
                    text: qsTr("View Nightsky!")
                    Layout.fillWidth: false

                    onClicked: {
                        var select_exoplanet = {
                            "planet": comboBoxSelectPlanets.currentText,
                            "checked_earth_pov": checkBoxfromEarthPOV.checked,
                        };
                        var star_chart = {
                            "star_size": parseFloat(starSizeTextField.text),
                            "magnitude_limit": parseFloat(starMagTextField.text),
                            "fov": parseFloat(fovTextField.text),
                        };
                        earthnightsky.create_star_chart(select_exoplanet, star_chart);
                    }
                }
            }

            Connections {
                target: earthnightsky

                function onUpdate_earth_nightsky() {
                    starsfromEarth.reload();
                }
            }

            Image {
                id: starsfromEarth
                anchors.top: rowInputStarData.bottom
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 90
                width: 500
                height: 500
                property real zoom: 0.0
                property real zoomStep: 0.1
                asynchronous: false
                smooth: true
                antialiasing: true
                mipmap: true
                transformOrigin: Item.Center

                function reload() {
                    source = "";
                    Qt.callLater(() => {
                        source = "image://provider/";
                    });
                }
            }

            Button {
                id: backExoConsteButton3
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(introduceExoplanetInterface)
                }
            }

            Button {
                id: forwardThreedViewButton
                text: "3D View"
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                onClicked: {
                    stackView.push(threedViewInterface)
                }
            }
        }
    }
    Component {
        id: threedViewInterface

        Item {
            Image {
                id: backgroundStarImage
                source: "../resources/pictures/universe_evolutionary.png"
                anchors.fill: parent
                anchors.centerIn: parent
                scale: Qt.KeepAspectRatio
                transformOrigin: Item.Center
            }

            Label {
                id: mainNightSky3DLabel
                text: "3D Night Sky (processing time can be slow for higher number of stars and star size)"
                color: "white"
                font.bold: true
                font.pixelSize: 17
                anchors.top: parent.top
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 10
            }

            Row {
                id: rowselectexoplanet
                anchors.top: mainNightSky3DLabel.bottom
                anchors.topMargin: 10
                anchors.left: parent.left
                anchors.leftMargin: 10
                spacing: 20

                Column{
                    Label {
                        id: viewStarfromEarthLabel
                        text: qsTr("View stars from Earth to")
                        color: "white"
                        font.bold: true
                        font.pixelSize: 15
                    }
                    ComboBox {
                        id: comboBoxSelectExoplanets
                        model: ["TOI-700 d", "Ross 128 b", "TRAPPIST-1 e"]
                        width: 180
                        height: 40
                        Layout.fillWidth: true
                        background: Rectangle {
                            color: "white"
                        }
                    }
                }
                Column {
                    Label {
                        id: starSize3DLabel
                        text: qsTr("Star size")
                        font.pixelSize: 15
                        color: "white"
                    }

                    TextField {
                        id: starSize3DTextField
                        placeholderText: qsTr("..in pixel")
                        height: 40
                        selectByMouse: true
                        text: "100"
                        color: "white"
                        validator: IntValidator {
                            bottom: 0
                        }
                    }
                }
                Column {
                    Label {
                        id: numberofStars3DLabel
                        text: qsTr("Number of shown stars")
                        font.pixelSize: 15
                        color: "white"
                    }

                    TextField {
                        id: numberofStars3DTextField
                        placeholderText: qsTr("..int type, max 50000")
                        height: 40
                        selectByMouse: true
                        text: "5000"
                        color: "white"
                        validator: IntValidator {
                            bottom: 1
                            top: 49999
                        }
                        onTextChanged: {
                            if (parseInt(numberofStars3DTextField.text) > 49999) {
                                numberofStars3DTextField.text = "49999";
                            } else if (parseInt(numberofStars3DTextField.text) < 1) {
                                numberofStars3DTextField.text = "1";
                            }
                        }
                    }
                }
                CheckBox {
                    id: checkBoxShiftReference
                    text: qsTr("Shift Reference?")
                    checked: false
                }
                Button {
                    id: viewNightSky
                    text: qsTr("View Nightsky in 3D!")
                    Layout.fillWidth: false

                    onClicked: {
                        var select_exoplanet = {
                            "planet": comboBoxSelectExoplanets.currentText,
                            "checked_earth_pov": checkBoxShiftReference.checked,
                        };
                        var threed_star_chart = {
                            "number_of_stars": Math.floor(parseFloat(numberofStars3DTextField.text)),
                            "star_size_perspective": parseFloat(starSize3DTextField.text),
                        };
                        earthnightsky.create_threed_star_chart(select_exoplanet, threed_star_chart);
                    }
                }
            }
            WebEngineView {
                id: webEngineView
                width: 500
                height: 500
                anchors.top: rowselectexoplanet.bottom
                anchors.topMargin: 30
                anchors.left: parent.left
                anchors.leftMargin: 90
                transformOrigin: Item.Center
                settings.webGLEnabled: true
                settings.accelerated2dCanvasEnabled: true
                backgroundColor: "transparent"
            }

            Connections {
                target: earthnightsky
                function onThreed_nightsky_changed() {
                    webEngineView.loadHtml(`
                        <html>
                        <head>
                            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
                        </head>
                        <body style="margin: 0; padding: 0; overflow: hidden;">
                            <div id="plot" style="width: 100vw; height: 100vh;"></div>
                            <script>
                                var plotData = ${earthnightsky.get_threed_nightsky};
                                var layout = plotData.layout;
                                layout.margin = { l: 0, r: 0, t: 0, b: 0 };
                                Plotly.newPlot('plot', plotData.data, layout);
                            </script>
                        </body>
                        </html>
                    `);
                }
            }

            Button {
                id: backNightSkyButton
                text: "Back"
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                onClicked: {
                    stackView.push(nightSkyInterface)
                }
            }
        }
    }
}
