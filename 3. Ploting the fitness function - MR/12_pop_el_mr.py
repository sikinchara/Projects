import pandas as pd
import matplotlib.pyplot as plt

def najveci_df():
    a,b,c = len(df1),len(df2),len(df3)
    najveci = a
    if(a<b and c<b):
        najveci = df2.index
    elif(a<c and b<c):
        najveci = df3.index
    else:
        najveci = df1.index
    return najveci
        
    
#Citanje podataka iz CSV file-a
#Podaci MORAJU biti u obliku "50_bp.csv"
df1 = pd.read_csv('50_bp.csv',delim_whitespace=True)
df2 = pd.read_csv('100_bp.csv',delim_whitespace=True)
df3 = pd.read_csv('200_bp.csv',delim_whitespace=True)

#Odabiranje stupca 'Min' iz datoteka
minimum1 = df1['Min']
minimum2 = df2['Min']
minimum3 = df3['Min']

#Sortiranje Min-ova u novi Data Frame
new_df = pd.concat([minimum1,minimum2,minimum3],axis = 1)
new_df.columns = ['50','100','200']
generacija = new_df.index

#plotanje rezultata
plt.figure()
new_df.plot()
plt.grid()
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.title('Pop 50,100,200 - bez permutacije')
plt.savefig('Pop12_BEZ_Permutacije.png')

#-----------------------Sa Permutacijom--------------------------------------

#Citanje podataka iz CSV file-a
df1 = pd.read_csv('50_p.csv',delim_whitespace=True)
df2 = pd.read_csv('100_p.csv',delim_whitespace=True)
df3 = pd.read_csv('200_p.csv',delim_whitespace=True)

#Odabiranje stupca 'Min' iz datoteka
minimum1 = df1['Min']
minimum2 = df2['Min']
minimum3 = df3['Min']

#Sortiranje Min-ova u novi Data Frame
new_df = pd.concat([minimum1,minimum2,minimum3],axis = 1)
new_df.columns = ['50','100','200']
generacija = new_df.index

#plotanje rezultata
plt.figure()
new_df.plot()
plt.grid()
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.title('Pop 50,100,200 - SA permutacijom')
plt.savefig('Pop12_SA_Permutacijom.png')

#---------------------------------Mutacija------------------------------------
#----------------------------------bez permutacije----------------------------

#Citanje podataka iz CSV file-a
#Podaci MORAJU biti u obliku "50_bp.csv"
df1 = pd.read_csv('50_bp.csv',delim_whitespace=True)
df2 = pd.read_csv('mr8_bp.csv',delim_whitespace=True)
df3 = pd.read_csv('mr16_bp.csv',delim_whitespace=True)

#Odabiranje stupca 'Min' iz datoteka
minimum1 = df1['Min']
minimum2 = df2['Min']
minimum3 = df3['Min']

#Sortiranje Min-ova u novi Data Frame
new_df = pd.concat([minimum1,minimum2,minimum3],axis = 1)
new_df.columns = ['4','8','16']
generacija = new_df.index

#plotanje rezultata
plt.figure()
new_df.plot()
plt.grid()
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.title('Mutacija 4,8,16 - bez permutacije')
plt.savefig('MR12_BEZ_Permutacije.png')

#-----------------------Sa Permutacijom--------------------------------------

#Citanje podataka iz CSV file-a
df1 = pd.read_csv('50_p.csv',delim_whitespace=True)
df2 = pd.read_csv('mr8_p.csv',delim_whitespace=True)
df3 = pd.read_csv('mr16_p.csv',delim_whitespace=True)

#Odabiranje stupca 'Min' iz datoteka
minimum1 = df1['Min']
minimum2 = df2['Min']
minimum3 = df3['Min']

#Sortiranje Min-ova u novi Data Frame
new_df = pd.concat([minimum1,minimum2,minimum3],axis = 1)
new_df.columns = ['4','8','16']
generacija = new_df.index

#plotanje rezultata
plt.figure()
new_df.plot()
plt.grid()
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.title('Mutacija 4,8,16 - SA permutacijom')
plt.savefig('MR12_SA_Permutacijom.png')

#---------------------------------Elita----------------------------------------
#----------------------------------bez permutacije----------------------------

#Citanje podataka iz CSV file-a
#Podaci MORAJU biti u obliku "50_bp.csv"
df1 = pd.read_csv('50_bp.csv',delim_whitespace=True)
df2 = pd.read_csv('el8_bp.csv',delim_whitespace=True)
df3 = pd.read_csv('el16_bp.csv',delim_whitespace=True)

#Odabiranje stupca 'Min' iz datoteka
minimum1 = df1['Min']
minimum2 = df2['Min']
minimum3 = df3['Min']

#Sortiranje Min-ova u novi Data Frame
new_df = pd.concat([minimum1,minimum2,minimum3],axis = 1)
new_df.columns = ['4','8','16']
generacija = new_df.index

#plotanje rezultata
plt.figure()
new_df.plot()
plt.grid()
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.title('Elita 4,8,16 - bez permutacije')
plt.savefig('EL12_BEZ_Permutacije.png')

#-----------------------Sa Permutacijom--------------------------------------

#Citanje podataka iz CSV file-a
df1 = pd.read_csv('50_p.csv',delim_whitespace=True)
df2 = pd.read_csv('el8_p.csv',delim_whitespace=True)
df3 = pd.read_csv('el16_p.csv',delim_whitespace=True)

#Odabiranje stupca 'Min' iz datoteka
minimum1 = df1['Min']
minimum2 = df2['Min']
minimum3 = df3['Min']

#Sortiranje Min-ova u novi Data Frame
new_df = pd.concat([minimum1,minimum2,minimum3],axis = 1)
new_df.columns = ['4','8','16']
generacija = new_df.index

#plotanje rezultata
plt.figure()
new_df.plot()
plt.grid()
plt.xlabel('Generacija')
plt.ylabel('Fitness')
plt.title('Elita 4,8,16 - SA permutacijom')
plt.savefig('EL12_SA_Permutacijom.png')