### ALGORITMI DI ASCESA DUALE PER PROBLEMI DI FACILITY LOCATION

#### Contenuti del progetto

1.  Codice sorgente per il software sviluppato
2.  Risultati dei test eseguiti 
    1. Tabelle
    2. Grafici
3.  Materiale per la consegna
    1.  Relazione
    2.  Slides di presentazione
4.  Istanze di test
    1. Istanze di test per UFL/SSCFL
    2. Istanze di test metriche per UFL
 
 
##### Codice sorgente
 
 Per eseguire il progetto è necessaria l'installazione di una release di Python 3.
 Occorre inoltre installare i packages amplpy (API AMPL per Python) e prettytable (libreria usata per il rendering dei risultati dei test in forma tabulare ).
 Per installare i pacchetti di cui sopra è sufficente eseguire da linea di comando :
 
     python -m pip install pip --upgrade 
     python -m pip install amplpy 
     python -m pip install prettytable
 
 Per avviare il software è sufficiente aprire un terminale nella cartella del progetto e eseguire il commando:
    
     python main.py

Un menù interattivo guiderà nella scelta dell’operazione da eseguire, in particolare verrà chiesto

*  Se calcolare la soluzione di problemi UFL o SSCFL
*  Se calcolare la soluzione di una istanza o più istanze, nel secondo caso è necessario fornire il path a una cartella che deve contenere solamente i file di istanza.
*  Se avere in ouput un file in formato .csv e uno in .txt con i risultati dell’esecuzione.
*  Se mostrare i singoli step di esecuzione degli algoritmi.
*  Se calcolare anche la soluzione primale relativa alle esecuzioni di DUALOC e Algoritmo Primale-Duale per l’UFL.

##### Risultati dei test

I risultati dei test sono reperibili nella cartella exam_material/test_results.
Si fa riferimento all'algoritmo DUALOC come definito in [1] pp. 303-305,all'algoritmo di Ascesa Duale semplice come definito in [1] p. 297 e all'algoritmo Primale - Duale come definito in [2] p. 7.

1. Tabelle
    * _metric_ufl_results.txt_ riguarda l'esecuzione del solver AMPL, dell'algoritmo DUALOC e dell'algoritmo Primale - Duale su istanze di tipo metrico per UFL.
    * _primal_metric_ufl_results.txt_ contiene gli stessi dati di _metric_ufl_results.txt_ e in più il valore della soluzione primale calcolata dall'algoritmo DUALOC e dall'algoritmo Primale - Duale
    * _ufl_results.txt_ riguarda l'esecuzione del solver AMPL e dell'algoritmo DUALOC sulle istanze di test per UFL.
    * _primal_ufl_results.txt_ contiene gli stessi dati di _ufl_results.txt_ e in più il valore della soluzione primale calcolata dall'algoritmo DUALOC.
    * _sscfl_results.txt_ riguarda l'esecuzione del solver AMPL e dell'algoritmo DUALOC adattato sulle istanze di test per SSCFL.
    * _ufl_simple_dualoc_results.txt_ riguarda l'esecuzione dell'algoritmo DUALOC e dell'algoritmo di Ascesa Duale semplice sulle istanze di test per UFL.
    
2. Grafici (ottenuti con l'utilizzo del software MATLAB)
    * _metric_ufl_primal_solution_comparison.jpg_ grafico di confronto tra la soluzioni primali di DUALOC (linea BLU) e algoritmo Primale - Duale (linea VERDE) su istanze di tipo metrico per UFL e le soluzioni del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero).
    * _solution_comparison_metric_ufl.jpg_ grafico di confronto tra la soluzioni di DUALOC (linea BLU) e algoritmo Primale - Duale (linea VERDE) su istanze di tipo metrico per UFL le soluzioni del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero).
    * _sscfl_solution_comparison.jpg_ grafico di confronto tra le soluzioni del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero), e dell'algoritmo DUALOC (linea BLU) adattato su istanze di test per SSCFL.
    * _sscfl_time_comparison.jpg_ grafico di confronto tra i tempi di esecuzione del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero), e dell'algoritmo DUALOC adattato (linea BLU) su istanze di test per SSCFL.
    * _ufl_metric_time_comparison.jpg_ grafico di confronto tra i tempi di esecuzione del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero) ,dell'algoritmo DUALOC (linea BLU) ,e dell'algoritmo Primale - Duale (linea VERDE) su istanze di tipo metrico per UFL.
    * _ufl_simple_dualoc_time_comparison.jpg_ grafico di confronto tra i tempi di esecuzione dell'algoritmo DUALOC (linea BLU) e dell'algoritmo di Ascesa Duale semplice (linea ROSSA) su istanze di test per UFL.
    * _ufl_primal_solution_comparison.jpg_ grafico di confronto tra la soluzione del PLI UFL individuata dal solver AMPL (linea ROSSA) e la soluzione primale calcolata dal DUALOC (linea BLU).
    * _ufl_simple_dualoc_solution_comparison.jpg_ grafico di confronto tra le soluzioni dell'algoritmo DUALOC (linea BLU) e dell'algoritmo di Ascesa Duale semplice (linea ROSSA) su istanze di test per UFL.
    * _ufl_solution_comparison.jpg_ grafico di confronto tra le soluzioni del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero) e dell'algoritmo DUALOC (linea BLU) su istanze di test per UFL.
    * _ufl_time_comparison.jpg_ grafico di confronto tra i tempi di esecuzione del solver AMPL (linea GIALLA per il rilassamento e ROSSA per il PL intero)  e dell'algoritmo DUALOC (linea BLU) su istanze di test per UFL.
    * _ufl_instance_comparison.jpg_ grafico di confronto tra la soluzione ottima della formulazione intera (rosso) delle istanze di test per UFL e della soluzione rilassata (Giallo).
    * _sscfl_instance_comparison.jpg_  grafico di confronto tra la soluzione ottima della formulazione intera (rosso) delle istanze di test per SSCFL e della soluzione rilassata (Giallo).
    
##### Materiale per la consegna

Nella cartella exam_material sono presenti una relazione in formato .pdf nella cartella report e le slide di presentazione in formato .pdf nella cartella slides.


##### Istanze di test

1. Istanze di test per UFL sono nella cartella ufl_test_instances ,nel nome del file il primo numero rappresenta il numero di clienti dell'istanza,il secondo il numero di facility.
2. Istanze di test per SSCFL sono nella cartella sscfl_test_instances ,nel nome del file il primo numero rappresenta il numero di facility dell'istanza,il secondo il numero di clienti.
3. Istanze di test metriche per UFL , sono state ottenuto modificando le istanze di test per UFL/SSCFL.Si trovano nella cartella metric_instances, il nome del file segue la stessa regola di cui al punto 1.


###### Riferimenti

1.  A. Sassano, Modelli e algoritmi della ricerca operativa, FrancoAngeli, 1999, Milano, pp. 267 – 308.
2.  A. Gupta,V. Gupta , “Lecture 5: Primal-Dual Algorithms and Facility.Location”, 2008, pp. 1 - 7.
