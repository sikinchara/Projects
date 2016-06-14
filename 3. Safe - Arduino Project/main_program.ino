#include <Wire.h>
#include <LiquidCrystal_I2C.h>
//Biblioteka pomocu koje koristimo tipkovnicu
#include "Keypad.h"

//Definiranje redova i stupaca za membransku tipkovnicu
//Oblik tipkovnice
const byte ROWS = 4; //cetiri reda
const byte COLS = 3; //tri stupca
char keys[ROWS][COLS] = {
{'1','2','3'},
{'4','5','6'},
{'7','8','9'},
{'*','0','#'}
};
//Definirani pinovi na Arduinu
byte rowPins[ROWS] = {8, 7, 6, 5}; //Pinovi koristeni za RED tipkovnice
byte colPins[COLS] = {4, 3, 2}; //Pinovi koristeni za STUPAC tipkovnice

//mapiranje tipkovnice
Keypad tipkovnica = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

//Potrebne varijable za lozinku
char lozinka[6];//Velicina lozinka
char broj_pina[6]="12345";//Lozinka
char tipka_vrijednost;//Varijabla za pohranu vrijednosti unesenih sa tipkovnice,pohrana od jednog znaka
int brojac_pin=3;//Brojac za krivo unesen pin
int brojac = 0;//brojac za kretanje kroz polje za lozinku
int i = 0; //ispis teksta

//LED-ice
#define CRVENI_PIN 24
#define ZUTI_PIN 26
#define ZELENI_PIN 28

//Step motor pinovi - polovi motora
#define IN1 10 //D
#define IN2 11 //C
#define IN3 12 //B
#define IN4 13 //A
//Brojcana vrijednost koja nam govori koliko je ciklusa potrebno za puni krug
#define MOTOR_KRUG 512
#define MIKRO_SKLOPKA 34

//TIPKA
int tipka_zatvaranje = 32;//Koristeni pin za tipku
int tipka_zatvaranje_vrijednost = 0;//pohrana vrijednosti sa tipke
bool zatvaranje = 0;//Flag varijabla pomocu koje ispunjavamo uvjet za zatvaranje

//LCD display - postavljanje adrese i mapiranje pinova
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

//Zvucnik
int zvucnikPin = 9; //analogni pin 9

//---------------------------STEP MOTOR--------------------------
//Funkcija za okretanje step motora
void motor_okretanje(float vrata)
{
  int ciklus = vrata * MOTOR_KRUG;
  ciklus = abs(ciklus);
  //Zatvaranje vrata - u smjeru kazaljke na satu
  if (vrata > 0)
  {
    for (int x=0;x<ciklus;x++)
    {
      for(int y=0; y<8; y++)
      {
        //Pozivanje funkcije pomocu koje se pale odredjeni polovi step motora
        motor_faze(y);
        delay(1);
      }
    }
  }
  //Otvaranje vrata - suprotno od smjera kazaljke na satu
  else
  {
    for (int x=0;x<ciklus;x++)
    {
      for(int y=7; y>=0; y--)
      {
        //Pozivanje funkcije pomocu koje se pale odredjeni polovi step motora
        motor_faze(y);
        delay(1);
      }
    }
  }
}

//Koristi se prilikom inicjalizacije vrata
void motor_ucitavanje(float vrata)
{
  int ciklus = vrata * MOTOR_KRUG;
  ciklus = abs(ciklus);
  //Zatvaranje vrata - u smjeru kazaljke na satu
  while(digitalRead(MIKRO_SKLOPKA)!=HIGH)
  {
    for (int x=0;x<ciklus;x++)
    {
      for(int y=0; y<8; y++)
      {
        //Pozivanje funkcije pomocu koje se pale odredjeni namotaji step motora
        motor_faze(y);
        delay(1);
        Serial.println(digitalRead(MIKRO_SKLOPKA));
      }
    }
  }
  delay(50);
 motor_okretanje(-0.5);
 Serial.println("Gotovo");
}
//Paljenje namotaja u odredjenom trenutku
void motor_faze(int faza)
{
  switch(faza)
  {
     case 0:
       digitalWrite(IN1, LOW); 
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, HIGH);
       break; 
     case 1:
       digitalWrite(IN1, LOW); 
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, HIGH);
       digitalWrite(IN4, HIGH);
       break; 
     case 2:
       digitalWrite(IN1, LOW); 
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, HIGH);
       digitalWrite(IN4, LOW);
       break; 
     case 3:
       digitalWrite(IN1, LOW); 
       digitalWrite(IN2, HIGH);
       digitalWrite(IN3, HIGH);
       digitalWrite(IN4, LOW);
       break; 
     case 4:
       digitalWrite(IN1, LOW); 
       digitalWrite(IN2, HIGH);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, LOW);
       break; 
     case 5:
       digitalWrite(IN1, HIGH); 
       digitalWrite(IN2, HIGH);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, LOW);
       break; 
     case 6:
       digitalWrite(IN1, HIGH); 
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, LOW);
       break; 
     case 7:
       digitalWrite(IN1, HIGH); 
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, HIGH);
       break; 
     default:
       digitalWrite(IN1, LOW); 
       digitalWrite(IN2, LOW);
       digitalWrite(IN3, LOW);
       digitalWrite(IN4, LOW);
       break; 
  }
}
//---------------------TIPKOVNICA----------------------------
void pocisti_pin()
{
  while(brojac != 0)
  {
    lozinka[brojac--] = 0;
  }  
}

//Unosi znamenaka pina u sustav
void unos_alarm()
{
  tipka_vrijednost = tipkovnica.getKey();
  //ako je tipka pritisnuta...
  if(tipka_vrijednost)
     {
      //Pohrana zasebne znamenke u polje 
         lozinka[brojac] = tipka_vrijednost;
         brojac++;
         if (brojac==5)
         {
          beep(250);
         }
     }
}
void unos()
{
  {
  tipka_vrijednost = tipkovnica.getKey();
  //Unos lozinke
  if(tipka_vrijednost)
     {
      //Pohrana zasebne znamenke u polje 
         lozinka[brojac] = tipka_vrijednost;
         beep(100);
         Serial.print(lozinka[brojac]);
         lcd.setCursor(brojac,1);
         lcd.print("*");
         brojac++;
     }
}
}
//------------------ZVUCNIK---------------------
void beep(unsigned char delayms)
{
  analogWrite(9,10);
  delay(delayms);
  analogWrite(9,0); 
  delay(delayms);
}

//---------------------------------------------

void setup() 
{
  Serial.begin(9600);
  lcd.begin(16,2);
  lcd.backlight();
  lcd.print("Ucitavam...");
  Serial.println("Inicijaliziram");
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  pinMode(MIKRO_SKLOPKA,INPUT);
  motor_ucitavanje(0.05);
  pinMode(tipka_zatvaranje, INPUT);
  pinMode(CRVENI_PIN,OUTPUT);
  pinMode(ZUTI_PIN,OUTPUT);
  pinMode(ZELENI_PIN,OUTPUT);
  digitalWrite(CRVENI_PIN,HIGH);
  delay(500);
  digitalWrite(CRVENI_PIN,LOW);
  digitalWrite(ZUTI_PIN,HIGH);
  delay(500);
  digitalWrite(ZUTI_PIN,LOW);
  digitalWrite(ZELENI_PIN,HIGH);
  delay(500);
  digitalWrite(ZELENI_PIN,LOW);
  pinMode(zvucnikPin, OUTPUT);
  beep(1000);
  digitalWrite(ZUTI_PIN,HIGH);
  lcd.clear();
  lcd.print("Gotovo!");
  delay(1250);
  lcd.clear();
  lcd.print("Lozinka: ");
  Serial.println("Gotovo!");
  Serial.println("Unesite lozinku: ");
}

void loop() 
{
  
  unos(); //Unos pina u sustav
  
  //Kad se sustav vrati na pocetak, ispisuje na ekran navedeni tekst
  while (i == 1)
  {
    Serial.println("Unesite lozinku: ");
    lcd.clear();
    lcd.print("Lozinka: ");
    i--;
  }
  //Ako je uneseno 5 znamenaka za lozinku
  if (brojac == 5)
  {
    if(!strcmp(lozinka,broj_pina))
    {
      digitalWrite(ZUTI_PIN,LOW);
      digitalWrite(ZELENI_PIN,HIGH);
      Serial.println("");
      Serial.println("Lozinka je prihvacena!");
     
      //Otvara vrata kad je tocno unesen pin
      lcd.clear();
      lcd.print("Otvaranje...");
      Serial.println("Otvaranje...");
      //Pali zvucnik 4 puta
      for(int j = 0; j<=3; j++)
      {
        beep(1000);
      }
      motor_okretanje(0.5);
      lcd.clear();
      lcd.print("Otvoreno!");
      Serial.println("Otvoreno!");
      //Petlja koja drzi vrata otvorena sve dok se ne pritisne tipka za zatvaranje vrata
      while(zatvaranje != 1)
      {
        //Pridruzivanje vrijednosti ocitanih sa pina tipka_zatvaranje (HIGH/LOW)
        tipka_zatvaranje_vrijednost = digitalRead(tipka_zatvaranje);
        if (tipka_zatvaranje_vrijednost == HIGH)
        {
          zatvaranje++; //Flag varijabla
        }
      }
      lcd.clear();
      lcd.print("Zatvaranje..");
      Serial.println("Zatvaranje...");
      for(int j = 0; j<=2; j++)
      {
        beep(1000);
      }
      motor_okretanje(-0.5);
      lcd.clear();
      lcd.print("Zatvoreno!");
      Serial.println("Zatvoreno!");
      zatvaranje = 0;
      pocisti_pin();
      digitalWrite(ZELENI_PIN,LOW);
      digitalWrite(ZUTI_PIN,HIGH);
      //U slucaju krivo unesene lozinke da postavi brojac za pin na pocetnu vrijednost
      if(brojac_pin != 3)
      {
        brojac_pin = 3;
      }
      delay(2000);
      lcd.clear();      
    }
//-------------------------------------NETOCNA LOZINKA--------------------------------
    else
    {
      //Broj krivo unesenih pinova
      brojac_pin--;
      lcd.clear();
      lcd.print("Netocna lozinka");
      Serial.println("");
      Serial.println("Lozinka je netocna!");
      //Kad counter dodje do 0, upali alarm (3. pokusaj)
      if(brojac_pin == 0)
      {
        lcd.clear();
        lcd.print("ALARM!");
        pocisti_pin();
        Serial.println("ALARM!");
        digitalWrite(ZUTI_PIN,LOW);
        digitalWrite(CRVENI_PIN,HIGH);
        for(int j=0; j<=3;j++)
        {
          beep(350);
          beep(350);
          digitalWrite(CRVENI_PIN,LOW);
          delay(500);
          digitalWrite(CRVENI_PIN,HIGH);
        }
        int otkljucavanje = 0;
        //Unos glavne lozinke za otkljucavanje sustava
        while(otkljucavanje != 1)
        {
            unos_alarm();
            if(!strcmp(lozinka,broj_pina))
            {
              otkljucavanje++;
            }
            if(brojac == 5)
            {
              pocisti_pin();
            }
        }
        
        otkljucavanje = 0;//Postavlja flag varijablu na 0 za ponovni rad
        brojac_pin = 3;//Broj pokusaja vracen na 3
        digitalWrite(CRVENI_PIN,LOW);
        digitalWrite(ZUTI_PIN,HIGH);
        lcd.clear();
        lcd.print("Spreman za rad!");
        delay(1500);
        lcd.clear();
      }
      else
      {
        delay(1250);
        lcd.clear();
        lcd.print("Preostalo unosa:");
        lcd.setCursor(7,1);
        lcd.print(brojac_pin);
        delay(1250);
        Serial.print("Preostalo pokusaja: ");
        Serial.println(brojac_pin);
      }
    }
    delay(500);
    pocisti_pin();
    i++;
  }
  
}//LOOP petlja
