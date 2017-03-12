# PARTE 1: Importazione delle librerie

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import matplotlib.pyplot as plt
import numpy as np


# PARTE 2: Funzioni

def AperturaFilePotenziali():
    PercorsoPotenziali=askopenfilename()
    FilePotenziali=open(PercorsoPotenziali,'r').read()
    Potenziale=FilePotenziali.split("\n")

    for i in range (0, len(Potenziale)):
        Potenziale[i]=float(Potenziale[i])
    return Potenziale
    
def AperturaFileCorrenti():
    PercorsoCorrenti=askopenfilename()
    FileCorrenti=open(PercorsoCorrenti,'r').read()
    Corrente=FileCorrenti.split("\n")

    for i in range (0, len(Corrente)):
        Corrente[i]=float(Corrente[i])
    return Corrente

# PARTE 3: Impostazione dell'interfaccia grafica

# Impostazione dell'ambiente di lavoro per differenziate, potenziali e differenziali (dpd)

dpd = Tk() # contenitore principale
dpd.title("Correnti, potenziali e differenziali") # titolo della finestra
dpd.minsize(height=100,width=574) # dimensione minima della finestra
dpd.maxsize(height=dpd.winfo_screenwidth(), width=574) # dimensione massima della finestra
dpd.iconify() # Riduce a icona la finestra dpd, che al momento tanto Ã¨ vuota e inutile!

# PARTE 4: Procedura guidata di importazione dei file

# Apertura dei file delle correnti

Risposta = askquestion("Conferma di apertura", "Premere sÃ¬ per selezionare il file che contiene i valori delle correnti")
if Risposta == 'yes':
    Corrente = AperturaFileCorrenti()
else:
    exit(0)
    
# Apertura del file dei potenziali

Risposta = askquestion("Conferma di apertura", "Premere sÃ¬ per selezionare il file che contiene i valori dei potenziali")
if Risposta == 'yes':
    Potenziale = AperturaFilePotenziali()
else:
    exit(0)

# PARTE 5: Calcolo del differenziale e creazione della tabella con potenziale, corrente e Differenziale punto per punto

# Creazione della lista Differenziale della dimensione giusta

Differenziale = []

for i in range (0, len(Potenziale)-1):
    Differenziale.insert(i, (float(Corrente[i+1]-Corrente[i])/float((Potenziale[i+1]-Potenziale[i])))) # Calcolo del Differenziale: dy/dx punto a punto

# Stampa del differenziale

# Creazione della barra di scorrimento verticale attraverso l'uso di frame e canvas

dpd.grid_rowconfigure(0, weight=1)
dpd.grid_columnconfigure(0, weight=1)
canvas=Canvas(dpd)
canvas.grid(row=0, column=0, sticky='nswe')

vScroll = Scrollbar(dpd, orient=VERTICAL, command=canvas.yview)
vScroll.grid(row=0, column=1, sticky='ns')

canvas.configure(yscrollcommand=vScroll.set)

frame=Frame(canvas)
canvas.create_window(0,0, window=frame, anchor='nw')

# Creazione della tabella con i valori di potenziale, corrente e differenziale

Tabella=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='yellow', justify='center')
Tabella.grid(row=0,column=0, sticky=NSEW)
Tabella.insert(END, 'Potenziali')

Tabella=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='yellow', justify='center')
Tabella.grid(row=0,column=1, sticky=NSEW)
Tabella.insert(END, 'Correnti')

Tabella=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='yellow', justify='center')
Tabella.grid(row=0,column=2, sticky=NSEW)
Tabella.insert(END, 'Differenziali')

rows = []
for i in range(1,len(Potenziale)):
    cols = []
    #for j in range(0,3):
    Tabella = Entry(frame, relief=RIDGE, justify='center')
    Tabella.grid(row=i, column=0, sticky=NSEW)
    
    Tabella.insert(END, '%f' % (Potenziale[i-1]))
    cols.append(Tabella)

    Tabella = Entry(frame, relief=RIDGE, justify='center')
    Tabella.grid(row=i, column=1, sticky=NSEW)
    
    Tabella.insert(END, '%f' % (Corrente[i-1]))
    cols.append(Tabella)
    
    Tabella = Entry(frame, relief=RIDGE, justify='center')
    Tabella.grid(row=i, column=2, sticky=NSEW)
    
    Tabella.insert(END, '%f' % (Differenziale[i-1]))
    cols.append(Tabella)
    rows.append(cols)

# Aggiornamento della barra di scorrimento in base al numero dei valori

dpd.deiconify() # Mostra la finestra dpd
frame.update_idletasks()
canvas.configure(scrollregion=(0,0,frame.winfo_width(), frame.winfo_height()))

# PARTE 5: Impostazione del rumore e calcolo dei massimi e dei minimi

# Creazione della finestra

rum = Tk() # contenitore principale
rum.title("Rumore") # titolo della finestra
rum.minsize(height=90,width=350) # dimensione minima della finestra
rum.maxsize(height=90, width=350) # dimensione massima della finestra (coincide con la dimensione minima: la finestra non puÃ² essere ridimensionata)

# Creazione di un'etichetta

rumEtichetta=Label(rum, text="Inserire il limite del rumore rispetto al differenziale:")
rumEtichetta.pack()

# Creazione di una casella per l'input

rumInput = Entry(rum)
rumInput.pack(pady=5)
rumInput.focus_set()

# Funzione per il calcolo

def Calcolo():
    PuntiPresi = []
    Inizio = []
    Fine=[]
    InizioC = []
    FineC = []
    CorrentiPrese = []
    Rumore = float(rumInput.get()) # Acquisizione del rumore dalla casella di input (widget Entry)

    if((len(set(Potenziale)))!= len(Potenziale)):
        showwarning("Errore", "I punti inseriti non sono validi perchÃ© in almeno un caso ad ogni valore di potenziale corrisponde piÃ¹ di un valore di corrente.")
        exit()
            
    if Rumore < 0:   # Il rumore deve essere in valore assoluto
        Rumore=Rumore*(-1)
        
    # Selezione dei punti al di fuori della fascia del rumore
    
    for i in range (0, len(Potenziale)-1):
        if Differenziale[i]<0:
            if Differenziale[i]<Rumore*(-1):
                PuntiPresi.insert(i, Potenziale[i+1])
                CorrentiPrese.insert(i, Corrente[i+1])
            else:
                 PuntiPresi.insert(i, 0)
                 CorrentiPrese.insert(i,0)
        else:
            if Differenziale[i]>Rumore:
                PuntiPresi.insert(i, Potenziale[i+1])
                CorrentiPrese.insert(i, Corrente[i+1])
            else:
                PuntiPresi.insert(i, 0)
                CorrentiPrese.insert(i, 0)
        
    # Selezione dei punti di inizio (dei picchi) -> potenziale e corrente

    j=1
    for i in range (1, len(Potenziale)-1):
        if PuntiPresi[i]!=0:
            if PuntiPresi[i-1]==0:
                Inizio.insert(j, PuntiPresi[i])
                InizioC.insert(j, CorrentiPrese[i])
                j=j+1
    
    # Selezione dei punti di fine (dei picchi) -> potenziale e corrente

    k=0
    for i in range (0, len(Potenziale)-1):
        if PuntiPresi[i]!=0:
            if PuntiPresi[i+1]==0 and k<=j:
                Fine.insert(k, PuntiPresi[i])
                FineC.insert(k, CorrentiPrese[i])
                k=k+1
   
    # Creazione della barra di scorrimento verticale attraverso l'uso di frame e canvas
    mm = Tk()
    mm.title("Inizio e fine dei picchi")
    mm.minsize(height=180,width=630) # dimensione minima della finestra
    mm.maxsize(height=mm.winfo_screenwidth(), width=630) # dimensione massima della finestra (non coincide con la dimensione minima: la finestra puÃ² essere ridimensionata)
    mm.grid_rowconfigure(0, weight=1)
    mm.grid_columnconfigure(0, weight=1)
    canvas=Canvas(mm)
    canvas.grid(row=0, column=0, sticky='nswe')

    vScroll = Scrollbar(mm, orient=VERTICAL, command=canvas.yview)
    vScroll.grid(row=0, column=1, sticky='ns')

    canvas.configure(yscrollcommand=vScroll.set)

    frame=Frame(canvas)
    canvas.create_window(0,0, window=frame, anchor='nw')
    
    # Creazione della tabella con valori massimi e minimi per ciascun picco

                    # ID  |    FINE   |   INIZIO  |
                    # num | pot | cor | pot | cor |

    # Intestazione
    
    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=5, justify='center')
    MinMax.grid(row=1,column=0)
    MinMax.insert(END, 'ID')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=31, justify='center')
    MinMax.grid(row=0,column=1, columnspan=2)
    MinMax.insert(END, 'Fine')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=31, justify='center')
    MinMax.grid(row=0,column=3, columnspan=2)
    MinMax.insert(END, 'Inizio')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=1, sticky=NSEW)
    MinMax.insert(END, 'Potenziali')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=2, sticky=NSEW)
    MinMax.insert(END, 'Correnti')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=3, sticky=NSEW)
    MinMax.insert(END, 'Potenziali')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=4, sticky=NSEW)
    MinMax.insert(END, 'Correnti')

    # Riempimento con i valori

    rows = []
    for i in range(2,len(Inizio)+1):
        cols = []
        for j in range(0,6):

            # ID del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=5, justify='center')
            Tabella.grid(row=i, column=0, sticky=NSEW)
            
            Tabella.insert(END, '%d' % (i-1))
            cols.append(Tabella)

            # Potenziale all'inizio del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=1, sticky=NSEW)
            
            Tabella.insert(END, '%0.3f' % (Inizio[i-2]))
            cols.append(Tabella)

            # Corrente all'inizio del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=2, sticky=NSEW)
            
            Tabella.insert(END, '%0.9f' % (InizioC[i-2]))
            cols.append(Tabella)

            # Potenziale alla fine del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=3, sticky=NSEW)
            
            Tabella.insert(END, '%0.3f' % (Fine[i-2]))
            cols.append(Tabella)

            # Corrente alla fine del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=4, sticky=NSEW)
            
            Tabella.insert(END, '%0.9f' % (FineC[i-2]))
            cols.append(Tabella)
            
        rows.append(cols)
  
    mm.deiconify() # Mostra la finestra mm
    frame.update_idletasks()
    canvas.configure(scrollregion=(0,0,frame.winfo_width(), frame.winfo_height()))
    
    # Calcolo dei dati della retta di base per ciascun picco (m e q)

    m = []
    q = []

    
    for i in range (0, len(Inizio)):
        if(Fine[i]!=Inizio[i]):
            m.insert(i, (FineC[i]-InizioC[i])/(Fine[i]-Inizio[i]))
            q.insert(i, InizioC[i])
        else:
           m.insert(i, 0)
           q.insert(i, InizioC[i])

    
    
    # Recupero tutti i punti all'interno di un picco, calcolo delle altezze e dell'area sottesa ad ogni picco
    
    MassimiCorrente = []
    PicchiPotenziali = []
    PicchiCorrenti = []
    RetteCorrenti=[]
    AltezzeCorrenti = []
    AreaTotalePicco=[]
    MassimiPotenziali=[]
    i=0
    j=0
    
    l=0
    
    for n in range (0, len(Inizio)-1): # Per n picchi
        c=0
        PiccoPotenziali = []
        PiccoCorrenti = []
        RettaCorrenti=[]
        AltezzaCorrenti=[]
        AreaParzialePicco=[]
        MassimoPot=[]
        k=0


        while (PuntiPresi[i]==0.0):
                i=i+1
                
        while(PuntiPresi[i]!=0.0): # Per tutti i punti di uno stesso picco
            PiccoPotenziali.insert(k, PuntiPresi[i])
            PiccoCorrenti.insert(k, CorrentiPrese[i])
            RettaCorrenti.insert(k, m[j]*PiccoPotenziali[k]+q[j])
            AltezzaCorrenti.insert(k, PiccoCorrenti[k]-RettaCorrenti[k])
            k=k+1
            i=i+1
        PicchiPotenziali.insert(n, PiccoPotenziali)
        PicchiCorrenti.insert(n, PiccoCorrenti)
        RetteCorrenti.insert(n, RettaCorrenti)
        AltezzeCorrenti.insert(n, AltezzaCorrenti)

        

        # Calcolo dell'altezza massima
        
        MassimoTemp=AltezzaCorrenti[0]
        MassimoTempCor=PiccoCorrenti[0]
        MassimoPot=PiccoPotenziali[0]
        for c in range (0, len(AltezzaCorrenti)):
            if AltezzaCorrenti[c] > MassimoTemp:
                MassimoTemp=AltezzaCorrenti[c]
                MassimoTempCor=PiccoCorrenti[c] # individua la corrente quando l'altezza del picco Ã¨ massima
                MassimoPot=PiccoPotenziali[c]
                
        MassimiCorrente.insert(l,MassimoTempCor)
        MassimiPotenziali.insert(l, MassimoPot)
    
    l=l+1
    # Calcolo le aree sotto ciascun picco
        
    
   
    AreePicchi = [] # ConterrÃ  tutte le aree dei picchi
    AreaParziale = [] # Area sotto una sezione del picco

    for z in range (0, len(Inizio)-1): # Per ogni picco
        AreaTotalePicco = 0.0 # Area sotto un picco (verrÃ  poi inserito in AreaPicchi come elemento della lista)
        
        for y in range (0, len(AltezzeCorrenti[z])-1): # Per ogni punto del picco
            AreaParziale.insert(y, (AltezzeCorrenti[z][y]+AltezzeCorrenti[z][y+1])*(PicchiPotenziali[z][y+1]-PicchiPotenziali[z][y])/2)
            AreaTotalePicco=AreaTotalePicco+AreaParziale[y]
        AreePicchi.insert(z, AreaTotalePicco)
        if AreePicchi[z]<0:
            AreePicchi[z]=AreePicchi[z]*(-1)
       
    AreePicchi=AreePicchi[::-1] # Inverto la lista delle aree dei picchi
    
    # Scrivo i massimi e le aree in una nuova finestra
    # Creazione della barra di scorrimento verticale attraverso l'uso di frame e canvas
    area = Tk()
    area.title("Area sottesa ai picchi e punti di massimo")
    area.minsize(height=180,width=580) # dimensione minima della finestra
    area.maxsize(height=area.winfo_screenwidth(), width=580) # dimensione massima della finestra (non coincide con la dimensione minima: la finestra puÃ² essere ridimensionata)
    area.grid_rowconfigure(0, weight=1)
    area.grid_columnconfigure(0, weight=1)
    canvas=Canvas(area)
    canvas.grid(row=0, column=0, sticky='nswe')

    vScroll = Scrollbar(area, orient=VERTICAL, command=canvas.yview)
    vScroll.grid(row=0, column=1, sticky='ns')

    canvas.configure(yscrollcommand=vScroll.set)

    frame=Frame(canvas)
    canvas.create_window(0,0, window=frame, anchor='nw')
    
    # Intestazione
    
    AM=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='plum', width=5, justify='center')
    AM.grid(row=0,column=0)
    AM.insert(END, 'ID')

    AM=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='plum', width=20, justify='center')
    AM.grid(row=0,column=1, sticky=NSEW)
    AM.insert(END, 'Massimo (corrente)')

    AM=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='plum', width=20, justify='center')
    AM.grid(row=0,column=2, sticky=NSEW)
    AM.insert(END, 'Massimo (potenziale)')

    AM=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='plum', width=15, justify='center')
    AM.grid(row=0,column=3, sticky=NSEW)
    AM.insert(END, 'Area sottesa')

    # Riempimento con i valori
    
    rows = []
    for i in range(2,len(Inizio)+1):
        cols = []
        for j in range(0,3):

            # ID del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=5, justify='center')
            Tabella.grid(row=i, column=0, sticky=NSEW)
            
            Tabella.insert(END, '%d' % (len(Inizio)-i+1))
            cols.append(Tabella)

            # Massimo (corrente)
            
            Tabella = Entry(frame, relief=RIDGE, width=20, justify='center')
            Tabella.grid(row=i, column=1, sticky=NSEW)
            
            Tabella.insert(END, '%0.10f' % (MassimiCorrente[i-2]))
            cols.append(Tabella)

            # Massimi (potenziali)
            
            Tabella = Entry(frame, relief=RIDGE, width=20, justify='center')
            Tabella.grid(row=i, column=2, sticky=NSEW)
            
            Tabella.insert(END, '%0.3f' % (MassimiPotenziali[i-2]))
            cols.append(Tabella)

            # Integrale
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=3, sticky=NSEW)
            
            Tabella.insert(END, '%0.15f' % (AreePicchi[i-2]))
            cols.append(Tabella)
            
        rows.append(cols)
  

    # Aggiornamento della barra di scorrimento in base al numero dei valori

    dpd.deiconify() # Mostra la finestra dpd
    frame.update_idletasks()
    canvas.configure(scrollregion=(0,0,frame.winfo_width(), frame.winfo_height()))

    
    rum.destroy() # Chiusura della finestra per l'acquisizione del rumore

    fig=plt.figure()
    fig.canvas.set_window_title('Grafico corrente-potenziale')
    plt.plot(Potenziale, Corrente)
    plt.ylabel('Corrente [A]')
    plt.xlabel('Potenziale [V]')
    plt.plot(Inizio, InizioC, 'ro')
    plt.plot(Fine, FineC, 'ro')
    plt.plot(MassimiPotenziali, MassimiCorrente, 'b^')
    plt.title('Grafico corrente-potenziale')
    plt.show()
    
# Creazione di un bottone per la conferma

rumBottone = Button(rum, text="Conferma",command=Calcolo)
rumBottone.pack(pady=10)

# Fine delle modifiche alle finestre

dpd.mainloop()
rum.mainloop()
