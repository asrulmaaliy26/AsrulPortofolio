#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>  // Untuk HTTPS
#include <MQ135.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Konfigurasi OLED
#define OLED_WIDTH 128
#define OLED_HEIGHT 64
#define OLED_ADDR 0x3C

// Pin Sensor
#define PIN_MQ135 A0
#define DHTPIN D4
#define DHTTYPE DHT11

// Konfigurasi WiFi dan Server
const char* ssid = "Wifigratis";
const char* password = "12345678";
const char* server = "asrul.pythonanywhere.com"; // Server API
const int httpsPort = 443;

WiFiClientSecure client;  // HTTPS client
MQ135 mq135_sensor(PIN_MQ135);
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT);

// Variabel Sensor
float temp, humi, ppm;
unsigned long lastUpdate = 0;
const long updateInterval = 5000; // Update setiap 5 detik

void setup() {
  Serial.begin(115200);
  
  // Inisialisasi OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("Gagal inisialisasi OLED!");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Menghubungkan WiFi...");
  display.display();

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  
  Serial.println("\nWiFi Terhubung!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Tampilkan IP Address di OLED
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("WiFi Terhubung!");
  display.print("IP: ");
  display.println(WiFi.localIP());
  display.display();
  delay(2000);

  dht.begin();
  
  // Menonaktifkan verifikasi sertifikat (tidak aman, tapi diperlukan untuk ESP8266)
  client.setInsecure();
}

void loop() {
  if (millis() - lastUpdate >= updateInterval) {
    humi = dht.readHumidity();
    temp = dht.readTemperature();
    ppm = mq135_sensor.getPPM();

    // Cek apakah data valid
    if (isnan(humi) || isnan(temp)) {
      Serial.println("Gagal membaca DHT!");
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("Gagal baca DHT!");
      display.display();
      return;
    }

    // Update OLED Display
    updateDisplay();

    // Kirim data ke server
    Serial.println("Menghubungkan ke server...");
    if (client.connect(server, httpsPort)) {
      Serial.println("Terhubung ke server!");

      // Format data untuk dikirim
      String postData = "ppm=" + String(ppm) + "&temp=" + String(temp) + "&humi=" + String(humi);
      
      // Kirim HTTP Request
      client.println("POST /api/receive/ HTTP/1.1");
      client.println("Host: " + String(server));
      client.println("User-Agent: ESP8266");
      client.println("Content-Type: application/x-www-form-urlencoded");
      client.print("Content-Length: ");
      client.println(postData.length());
      client.println();
      client.println(postData);

      // Tunggu respons server
      Serial.println("Menunggu respons server...");
      while (client.connected() && !client.available()) delay(100);

      while (client.available()) {
        String response = client.readString();
        Serial.println("Respons Server: ");
        Serial.println(response);
      }

      display.setCursor(0, 56);
      display.println("Data Terkirim!");
      display.display();
    } else {
      Serial.println("Gagal menghubungi server!");
      display.setCursor(0, 56);
      display.println("Gagal Koneksi!");
      display.display();
    }

    client.stop();
    lastUpdate = millis();
  }
}

// Fungsi untuk memperbarui tampilan OLED
void updateDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  
  display.setCursor(0, 0);
  display.print("PPM : ");
  display.print(ppm);
  display.println(" PPM");

  display.setCursor(0, 20);
  display.print("Temp: ");
  display.print(temp);
  display.println(" C");

  display.setCursor(0, 40);
  display.print("Hum : ");
  display.print(humi);
  display.println(" %");

  display.display();
}
