# PARTE 1: Importazione delle librerie

from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import matplotlib.pyplot as plt
import numpy as np


# PARTE 2: Funzioni

def AperturaFileTempRit():
    PercorsoTempRit=askopenfilename()
    FileTempRit=open(PercorsoTempRit,'r').read()
    TRit=FileTempRit.split("\n")
    TRit=TRit[:-1]

    for i in range (0, len(TRit)):
        TRit[i]=float(TRit[i])
    return TRit
    
def AperturaFileAbb():
    PercorsoAbb=askopenfilename()
    FileAbb=open(PercorsoAbb,'r').read()
    Abbond=FileAbb.split("\n")
    Abbond=Abbond[:-1]


    for i in range (0, len(Abbond)):
        Abbond[i]=float(Abbond[i])
    return Abbond

# PARTE 3: Impostazione dell'interfaccia grafica

# Impostazione dell'ambiente di lavoro per differenziate, potenziali e differenziali (dpd)

dpd = Tk() # contenitore principale
dpd.title("Abbondanza e tempo di ritenzione") # titolo della finestra
dpd.minsize(height=100,width=574) # dimensione minima della finestra
dpd.maxsize(height=dpd.winfo_screenwidth(), width=574) # dimensione massima della finestra
dpd.iconify() # Riduce a icona la finestra dpd, che al momento tanto Ã¨ vuota e inutile!

# PARTE 4: Procedura guidata di importazione dei file


Risposta = askquestion("Conferma di apertura", "Aprire il file relativo alle quantità di sostanza rilevate?")
if Risposta == 'yes':
    Abbond = AperturaFileAbb()
else:
    exit(0)
    
Risposta = askquestion("Conferma di apertura", "Aprire il file relativo ai tempi di ritenzione?")
if Risposta == 'yes':
    TRit = AperturaFileTempRit()
else:
    exit(0)

# PARTE 5: Calcolo del differenziale e creazione della tabella con tempo di ritenzione, abbondanza e Differenziale punto per punto

# Creazione della lista Differenziale della dimensione giusta

Differenziale = []

for i in range (0, len(TRit)-1):
    Differenziale.insert(i, (float(Abbond[i+1]-Abbond[i])/float((TRit[i+1]-TRit[i])))) # Calcolo del Differenziale: dy/dx punto a punto

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

# Creazione della tabella con i valori di tempo di ritenzione, abbondanza e differenziale

Tabella=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='yellow', justify='center')
Tabella.grid(row=0,column=0, sticky=NSEW)
Tabella.insert(END, 'Tempo')

Tabella=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='yellow', justify='center')
Tabella.grid(row=0,column=1, sticky=NSEW)
Tabella.insert(END, 'Abbondanza')

Tabella=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='yellow', justify='center')
Tabella.grid(row=0,column=2, sticky=NSEW)
Tabella.insert(END, 'Differenziali')

rows = []
for i in range(1,len(TRit)):
    cols = []
    #for j in range(0,3):
    Tabella = Entry(frame, relief=RIDGE, justify='center')
    Tabella.grid(row=i, column=0, sticky=NSEW)
    
    Tabella.insert(END, '%f' % (TRit[i-1]))
    cols.append(Tabella)

    Tabella = Entry(frame, relief=RIDGE, justify='center')
    Tabella.grid(row=i, column=1, sticky=NSEW)
    
    Tabella.insert(END, '%f' % (Abbond[i-1]))
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
rum.maxsize(height=90, width=350) # dimensione massima della finestra (coincide con la dimensione minima: la finestra non può essere ridimensionata)

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
    AbbPrese = []
    Rumore = float(rumInput.get()) # Acquisizione del rumore dalla casella di input (widget Entry)

    if((len(set(TRit)))!= len(TRit)):
        showwarning("Errore", "I punti inseriti non sono validi perché in almeno un caso ad un istante corrisponde più di un valore.")
        exit()
            
    if Rumore < 0:   # Il rumore deve essere in valore assoluto
        Rumore=Rumore*(-1)
        
    # Selezione dei punti al di fuori della fascia del rumore
    
    for i in range (0, len(TRit)-1):
        if Differenziale[i]<0:
            if Differenziale[i]<Rumore*(-1):
                PuntiPresi.insert(i, TRit[i+1])
                AbbPrese.insert(i, Abbond[i+1])
            else:
                 PuntiPresi.insert(i, 0)
                 AbbPrese.insert(i,0)
        else:
            if Differenziale[i]>Rumore:
                PuntiPresi.insert(i, TRit[i+1])
                AbbPrese.insert(i, Abbond[i+1])
            else:
                PuntiPresi.insert(i, 0)
                AbbPrese.insert(i, 0)
        
    # Selezione dei punti di inizio (dei picchi) -> tempor e abbondanza

    j=1
    for i in range (1, len(TRit)-1):
        if PuntiPresi[i]!=0:
            if PuntiPresi[i-1]==0:
                Inizio.insert(j, PuntiPresi[i])
                InizioC.insert(j, AbbPrese[i])
                j=j+1
    
    # Selezione dei punti di fine (dei picchi) -> tempor e abbondanza

    k=0
    for i in range (0, len(TRit)-1):
        try:
            if PuntiPresi[i]!=0:
                if PuntiPresi[i+1]==0 and k<=j:
                    Fine.insert(k, PuntiPresi[i])
                    FineC.insert(k, AbbPrese[i])
                    k=k+1
        except:
            pass
   
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
                    # num | trt | abb | trt | abb |

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
    MinMax.insert(END, 'Tempo')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=2, sticky=NSEW)
    MinMax.insert(END, 'Abbondanza')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=3, sticky=NSEW)
    MinMax.insert(END, 'Tempo')

    MinMax=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='paleturquoise', width=15, justify='center')
    MinMax.grid(row=1,column=4, sticky=NSEW)
    MinMax.insert(END, 'Abbondanza')

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

            # TRit all'inizio del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=1, sticky=NSEW)
            
            Tabella.insert(END, '%0.3f' % (Inizio[i-2]))
            cols.append(Tabella)

            # Abbond all'inizio del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=2, sticky=NSEW)
            
            Tabella.insert(END, '%0.9f' % (InizioC[i-2]))
            cols.append(Tabella)

            # TRit alla fine del picco
            
            Tabella = Entry(frame, relief=RIDGE, width=15, justify='center')
            Tabella.grid(row=i, column=3, sticky=NSEW)
            
            Tabella.insert(END, '%0.3f' % (Fine[i-2]))
            cols.append(Tabella)

            # Abbond alla fine del picco
            
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
    
    MassimiAbbond = []
    PicchiTempRit = []
    PicchiAbb = []
    RetteAbb=[]
    AltezzeAbb = []
    AreaTotalePicco=[]
    MassimiTempRit=[]
    i=0
    j=0
    
    l=0
    
    for n in range (0, len(Inizio)-1): # Per n picchi
        c=0
        PiccoTempRit = []
        PiccoAbb = []
        RettaAbb=[]
        AltezzaAbb=[]
        AreaParzialePicco=[]
        MassimoPot=[]
        k=0


        while (PuntiPresi[i]==0.0):
                i=i+1
                
        while(PuntiPresi[i]!=0.0): # Per tutti i punti di uno stesso picco
            PiccoTempRit.insert(k, PuntiPresi[i])
            PiccoAbb.insert(k, AbbPrese[i])
            RettaAbb.insert(k, m[j]*PiccoTempRit[k]+q[j])
            AltezzaAbb.insert(k, PiccoAbb[k]-RettaAbb[k])
            k=k+1
            i=i+1
        PicchiTempRit.insert(n, PiccoTempRit)
        PicchiAbb.insert(n, PiccoAbb)
        RetteAbb.insert(n, RettaAbb)
        AltezzeAbb.insert(n, AltezzaAbb)

        

        # Calcolo dell'altezza massima
        
        MassimoTemp=AltezzaAbb[0]
        MassimoTempCor=PiccoAbb[0]
        MassimoPot=PiccoTempRit[0]
        for c in range (0, len(AltezzaAbb)):
            if AltezzaAbb[c] > MassimoTemp:
                MassimoTemp=AltezzaAbb[c]
                MassimoTempCor=PiccoAbb[c] # individua la abbondanza quando l'altezza del picco Ã¨ massima
                MassimoPot=PiccoTempRit[c]
                
        MassimiAbbond.insert(l,MassimoTempCor)
        MassimiTempRit.insert(l, MassimoPot)
    
    l=l+1
    # Calcolo le aree sotto ciascun picco
        
    
   
    AreePicchi = [] # ConterrÃ  tutte le aree dei picchi
    AreaParziale = [] # Area sotto una sezione del picco

    for z in range (0, len(Inizio)-1): # Per ogni picco
        AreaTotalePicco = 0.0 # Area sotto un picco (verrÃ  poi inserito in AreaPicchi come elemento della lista)
        
        for y in range (0, len(AltezzeAbb[z])-1): # Per ogni punto del picco
            AreaParziale.insert(y, (AltezzeAbb[z][y]+AltezzeAbb[z][y+1])*(PicchiTempRit[z][y+1]-PicchiTempRit[z][y])/2)
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
    AM.insert(END, 'Massimo (Abbondanza)')

    AM=Entry(frame, relief=RIDGE, font=("Verdana",10,"bold"), background='plum', width=20, justify='center')
    AM.grid(row=0,column=2, sticky=NSEW)
    AM.insert(END, 'Massimo (Tempo)')

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

            # Massimo (abbondanza)
            
            Tabella = Entry(frame, relief=RIDGE, width=20, justify='center')
            Tabella.grid(row=i, column=1, sticky=NSEW)
            
            Tabella.insert(END, '%0.10f' % (MassimiAbbond[i-2]))
            cols.append(Tabella)

            # Massimi (potenziali)
            
            Tabella = Entry(frame, relief=RIDGE, width=20, justify='center')
            Tabella.grid(row=i, column=2, sticky=NSEW)
            
            Tabella.insert(END, '%0.3f' % (MassimiTempRit[i-2]))
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
    fig.canvas.set_window_title('Grafico')
    plt.plot(TRit, Abbond)
    plt.ylabel('Abbondanza [mL]')
    plt.xlabel('Tempo di ritenzione [s]')
    plt.plot(Inizio, InizioC, 'ro')
    plt.plot(Fine, FineC, 'ro')
    plt.plot(MassimiTempRit, MassimiAbbond, 'b^')
    plt.title('Grafico')
    plt.show()
    
# Creazione di un bottone per la conferma

rumBottone = Button(rum, text="Conferma",command=Calcolo)
rumBottone.pack(pady=10)

# Fine delle modifiche alle finestre

dpd.mainloop()
rum.mainloop()
