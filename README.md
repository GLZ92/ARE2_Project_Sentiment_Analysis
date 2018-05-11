# ARE2_Project_Sentiment_Analysis
Sentiment analysis on tweets

Questa è la documentazione relativa al Progetto di Are2 che ha come scopo la classificazione di tweet a seconda del suo sentimento.

INSTALLAZIONE

Scaricare il repository https://github.com/harvardnlp/sent-conv-torch nel quale sono indicate la dipendenze necessarie al suo funzionamento.

Scaricare i file preprocess.py, main0.lua, preprocess0.py e GUI.py da questo repository e metterli nella cartella sent-corv-torch scaricata precedentemente.

Sovrascrivere tranquillamente il file preprocess.py. Esso dal punto di vista algoritmico è identico al preprocess preesistente, ma permette di generare un file contenente le indicizzazioni delle parole in un formato utilizzabile dal file preprocess0.py, evitando la nascita di conflitti che sballino le future procedure di classificazione.


ESECUZIONE

Generare i modelli con lo script preprocess.py come indicato nelle documentazione del progetto sent-conv-torch

Per avviare la classificazione su tweet/testi generati in tempo reale avviare lo script GUI.py

Specificare il testo, il task di classificazione e premere "Start classification"
Il programma eseguirà nell'ordine preprocess0.py e main0.py; l'utente dovrà solo attendere la comunicazione della predizione da parte del programma.
