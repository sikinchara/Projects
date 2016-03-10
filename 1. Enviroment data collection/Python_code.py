"""
Projektni zadatak iz kolegija "Raspoznavanje uzoraka i strojno ucenje".
Cilj projekta je pomocu Arduino razvojnog sustava napraviti dataset koji pomocu
senzora mjeri stanje prostorije (temperatura, CO2, vlaga, svjetlina) te 
u Python programskom okruzenju napraviti obradu, vizualizaciju i 
napraviti predikciju pomocu linearne i logisticke regresije nad podacima.
"""
#Koristene biblioteke
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np


#Citanje podataka iz csv dokumenta
df = pd.read_csv('soba.csv')
#Dodavanje stupca "Vrijeme" unutar postojeceg dataframe-a
df['Vrijeme']= pd.date_range('2016-03-02 21:15:00', periods=len(df), freq='15T')
#Sortiranje indeksa
df = df[['Vrijeme','CO2','Temperatura','Vlaga','Svjetlina','Prisutnost']]
print ('Skup podataka se sastoji od {} elemenata\n'.format(len(df)))


#Statisticki pregled podataka
print df.describe()
print('\n')
#Standardna devijacija podataka (prosjecno odstupanje od prosjeka i to u apsolutnom iznosu)
print df.std()
print('\n')
#Ispis prva tri elementa
print "Ispis prva tri reda:\n",df.head(3)
print('\n')
#Ispis zadnja tri elementa
print "Ispis zadnja tri reda:\n",df.tail(3)
#Ukupni pregled podataka pomocu histograma
df.hist()

#Pojedinacni histogrami
vlaga = df['Vlaga']
plt.figure()
plt.hist(vlaga, facecolor='red',alpha=0.75)
plt.title('Vlaga')
plt.grid()
plt.show()

co2 = df['CO2']
plt.figure()
plt.hist(co2,facecolor='green',alpha=0.75)
plt.title('Kolicina CO2')
plt.grid()
plt.show()

temperatura = df['Temperatura']
plt.figure()
plt.hist(temperatura, facecolor='cyan',alpha=0.75)
plt.title('Temperatura')
plt.grid()
plt.show()

svjetlina = df['Svjetlina']
plt.figure()
plt.hist(svjetlina,facecolor='yellow',alpha=0.75)
plt.title('Jacina svjetlosti')
plt.grid()
plt.show()

prisutnost = df['Prisutnost']
plt.figure()
plt.hist(prisutnost,facecolor='black',alpha=0.75)
plt.title('Prisutnost')
plt.grid()
plt.show()

#Moramo ga oblikovat kao 1-d polje
co2ts = co2.reshape([1,458])
vrijemets = pd.date_range('2016-03-02 21:15:00', periods=len(co2),freq='15T')
#Pomocu naredbe ravel() ga pretvaramo u 1-d niz (array)
ts_co2 = pd.Series(data=co2ts.ravel(), index = vrijemets)
plt.figure()
plt.title('Kolicina CO2 od 03.02. do 07.02.')
ts_co2.plot(grid=True)


#------------------------------PRIMJENA MODELA---------------------------------
#Omjeri
#70% podataka
train = round(len(df)*0.7,0)
train_int = int(train)
#30% podataka
test = round(len(df)*0.3,0)
test_int = int(test)

#Koristenje CO2 stupca
co2 = df['CO2']
#Koristenje stupca sa temperaturama
vlaga = df['Vlaga']

#Podjela CO2 podataka u podatke za treniranje/testiranje
co2_x_train = co2[:train_int]
co2_x_test = co2[test_int*(-1):]

#Podjela temperaturnih podataka u podatke za treniranje/testiranje
co2_y_train = vlaga[:train_int]
co2_y_test = vlaga[test_int*(-1):]

#-----------------------------Linearna regresija-------------------------------

#Regresijski model koji koristimo
regr = linear_model.LinearRegression()

#Preoblikovanje elemenata kako bi sklearn mogao koristiti podatke
co2x_train = co2_x_train.reshape((321,1))
co2y_train = co2_y_train.reshape((321,1))

co2x_test = co2_x_test.reshape((137,1))
co2y_test = co2_y_test.reshape((137,1))

#Fitanje regresijskog modela
regr.fit(co2x_train, co2y_train)

#Plotanje rezultata dobiveni pomoću linearne regresije
plt.figure()
plt.scatter(co2x_test, co2y_test, color='orange')
plt.plot(co2x_test, regr.predict(co2x_test), color='blue', linewidth=2)
plt.title("Linearna regresija (CO2 i Prisutnost)")
plt.xticks(())
plt.yticks(())
plt.show()

#Ispis podataka modela
print('Koeficijenti: {}'.format(regr.coef_))
print('Kvadratna pogreska: {}'.format(np.mean((regr.predict(co2x_test)-co2y_test)**2)))
print('Varijanca: {}'.format(regr.score(co2x_test, co2y_test)))


#-----------------------------Logisticka Funkcija------------------------------

prisutnost = df['Prisutnost']

clf = linear_model.LogisticRegression()
#clf.fit()
