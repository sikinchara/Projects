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
import sklearn.cross_validation as cv
from sklearn import metrics
import numpy as np

#Citanje podataka iz csv dokumenta
df = pd.read_csv('soba.csv')
#Dodavanje stupca "Vrijeme" unutar postojeceg dataframe-a
df['Vrijeme']= pd.date_range('2016-03-02 21:15:00', periods=len(df), freq='15T')
#Sortiranje indeksa
df = df[['Vrijeme','CO2','Temperatura','Vlaga','Svjetlina','Prisutnost']]
print ('Skup podataka se sastoji od {} elemenata\n'.format(len(df)))


#Statisticki pregled podataka
print df.describe().transpose()
print('\n')
#Standardna devijacija podataka (prosjecno odstupanje od prosjeka i to u apsolutnom iznosu)
print ("Standardna devijacija podataka:")
print df.std()
print('\n')
#Ispis prva tri elementa
print "Ispis prva tri reda:\n",df.head(3)
print('\n')
#Ispis zadnja tri elementa
print "Ispis zadnja tri reda:\n",df.tail(3)
#Ukupni pregled podataka pomocu histograma
df.hist(figsize=(8,8))

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
temperaturats = temperatura.reshape([1,458])
vlagats = vlaga.reshape([1,458])
vrijemets = pd.date_range('2016-03-02 21:15:00', periods=len(co2),freq='15T')
#Pomocu naredbe ravel() ga pretvaramo u 1-d niz (array)
ts_co2 = pd.Series(data=co2ts.ravel(), index = vrijemets)
ts_temperatura = pd.Series(data=temperaturats.ravel(), index = vrijemets)
ts_vlaga = pd.Series(data=vlagats.ravel(), index = vrijemets)
plt.figure()
plt.title('Kolicina CO2 od 03.02. do 07.02.')
ts_co2.plot(grid=True)
plt.figure()
plt.title('Temperatura od 03.02. do 07.02.')
ts_temperatura.plot(grid=True)
plt.figure()
plt.title('Vlaga od 03.02. do 07.02.')
ts_vlaga.plot(grid=True)

#------------------------------PRIMJENA MODELA---------------------------------
#Podjela ulazno/izlaznih podataka na treniranje i testiranje
#Omjer -> Train:Test = 70:30
(X_train, X_test, y_train, y_test) = cv.train_test_split(vlaga, co2, test_size=.3, random_state=0)

#-----------------------------Linearna regresija-------------------------------
print("-------------------------------LINEARNA REGRESIJA----------------------------")
#Koristeni regresijski model
regr = linear_model.LinearRegression()

#Preoblikovanje elemenata kako bi sklearn mogao koristiti podatke (za X i Y)
X_train = X_train.reshape((len(X_train),1))
X_test = X_test.reshape((len(X_test),1))

y_train = y_train.reshape((len(y_train),1))
y_test = y_test.reshape((len(y_test),1))

#Fitanje regresijskog modela
regr.fit(X_train, y_train)

#Plotanje rezultata dobiveni pomocu linearne regresije
plt.figure(figsize=(10,10))
plt.plot(X_test, regr.predict(X_test), color='blue', linewidth=2, label='Predikcija',hold='on',alpha=.75)
plt.scatter(X_test, y_test, color='orange',label='Podaci za treniranje',alpha=.5)
plt.legend(loc=2)
plt.xlabel('Vlaga')
plt.ylabel('CO2')
plt.title("Linearna regresija (CO2 i Vlaga)")
plt.xticks(())
plt.yticks(())
plt.show()

#Ispis podataka modela
#Estimirani koeficijenti dobiveni na temelju podataka
print "------------------------------------------------------------------------------\n"
b1 = regr.coef_[0]
print("Model po kojem se pravac estimirao: y= {} + {}x".format(regr.intercept_[0],b1[0]))
#Odstupanje od estimiranog pravca na testnim podacima
print('Srednja kvadratna pogreska: {}'.format(metrics.mean_squared_error(y_test,regr.predict(X_test))))
#Koliko su podaci dobro fitani za dan model
print('Varijanca: {}\n'.format(regr.score(X_test, y_test)))


#-----------------------------Logisticka Regresija-----------------------------
print("-------------------------------LOGISTICKA REGRESIJA----------------------------\n")
#Primjena modela za ucenje
#L1 - smanjenje overfitanja modela (regularizacija), C - inverz regularizacijske snage 
#veca vrijednost C-a, veci prostor rješenja
lr = linear_model.LogisticRegression(penalty='l1',C=100,tol=0.0001)
#from sklearn import metrics

#Podjela podataka na treniranje i testiranje pri cemu je X = co2, a Y = prisutnost
#Omjer podjele je treniranje:testiranje=7:3
(X_train, X_test, y_train, y_test) = cv.train_test_split(co2, prisutnost, test_size=.3, random_state=0)
print("----------------------------------CO2/PRISUTNOST-------------------------------\n")
print ('Distribucija po klasama testnog skupa:')
print y_test.value_counts()
#Prisutnost izrazena u postocima
print ("Postotak jedinica (prisutan): {:2f}%".format(y_test.mean()*100))
print ("Postotak nula (nije prisutan): {:2f}%\n".format(100-y_test.mean()*100))
#Oblikovanje ulaznog i izlaznog skupa za treniranje s kojima naredba fit moze radit

X_train = X_train.reshape((len(X_train),1))
y_train = y_train.reshape((len(y_train),1)).ravel()
lr.fit(X_train, y_train)
print ('Varijanca: {:2f} %'.format(lr.score(X_train,y_train)*100))

#sorted(X_test, key=int)
#sorted(y_test, key=int)
X_test = X_test.reshape(len(X_test),1)
y_test = y_test.reshape(len(y_test),1)
y_predikcija = lr.predict(X_test)

#Ispis prvih 25 vrijednosti True i Predictet klasa
print ("Usporedba pravih i predvidjenih vrijednosti")
print ('True:{}'.format(y_test[:23].reshape(1,23)))
print ('Pred:[{}]'.format(y_predikcija[:23]))

#Iscrtavanje podataka pomocu scatter plot-a
plt.figure()
plt.scatter(X_test,y_test, alpha=.6, hold="on",label="Test")
plt.scatter(X_test,y_predikcija, alpha=.4, color='orange',marker='^',label="Predicted")
plt.legend(loc=6)

#def model(x):
#    return 1 / (1 + np.exp(-x))
#model(X_test)
#plt.plot(y_test, model(X_test), color='blue', linewidth=2)

plt.title("Testni i predvidjeni podaci")
plt.show()

vjerojatnosti = lr.predict_proba(X_test)

labels = ['Nije prisutan', 'Prisutan']
cm = metrics.confusion_matrix(y_test, y_predikcija)
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels,rotation='vertical')
for i in range (len(cm)):
    for j in range (len(cm)):
        ax.annotate(str(cm[j][i]), xy = (i,j),fontsize=25)

plt.colorbar(cax)
plt.title("Konfuzijska matrica (CO2|Prisutnost)")
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

print ("Tocnost klasifikacije: {} %".format(metrics.accuracy_score(y_test, y_predikcija)*100))



#--------------------------------------Temperatura/CO2-----------------------------------

print("------------------------------TEMPERATURA/PRISUTNOST-----------------------------------")
(X_train, X_test, y_train, y_test) = cv.train_test_split(temperatura, prisutnost, test_size=.3, random_state=0)

X_train = X_train.reshape((len(X_train),1))
y_train = y_train.reshape((len(y_train),1)).ravel()
lr.fit(X_train, y_train)

X_test = X_test.reshape(len(X_test),1)
y_test = y_test.reshape(len(y_test),1)
y_predikcija = lr.predict(X_test)

print ('Varijanca: {:2f} %'
.format(metrics.accuracy_score(y_test,y_predikcija)*100))

#Ispis prvih 25 vrijednosti True i Predictet klasa
print ("Usporedba pravih i predvidjenih vrijednosti")
print ('True:{}'.format(y_test[:23].reshape(1,23)))
print ('Pred:[{}]'.format(y_predikcija[:23]))


plt.figure()
plt.scatter(X_test,y_test, alpha=.6, hold="on",label="Test")
plt.scatter(X_test,y_predikcija, alpha=.4, color='orange',marker='^',label="Predicted")
plt.legend(loc=6)
plt.title("Testni i predvidjeni podaci")
plt.show()

vjerojatnosti = lr.predict_proba(X_test)
labels = ['Nije prisutan', 'Prisutan']
cm = metrics.confusion_matrix(y_test, y_predikcija)
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(cm)
ax.set_xticklabels([''] + labels)
ax.set_yticklabels([''] + labels,rotation='vertical')
for i in range (len(cm)):
    for j in range (len(cm)):
        ax.annotate(str(cm[j][i]), xy=(i,j),fontsize=25)

plt.colorbar(cax)
plt.title("Konfuzijska matrica (Temperatura|Prisutnost)")
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

print ("Tocnost klasifikacije: {} %".format(metrics.accuracy_score(y_test, y_predikcija)*100))


#------------------------------------------------------------------------------





