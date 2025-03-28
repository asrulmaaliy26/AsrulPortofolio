#include <ESP8266WiFi.h>
#include <MQ135.h>
#include <DHT.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// **Konfigurasi OLED**
#define OLED_WIDTH 128
#define OLED_HEIGHT 64
#define OLED_ADDR 0x3C

// **Pin Sensor**
#define PIN_MQ135 A0
#define DHTPIN D4
#define DHTTYPE DHT11

// **Konfigurasi WiFi**
// const char* ssid = "Wifigratis";
// const char* password = "12345678";
// const char* server = "192.168.226.179"; // IP server lokal
// const int serverPort = 3000;

const char* ssid = "TOTOLINK";
const char* password = "AHDA12345";
const char* server = "192.168.0.111"; // IP server lokal
const int serverPort = 3000;

WiFiClient client;
MQ135 mq135_sensor(PIN_MQ135);
DHT dht(DHTPIN, DHTTYPE);
Adafruit_SSD1306 display(OLED_WIDTH, OLED_HEIGHT);

float temp, humi, ppm;
float tempout, humiout, tempac;
int modeac;
int randomValue = 0;
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
  humi = dht.readHumidity();
  temp = dht.readTemperature();
  ppm = mq135_sensor.getPPM();

  tempout = random(20, 35);
  humiout = random(40, 80);
  tempac = random(16, 30);
  modeac = random(0, 3);

  // **Cek validitas data sensor**
  if (isnan(humi) || isnan(temp)) {
    Serial.println("Gagal membaca DHT!");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Gagal baca DHT!");
    display.display();
    return;
  }

  Serial.print("PPM: "); Serial.print(ppm);
  Serial.print(" | Temp: "); Serial.print(temp);
  Serial.print(" | Hum: "); Serial.println(humi);

  Serial.print(" | TempOut: "); Serial.print(tempout);
  Serial.print(" | HumiOut: "); Serial.print(humiout);
  Serial.print(" | TempAC: "); Serial.print(tempac);
  Serial.print(" | ModeAC: "); Serial.println(modeac);
}

// **Fungsi memperbarui OLED**
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

  display.setCursor(0, 30);
  display.print("Out T: "); display.print(tempout);
  display.println(" C");

  display.setCursor(0, 40);
  display.print("Out H: "); display.print(humiout);
  display.println(" %");

  display.setCursor(0, 50);
  display.print("AC T: "); display.print(tempac);
  display.print("C M:"); display.print(modeac);

  display.setCursor(0, 56);
  display.print("Rand: ");
  display.print(randomValue);  // Menampilkan nilai random dari server

  display.display();
}

// **Fungsi mengirim data ke server**
void kirimData() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi terputus! Mencoba koneksi ulang...");
    WiFi.reconnect();
    return;
  }

  Serial.println("Mengirim data ke server...");
  if (client.connect(server, serverPort)) {
    String postData = "ppm=" + String(ppm) + "&temp=" + String(temp) + "&humi=" + String(humi) + 
                      "&tempout=" + String(tempout) + "&humiout=" + String(humiout) + 
                      "&tempac=" + String(tempac) + "&modeac=" + String(modeac);

    client.println("POST /iot/sensorsmartac/api/receive/ HTTP/1.1");
    client.println("Host: " + String(server));
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.println(postData);

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
  int pos = response.indexOf("\"nilai_random\":");
  if (pos != -1) {
    int start = pos + 15;
    int end = response.indexOf("}", start);
    if (end == -1) end = response.length();
    String randomStr = response.substring(start, end);
    randomValue = randomStr.toInt();  // Konversi ke integer
  } else {
    Serial.println("Nilai random tidak ditemukan dalam respons!");
  }

  Serial.print("Nilai Random dari server: ");
  Serial.println(randomValue);
}
