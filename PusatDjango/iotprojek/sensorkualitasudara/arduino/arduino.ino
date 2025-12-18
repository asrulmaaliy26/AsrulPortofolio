// please check the video
// https://www.youtube.com/watch?v=xj-j5zgZnoo

#include <ESP8266WebServer.h>
#include <ESP8266mDNS.h>
#include <IRsend.h>
const char* ssid = "TP-Link_0260";
const char* password = "AHDA12345";

MDNSResponder mdns;

String Domain = "home";
String switch1name = "Light";
String switch1 = "OFF";
String Fan = "OFF";
String AC = "OFF";
int currentTemp = 24; // Suhu awal (ubah sesuai kebutuhan)

ESP8266WebServer server(80);

IRsend irsend(D4);

void handleRoot() {
 server.send(200, "text/html", 
"<!DOCTYPE html>" \
"<html>" \
"<head>" \
"<title>home</title>" \
"</head>" \
"<body>" \
"<h1>Home Automation</h1>" \
"<h2>"+ switch1name +": "+ switch1 +"</h2>" \
"<p><a href=\"/Switch1OFF\"><button class=\"button\">OFF</button></a><a href=\"/Switch1ON\"><button class=\"button\">ON</button></a></p>" \
"<h2>Fan: "+ Fan +"</h2>" \
"<p><a href=\"/FanOFF\"><button class=\"button\">OFF</button></a><a href=\"/FanSpeed1\"><button class=\"button\">Speed1</button></a><a href=\"/FanSpeed2\"><button class=\"button\">Speed2</button></a><a href=\"/FanSpeed3\"><button class=\"button\">Speed3</button></a><a href=\"/FanSpeed4\"><button class=\"button\">Speed4</button></a></p>" \
"<h2>Ac: "+ AC +"</h2>" \
"<p><a href=\"/AcOFF\"><button class=\"button\">OFF</button></a><a href=\"/AcON\"><button class=\"button\">ON</button></a></p>" \
"<p>Suhu: " + String(currentTemp) + "°C</p>" \
"<p><a href=\"/TempDown\"><button class=\"button\">-</button></a><a href=\"/TempUp\"><button class=\"button\">+</button></a></p>" \
"</body>" \
"</html>" \
);
}

void switch1ON(){
  switch1 = "ON";
  digitalWrite(D1, LOW);
  handleRoot();
}

void switch1OFF(){
  switch1 = "OFF";
  digitalWrite(D1, HIGH);
  handleRoot();
}

void FanOFF(){
  Fan = "OFF";
  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  handleRoot();
}

void FanSpeed1(){
  Fan = "Speed1";
  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  delay(500);
  digitalWrite(D5, LOW);
  handleRoot();
}

void FanSpeed2(){
  Fan = "Speed2";
  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  delay(500);
  digitalWrite(D6, LOW);
  handleRoot();
}

void FanSpeed3(){
  Fan = "Speed3";
  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  delay(500);
  digitalWrite(D5, LOW);
  digitalWrite(D6, LOW);
  handleRoot();
}

void FanSpeed4(){
  Fan = "Speed4";
  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  delay(500);
  digitalWrite(D7, LOW);
  handleRoot();
}

void AcON(){
  AC = "ON";
  irsend.sendNEC(142607175, 28);
  handleRoot();
}

void AcOFF(){
  AC = "OFF";
  irsend.sendNEC(143392849, 28);
  handleRoot();
}

void sendAcTemp(int temp) {
  // Contoh pakai suhu 24-30, sesuaikan kode IR berikut dengan remot AC kamu
  switch (temp) {
    case 24:
      irsend.sendNEC(142607175, 28);
      break;
    case 25:
      irsend.sendNEC(142639935, 28);
      break;
    case 26:
      irsend.sendNEC(142672695, 28);
      break;
    case 27:
      irsend.sendNEC(142705455, 28);
      break;
    case 28:
      irsend.sendNEC(142738215, 28);
      break;
    case 29:
      irsend.sendNEC(142770975, 28);
      break;
    case 30:
      irsend.sendNEC(142803735, 28);
      break;
    default:
      irsend.sendNEC(142607175, 28); // default ke 24
      break;
  }
}

void TempUp() {
  if (currentTemp < 30) currentTemp++;
  sendAcTemp(currentTemp);
  AC = "ON (" + String(currentTemp) + "°C)";
  handleRoot();
}

void TempDown() {
  if (currentTemp > 24) currentTemp--;
  sendAcTemp(currentTemp);
  AC = "ON (" + String(currentTemp) + "°C)";
  handleRoot();
}



void setup(void){
  pinMode(D1, OUTPUT);
  pinMode(D4, OUTPUT);
  pinMode(D5, OUTPUT);
  pinMode(D6, OUTPUT);
  pinMode(D7, OUTPUT);
  digitalWrite(D1, HIGH);
  digitalWrite(D4, HIGH);
  digitalWrite(D5, HIGH);
  digitalWrite(D6, HIGH);
  digitalWrite(D7, HIGH);
  
  Serial.begin(115200);
  
  WiFi.begin(ssid, password);
  Serial.println("");

  while (WiFi.status() != WL_CONNECTED) {
    delay(200);
    digitalWrite(D4, HIGH);
    delay(200);
    digitalWrite(D4, LOW);
    Serial.print(".");
  }

  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP()); 

  if(mdns.begin(Domain)){
    Serial.println("MDNS Started: " + Domain + ".local/");
  }
 
  server.on("/", handleRoot);   
  server.on("/Switch1ON", switch1ON);  
  server.on("/Switch1OFF", switch1OFF);      
  server.on("/FanOFF", FanOFF); 
  server.on("/FanSpeed1", FanSpeed1);   
  server.on("/FanSpeed2", FanSpeed2);
  server.on("/FanSpeed3", FanSpeed3);
  server.on("/FanSpeed4", FanSpeed4);  
  server.on("/AcON", AcON);  
  server.on("/AcOFF", AcOFF);     
  server.on("/TempUp", TempUp);
  server.on("/TempDown", TempDown);

  server.begin();                 
  Serial.println("HTTP server started");
  digitalWrite(D4, LOW);
}

void loop(void){
  mdns.update();
  server.handleClient();  
}