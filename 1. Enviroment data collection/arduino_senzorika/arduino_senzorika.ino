//Biblioteke za rad sa DHT11 senzorom
#include "DHT.h"
//Najava korištenog pina na Arduinu (PWM 2)
#define DHTPIN 2
//Najava korištenog senzora
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

//Korišteni pin za fotootpornik A0
int fotopin = 0;

//Pin D3 za prisutnost
int prekidacpin = 3;
//Varijabla u koju se sprema informacija o prisutnosti
int a=0;
//Varijabla u koju se sprema trenutno stanje sa prekidaca
int stanje = 0;
int co2pin = 1;

void setup() 
{
//Pocetak serijske komunikacije
  Serial.begin(57600);
//Početak korištenja DHT11 senzora
  dht.begin();
//Ispisuje jednom navedeni tekst
  Serial.print(__DATE__);
  Serial.print(" ");
  Serial.println(__TIME__);
  Serial.print("Svjetlina,Vlaga,Temperatura,CO2,Prisutnost");
  pinMode(co2pin, INPUT);
  pinMode(prekidacpin,INPUT);
}

//Funkcija koja na temelju stanja prekidaca daje 0 ili 1
int prisutnost()
{
  stanje = digitalRead(prekidacpin);
  if (stanje == HIGH)
  {
    a=1;
  }
  else 
  {
    a=0;  
  }
   return a;
}

//Funkcija pomocu koje ocitavamo i uzimamo medijan za co2
int co2()
{
  //Najava varijabli koje se koriste u funkciji
  int vrijednost = 0;
  int co2[5],i=0,j=0,najveca=0,temp=0;
  //Dodjeljivanje vrijednosti sa CO2 pina u polje sa zastojem
  //od 3 sekunde
  co2[0] = analogRead(co2pin);
  delay(3000);
  co2[1] = analogRead(co2pin);
  delay(3000);
  co2[2] = analogRead(co2pin);
  delay(3000);
  co2[3] = analogRead(co2pin);
  delay(3000);
  co2[4] = analogRead(co2pin);
  delay(3000);
  //Sortiranje elemenata - Bubble sort, padajuci
  for(i=0;i<5;i++)
  {
      for(j=1;j<5;j++)
      {
          if(co2[i]<co2[j])
          {
            temp = co2[i];
            co2[i] = co2[j];
            co2[j] = temp;
          }
      }
  }
  //Medijan od niza co2
  int medijan = co2[2];
  return medijan;
}
void loop() 
{
  //Varijabla u koju se sprema informacija o vlagi
  float h = dht.readHumidity();
  
  //Varijabla u koju se sprema informacija o temperaturi
  float t = dht.readTemperature();
  
  //Varijabla u koju se sprema informacija o svjetlosti
  float svjetlina = analogRead(fotopin);
  
  //Varijabla u koju se sprema informacija o CO2
  float co2vr = analogRead(co2pin);

  //Prikazuje prisutnost (1-prisutan, 0-nije prisutan)
  int prisutan = prisutnost();
   
  Serial.println("");
  //Serial.print("Svjetlina:");
  Serial.print(svjetlina);
  Serial.print(",");
  //Serial.print("Vlaga:");
  Serial.print(h);
  Serial.print(",");
  //Serial.print("Temperatura: ");
  Serial.print(t);
  Serial.print(",");
  //Serial.print("CO2: ");
  Serial.print(co2());
  Serial.print(",");
  //Serial.print("Prisutnost: ");
  Serial.print(prisutan);
  delay(885000);
}
