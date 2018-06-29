// Load WiFi library.
#include <ESP8266WiFi.h>

// Replace with your network credentials.
const char* ssid     = "<Your Wifi network>";
const char* password = "<Your Wifi password>";

// Open up a web server at port 80.
WiFiServer server(80);

// Pin numbers for motor.
const int PUL = 14;  // D5
const int DIR = 4;  // D2
const int ENA = 15;  // D8

// Variable to store the HTTP request.
String header;

// Number of rotations.
int rotations = 0;

void setup() {
  // Connect to Wi-Fi network with SSID and password
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  /*
  // Print local IP address and start web server. You can uncomment this to
  // determine the IP address of the microcontroller.
  Serial.begin(9600);
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  */

  // Set the pins.
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(ENA, OUTPUT);
  digitalWrite(ENA, HIGH);

  // Start the server.
  server.begin();
}

void MaybeRunMotor() {
  if (rotations != 0) {
    digitalWrite(ENA,LOW);
    if (rotations < 0) {
      digitalWrite(DIR, HIGH);
      rotations *= -1;
    } else {
      digitalWrite(DIR, LOW);
    }
    // Driver configuration: 110110.
    for (int i = 0; i < rotations; ++i) {
      digitalWrite(PUL, HIGH);
      delayMicroseconds(500);
      digitalWrite(PUL, LOW);
      delayMicroseconds(500);
      // Reset the watch dog timer in case of long rotations.
      ESP.wdtFeed();
    }
    rotations = 0;
    delayMicroseconds(1000);
    digitalWrite(ENA, HIGH);
  }
}

void loop(){
  WiFiClient client = server.available();

  if (client) {
    String currentLine = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        header += c;
        if (c == '\n') {
          if (currentLine.length() == 0) {
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println("Connection: close");
            client.println();

            if (header.indexOf("/left") > 0) {
              client.println("Motor-state: left");
              int leftIndex = header.indexOf("/left");
              int spaceIndex = header.indexOf(" ", leftIndex);
              if (spaceIndex > 0) {
                int steps = header.substring(leftIndex + 6, spaceIndex).toInt();
                rotations = steps;
              } else {
                rotations = 800;
              }
            } else if (header.indexOf("/right") > 0) {
              client.println("Motor-state: right");
              int rightIndex = header.indexOf("/right");
              int spaceIndex = header.indexOf(" ", rightIndex);
              if (spaceIndex > 0) {
                int steps = header.substring(rightIndex + 7, spaceIndex).toInt();
                rotations = -steps;
              } else {
                rotations = -800;
              }
            } else if (header.indexOf("/off") > 0) {
              client.println("Motor-state: off");
              rotations = 0;
            } else if (header.indexOf("/enahigh") > 0) {
              digitalWrite(ENA, HIGH);
              client.println("Ena: HIGH");
            } else if (header.indexOf("/enalow") > 0) {
              digitalWrite(ENA, LOW);
              client.println("Ena: LOW");
            }

            client.println();
            break;
          } else {
            currentLine = "";
          }
        } else if (c != '\r') {
          currentLine += c;
        }
      }
    }
    header = "";
    client.stop();
  }
  MaybeRunMotor();
}
