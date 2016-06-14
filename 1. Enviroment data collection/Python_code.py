"""
Projektni zadatak iz kolegija "Raspoznavanje uzoraka i strojno ucenje".
Cilj projekta je pomocu Arduino razvojnog sustava napraviti dataset koji pomocu
senzora mjeri stanje prostorije (temperatura, CO2, vlaga, svjetlina) te 
u Python programskom okruzenju napraviti obradu, vizualizaciju i 
predikcijski model pomocu linearne i logisticke regresije.
"""
#Koristene biblioteke
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
#from sklearn.neural_network import BernoulliRBM as BNN
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
#Omjeri podataka
#70% podataka za treniranje
train = round(len(df)*0.7,0)
train_int = int(train)
#30% podataka za testiranje
test = round(len(df)*0.3,0)
test_int = int(test)

#Koristenje CO2 stupca
co2 = df['CO2']
#Koristenje stupca sa vlagom
vlaga = df['Vlaga']

#Podjela CO2 podataka u podatke za treniranje/testiranje
co2_x_train = co2[:train_int]
co2_x_test = co2[test_int*(-1):]

#Podjela CO2 podataka u podatke za treniranje/testiranje
co2_y_train = vlaga[:train_int]
co2_y_test = vlaga[test_int*(-1):]

#-----------------------------Linearna regresija-------------------------------

#Koristeni regresijski model
regr = linear_model.LinearRegression()

#Preoblikovanje elemenata kako bi sklearn mogao koristiti podatke (za X i Y)
co2x_train = co2_x_train.reshape((321,1))
co2y_train = co2_y_train.reshape((321,1))

co2x_test = co2_x_test.reshape((137,1))
co2y_test = co2_y_test.reshape((137,1))

#Fitanje regresijskog modela
regr.fit(co2x_train, co2y_train)

#Plotanje rezultata dobiveni pomocu linearne regresije
plt.figure(figsize=(8,6), dpi=100)
plt.scatter(co2x_test, co2y_test, color='orange')
plt.plot(co2x_test, regr.predict(co2x_test), color='blue', linewidth=2)
plt.title("Linearna regresija (CO2 i Vlaga)")
plt.xticks(())
plt.yticks(())
plt.show()

#Ispis podataka modela
print('Koeficijenti: {}'.format(regr.coef_))
print('Kvadratna pogreska: {}'.format(np.mean((regr.predict(co2x_test)-co2y_test)**2)))
print('Varijanca: {}'.format(regr.score(co2x_test, co2y_test)))

#-----------------------------Logisticka Regresija-----------------------------

#Korištena metoda Logističke Regresije
clf = linear_model.LogisticRegressionCV()
#Preoblikovanje u matricni oblik posto radi s takvim oblikom podataka
co2 = co2.reset_index().as_matrix()
#co2 = df[['Temperatura','CO2']].as_matrix()


##Podjela CO2 podataka u podatke za treniranje/testiranje
#co2_x_train = co2[:train_int]
#co2_x_test = co2[test_int*(-1):]
#
##Podjela CO2 podataka u podatke za treniranje/testiranje
#prisutnost_y_train = prisutnost[:train_int]
#prisutnost_y_test = prisutnost[test_int*(-1):]
#prisutnost = prisutnost.reshape(458,1).ravel()

clf.fit(co2,prisutnost)
#Fit - train podaci, predict - test
#Finoca crtanje granice odluke
h = 1

#Podaci sluze pregledniji prikaz podataka na grafu
#Odabir min i max vrijednosti od svih elemenata iz 0. stupca
x_min, x_max = co2[:, 0].min()-.5, co2[:, 0].max()+.5

#Odabir min i max vrijednosti od svih elemenata iz 1. stupca
y_min, y_max = co2[:, 1].min()-.5, co2[:, 1].max()+.5


#Izvlacenje koordinata x_min, y_min, x_max i y_max u matricnom obliku
#h => velicina jednog koraka
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])

# Put the result into a color plot
Z = Z.reshape(xx.shape)
plt.figure(1, figsize=(8,6), dpi=100)
plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

# Plot also the training points
plt.scatter(co2[:, 0], co2[:, 1], c=prisutnost, edgecolors='k', cmap=plt.cm.Paired)
plt.xlabel('Index')
plt.ylabel('CO2')
plt.title("Logisticka regresija")
#Granice na grafu za X i Y
plt.xlim(xx.min(), xx.max())
plt.ylim(yy.min(), yy.max())

plt.xticks(())
plt.yticks(())

plt.show()
# 