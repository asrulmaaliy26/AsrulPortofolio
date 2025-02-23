#include <ESP8266WiFi.h>
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

// Konfigurasi WiFi
const char* ssid = "Wifigratis";
const char* password = "12345678";
const char* server = "192.168.70.179"; // IP server lokal

WiFiClient client;
MQ135 mq135_sensor(PIN_MQ135);
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT);

// Variabel Sensor
float temp, humi, ppm;
unsigned long lastUpdate = 0;
const long updateInterval = 5000; // Update setiap 5 detik

void setup() {
  // Inisialisasi OLED
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    while (true); // Jika OLED gagal, berhenti di sini
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
  }

  // Tampilkan IP Address di OLED
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("WiFi Terhubung!");
  display.print("IP: ");
  display.println(WiFi.localIP());
  display.display();
  delay(2000);

  dht.begin();
}

void loop() {
  if (millis() - lastUpdate >= updateInterval) {
    humi = dht.readHumidity();
    temp = dht.readTemperature();
    ppm = mq135_sensor.getPPM();

    // Cek apakah data valid
    if (isnan(humi) || isnan(temp)) {
      display.clearDisplay();
      display.setCursor(0, 0);
      display.println("Gagal baca DHT!");
      display.display();
      return;
    }

    // Update OLED Display
    updateDisplay();

    // Kirim data ke server
    if (client.connect(server, 3000)) {
      String postData = "ppm=" + String(ppm) + "&temp=" + String(temp) + "&humi=" + String(humi);

      client.println("POST /server.php HTTP/1.1");
      client.println("Host: " + String(server));
      client.println("Content-Type: application/x-www-form-urlencoded");
      client.print("Content-Length: ");
      client.println(postData.length());
      client.println();
      client.println(postData);

      display.setCursor(0, 56);
      display.println("Data Terkirim!");
      display.display();
    } else {
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
