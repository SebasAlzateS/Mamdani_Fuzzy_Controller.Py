#include "TM1637Display.h"
#define triac 5
TM1637Display displayseg(8,9);
#include <OneWire.h>
#include <DallasTemperature.h>

int P;
int numero;
char aux;
String ang_min;
int angulo,ang_salida=100;
int enviado;
unsigned long Tiempo_previo = 0; 
unsigned long Tiempo_actual = 0;
int Read_Delay = 1000;     // Periodo de muestreo en milisegundos
int Temperatura = 0;       // Celsius
OneWire oneWireObjeto(10);
DallasTemperature sensorDS18B20(&oneWireObjeto);

// display 
const uint8_t celsius[] = {
  SEG_A | SEG_B | SEG_G | SEG_F, // cero volado
  SEG_A | SEG_F | SEG_E | SEG_D // C
};
void setup() {
  Serial.begin(115200);
  pinMode(2, INPUT); //entrada Cruce por cero
  digitalWrite(2, HIGH); // pull up
  pinMode(triac, OUTPUT); //salida controlar angulo o fase PWM
  Serial.setTimeout(50);
  displayseg.setBrightness(7,true);
  displayseg.clear();
  
}

void loop() {
   attachInterrupt(0, Fase, RISING); //interrupcion se llama la funcion 
   Tiempo_actual = millis(); // Tiempo Actual    
   if(Serial.available()>0)
    {
      enviado = Serial.parseInt();
      //ang_min= Serial.readString();
      //angulo= ang_min.toInt();
      ang_salida=map(enviado,0,180,0,100);
    }
   if(Tiempo_actual - Tiempo_previo >= Read_Delay){
       Tiempo_previo += Read_Delay;              
       sensorDS18B20.requestTemperatures();    
       Temperatura = sensorDS18B20.getTempCByIndex(0);     //Lectura del sensor LM35
       Serial.println(Temperatura);
       displayseg.showNumberDec(Temperatura,false,2,0);
       displayseg.setSegments(celsius, 2,2);
   }
  
}

void Fase()  
{ 
  P= map(ang_salida,100,0,7600,10);//los valores del potenciometro interpolan en grados de 0 a 180 */
  delayMicroseconds(P); //para que el delay sea del orden 8000us cuando el POT sea 5v
  digitalWrite(triac, HIGH);
  delayMicroseconds(200);  
  // retraso de 200 uSec en el pulso de salida para encender el triac
  digitalWrite(triac, LOW);
}
