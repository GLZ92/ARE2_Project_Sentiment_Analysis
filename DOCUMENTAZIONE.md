# ARE2_Project_Sentiment_Analysis

Sentiment analysis di tweet generati in tempo reale.

__________________________________________________________

Questa è la documentazione relativa al Progetto di Are2 che affronta alcuni task di classificazione di tweet/testi generati in tempo reale dall'utente, tramite un'interfaccia grafica creata ad hoc, sulla base del suo sentimento.


## INSTALLAZIONE

Scaricare il repository https://github.com/harvardnlp/sent-conv-torch nel quale sono indicate la dipendenze di cui si necessità l'installazione al fine di ottenere il suo corretto funzionamento.

Scaricare i file **preprocess.py**, **main0.lua**, **preprocess0.py** e **GUI.py** da questo repository e metterli nella cartella sent-corv-torch scaricata precedentemente.

Sovrascrivere tranquillamente il file **preprocess.py**. Esso non fa altro che generare il file .txt di word_mapping contenente le indicizzazioni delle parole in un formato utilizzabile dallo script **preprocess0.py**. Inoltre al fine di eliminare anomalie, esso applica prima l'indicizzazione delle parole presenti nel dev-set (ovviamente nel caso in cui esso venga specificato) rispetto a quelle del test-set.

**preprocess0.py** e **main0.lua** sono due varianti degli script **preprocess.py** e **main.lua** originali che consentono rispettivamente di generare hdf5 contenenti solo le informazioni relative al test-set e di eseguirne la classificazione senza verificare la presenza di dati relativa al train-set di cui non si necessita.

**GUI.py** infine è lo script che avvia l'interfaccia grafica mediante la quale l'utente potrà specificare un tweet/testo e avviare la classificazione dopo aver selezionato il task desiderato.


## GENERAZIONE MODELLI e HDF5

Generare i modelli con lo script **preprocess.py** come indicato nella documentazione del progetto sent-conv-torch.

Eseguire **main.py** per generare i modelli.

Occorre sapere che **GUI.py** a seconda del task selezionato dall'utente avviera il modello opportuno e utilizza l'hdf5 relativo al test generato per quel task. In sostanza l'utente dovrà assicurarsi che i modelli e gli hdf5 risultino avere dei nomi specifici a seconda del task.
Si riportano in seguito le corrispondenza tra task e nomenclature dei file da generare:

 Task                | Model           | HDF5  |
| -----------------  |:-------------:| -----:|
| EI-oc , Angry      | EI-oc-angry.t7 | EI-oc-angry.hdf5 |
| EI-oc , Joy        | EI-oc-joy.t7 | EI-oc-joy.hdf5 |
| EI-oc , Sadness    | EI-oc-sadness.t7 | EI-oc-sadness.hdf5 |
| EI-oc , Fear       | EI-oc-fear.t7 | EI-oc-fear.hdf5 |


## ESECUZIONE

Per avviare il programma eseguire lo script **GUI.py**

Specificare il testo, il task di classificazione e premere **Start classification**

Il programma eseguirà nell'ordine **preprocess0.py** e **main0.py**; l'utente riceverà tramtite un messageBox la comunicazione della predizione effettuata da parte del programma.