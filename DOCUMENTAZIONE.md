# ARE2_Project_Sentiment_Analysis

Sentiment analysis di tweet generati in tempo reale.

__________________________________________________________

Questa è la documentazione relativa al Progetto di Are2 che affronta alcuni task di classificazione di tweet/testi generati in tempo reale dall'utente, tramite un'interfaccia grafica creata ad hoc, sulla base del suo sentimento.


## INSTALLAZIONE

Scaricare il repository https://github.com/harvardnlp/sent-conv-torch nel quale sono indicate la dipendenze di cui si necessita l'installazione al fine di ottenere il suo corretto funzionamento.

Scaricare i file **preprocess.py**, **main0.lua**, **preprocess0.py**, **GUI.py** e **stopwords.txt** da questo repository e metterli nella cartella sent-corv-torch scaricata precedentemente.

Sovrascrivere tranquillamente il file **preprocess.py**. Esso non fa altro che generare il file .txt di word_mapping contenente le indicizzazioni delle parole in un formato utilizzabile dallo script **preprocess0.py**. Inoltre al fine di eliminare anomalie, esso applica prima l'indicizzazione delle parole presenti nel dev-set (ovviamente nel caso in cui esso venga specificato) rispetto a quelle del test-set.

**preprocess0.py** e **main0.lua** sono due varianti degli script **preprocess.py** e **main.lua** originali che consentono rispettivamente di generare hdf5 contenenti solo le informazioni relative al test-set e di eseguirne la classificazione senza verificare la presenza di dati relativa al train-set di cui non si necessita e senza generare alcun nuovo modello.

**GUI.py** è lo script che avvia l'interfaccia grafica mediante la quale l'utente potrà specificare un tweet/testo e avviare la classificazione dopo aver selezionato il task desiderato.

**stopwords.txt** è un file contenente espressioni come articoli e congiunzioni e in generale parole di bassa rilevanza, che il programma ignorerà e scarterà dal tweet/testo generato tramite **GUI.py**


## CREAZIONE PATH FILE DI TEST

Utilizzando **GUI.py** verrà creato un file di tipo txt contenente il tweet inserito e salvato in opportune directory a seconda del task selezionato. Dobbiamo quindi creare prima gli opportune directory, nel modo seguente:

```
cd sent-conv-torch
mkdir custom_data
mkdir EI-oc
mkdir V-oc
mkdir V-oc-3c
mkdir angry
mkdir fear
mkdir joy
mkdir sadness
```
## GENERAZIONE MODELLI e HDF5

Generare i modelli con lo script **preprocess.py** come indicato nella documentazione del progetto sent-conv-torch.

Eseguire **main.lua** per generare i modelli.

Occorre sapere che **GUI.py** a seconda del task selezionato dall'utente avviera il modello opportuno e utilizza l'hdf5 relativo al test generato per quel task. In sostanza l'utente dovrà assicurarsi che i modelli e gli hdf5 risultino avere dei nomi specifici a seconda del task.
Il nome dell'hdf5 verrà indicato inizializzando il flag --custom_name, mentre il nome del modello viene specificato tramite il flag savefile. Nella documentazione del progetto sent-conv-torch sono riportati i dettagli relativi all'uso di questi flag.

Si riportano in seguito le corrispondenza tra task e nomenclature dei file da generare:

 Task                | Model           | HDF5  |
| -----------------  |:-------------:| -----:|
| EI-oc , Anger      | EI-oc-angry.t7 | EI-oc-angry.hdf5 |
| EI-oc , Joy        | EI-oc-joy.t7 | EI-oc-joy.hdf5 |
| EI-oc , Sadness    | EI-oc-sadness.t7 | EI-oc-sadness.hdf5 |
| EI-oc , Fear       | EI-oc-fear.t7 | EI-oc-fear.hdf5 |
| V-oc               | V-oc.t7       | V-oc.hdf5 |
| V-oc-3c               | V-oc-3c.t7       | V-oc-3c.hdf5 |


## ESECUZIONE

Per avviare il programma eseguire lo script **GUI.py**

Specificare il testo, il task di classificazione e premere **Start classification**

Il programma eseguirà nell'ordine **preprocess0.py** e **main0.py**; l'utente riceverà tramtite un messageBox la comunicazione della predizione effettuata da parte del programma.
