# ARE2_Project_Sentiment_Analysis

Sentiment analysis di tweet generati in tempo reale.

__________________________________________________________

Questa è la documentazione relativa al Progetto di Are2 che affronta alcuni task di classificazione di tweet/testi generati in tempo reale dall'utente, tramite un'interfaccia grafica creata ad hoc, sulla base del suo sentimento.

## INSTALLAZIONE

Scaricare il repository https://github.com/harvardnlp/sent-conv-torch nel quale sono indicate la dipendenze necessarie al suo corretto funzionamento.

Scaricare i file preprocess.py, main0.lua, preprocess0.py e GUI.py da questo repository e metterli nella cartella sent-corv-torch scaricata precedentemente.

Sovrascrivere tranquillamente il file preprocess.py. Esso permette di generare un file .txt di word_mapping contenente le indicizzazioni delle parole in un formato utilizzabile dal file preprocess0.py, evitando la nascita di conflitti che sballino le future procedure di classificazione. Inoltre sempre al fine di elminare anomalie, esso applica prima l'indicizzazione delle parole presenti nel dev-set (nel caso in cui sia indicato ovviamente) rispetto a quelle del test-set.


## ESECUZIONE

Generare i modelli con lo script preprocess.py come indicato nelle documentazione del progetto sent-conv-torch

Per avviare la classificazione su tweet/testi generati in tempo reale avviare lo script GUI.py

Specificare il testo, il task di classificazione e premere "Start classification"

Il programma eseguirà nell'ordine preprocess0.py e main0.py; l'utente riceverà tramtite un messageBox la comunicazione della predizione efettuata da parte del programma.
