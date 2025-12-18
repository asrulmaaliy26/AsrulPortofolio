#include <Arduino.h>
#include <IRrecv.h>
#include <IRremoteESP8266.h>
#include <IRutils.h>

// Ubah pin ini sesuai wiring kamu (abu-abu ke D2 -> GPIO4)
const uint16_t kRecvPin = 14;  // D2 pada ESP8266

IRrecv irrecv(kRecvPin);
decode_results results;

void setup() {
  Serial.begin(9600);  // baud rate sesuai Serial Monitor
  irrecv.enableIRIn();  // Start the receiver
  Serial.println("Tunggu sinyal dari remote AC...");
}

void loop() {
  if (irrecv.decode(&results)) {
    Serial.println(resultToHumanReadableBasic(&results));  // Human readable
    Serial.println(resultToSourceCode(&results));          // Bisa dipakai untuk replay

    Serial.print("Mesin waktu microseconds: ");
    Serial.println(results.value, HEX); // ini bisa jadi panjang dan kompleks

    Serial.println("Raw Data:");
    Serial.println(resultToTimingInfo(&results)); // Timing info buat replay
    Serial.println("=======================================");
    irrecv.resume();  // Continue receiving
  }
}
