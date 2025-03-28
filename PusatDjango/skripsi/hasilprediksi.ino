#include <ESP8266WiFi.h>
#include <MQ135.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <ArduinoJson.h>  // Gunakan library JSON untuk memformat data dengan benar

// **Konfigurasi OLED**
#define OLED_WIDTH 128
#define OLED_HEIGHT 64
#define OLED_ADDR 0x3C

// **Pin Sensor**
#define PIN_MQ135 A0
#define DHTPIN D4
#define DHTTYPE DHT11

// **Konfigurasi WiFi**
const char* ssid = "TOTOLINK";
const char* password = "AHDA12345";
const char* server = "192.168.0.111";  // IP server Django
const int serverPort = 3000;  // Pastikan port sesuai dengan Django

WiFiClient client;
MQ135 mq135_sensor(PIN_MQ135);
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT);

float tempout, humiout, tempac;
int modeac;
int hasil_prediksi = 0;
unsigned long lastUpdate = 0;
const long updateInterval = 10000; // Update setiap 10 detik

void setup() {
  Serial.begin(115200);

  // **Inisialisasi OLED**
  if (!display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("OLED gagal diinisialisasi!");
    while (true);
  }

  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Menghubungkan WiFi...");
  display.display();

  // **Koneksi WiFi**
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Menghubungkan ke WiFi...");
  }

  // **Tampilkan IP Address di OLED**
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
    bacaSensor();
    updateDisplay();
    kirimData();
    lastUpdate = millis();
  }
}

// **Fungsi membaca sensor**
void bacaSensor() {
  humiout = dht.readHumidity();
  tempout = dht.readTemperature();
  tempac = random(16, 30);
  modeac = random(0, 3);

  // **Cek validitas data sensor**
  if (isnan(humiout) || isnan(tempout)) {
    Serial.println("Gagal membaca DHT!");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Gagal baca DHT!");
    display.display();
    return;
  }

  Serial.print("TempOut: "); Serial.print(tempout);
  Serial.print(" | HumiOut: "); Serial.print(humiout);
  Serial.print(" | TempAC: "); Serial.print(tempac);
  Serial.print(" | ModeAC: "); Serial.println(modeac);
}

// **Fungsi memperbarui OLED**
void updateDisplay() {
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);

  display.setCursor(0, 10);
  display.print("Out T: "); display.print(tempout);
  display.println(" C");

  display.setCursor(0, 20);
  display.print("Out H: "); display.print(humiout);
  display.println(" %");

  display.setCursor(0, 30);
  display.print("AC T: "); display.print(tempac);
  display.println(" C");  

  display.setCursor(0, 40);
  display.print("Mode AC: "); display.print(modeac);

  display.setCursor(0, 50);
  display.print("Hasil Pred: ");
  display.print(hasil_prediksi);

  display.display();
}

// **Fungsi mengirim data ke server dalam format JSON**
void kirimData() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi terputus! Mencoba koneksi ulang...");
    WiFi.reconnect();
    return;
  }

  Serial.println("Mengirim data ke server...");
  if (client.connect(server, serverPort)) {
    // **Buat JSON data**
    StaticJsonDocument<200> jsonDoc;
    jsonDoc["tempout"] = tempout;
    jsonDoc["humiout"] = humiout;
    jsonDoc["tempac"] = tempac;
    jsonDoc["modeac"] = modeac;
    
    String jsonString;
    serializeJson(jsonDoc, jsonString);

    // **Kirim permintaan HTTP POST**
    client.println("POST /skripsi/api/receive_data_ac/ HTTP/1.1");
    client.println("Host: " + String(server));
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(jsonString.length());
    client.println();
    client.println(jsonString);

    // Tunggu respons dari server
    delay(500);
    String response = "";
    while (client.available()) {
      char c = client.read();
      response += c;
    }
    Serial.println("Response dari server: " + response);

    // **Tampilkan "Data Terkirim!" di OLED**
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 56);
    display.println("Data Terkirim!");
    display.display();

    // Tunggu 2 detik sebelum mengganti dengan nilai random
    delay(2000);

    // **Panggil fungsi untuk mengekstrak nilai random**
    terimaNilaiRandom(response);

    // **Tampilkan nilai random setelah 2 detik**
    updateDisplay();

  } else {
    Serial.println("Gagal terhubung ke server!");
    display.setCursor(0, 56);
    display.println("Gagal Koneksi!");
    display.display();
  }

  client.stop();
}

// **Fungsi untuk mengekstrak nilai random dari respons JSON**
void terimaNilaiRandom(String response) {
  StaticJsonDocument<200> doc;
  DeserializationError error = deserializeJson(doc, response);

  if (error) {
    Serial.print("Gagal parsing JSON: ");
    Serial.println(error.f_str());
    return;
  }

  if (doc.containsKey("hasil_prediksi")) {
    hasil_prediksi = doc["hasil_prediksi"];
    Serial.print("Hasil Prediksi dari server: ");
    Serial.println(hasil_prediksi);
  } else {
    Serial.println("Key 'hasil_prediksi' tidak ditemukan dalam respons!");
  }
}

