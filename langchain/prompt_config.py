class Prompt_Config:
    
    def __init__(self, lang):
        self.lang = lang
        if lang == 'it':
            self.set_Italian_config()    
        elif lang == 'es':
            self.set_Spanish_config()
        else:
            self.set_Basque_config()

    

    def set_Italian_config(self):
        self.few_shot_doc_ids = ['101184', '101165', '101180', '100998', '101191']

        self.prompt_prefix = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco un esempio di testo e output:"
        self.prompt_prefix_2 = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco due esempi di testo e output:"

        self.prompt_suffix = """
        Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

        Ora dammi l'output per il seguente testo:

        {Text}

        Stampa solo l'output se presente e nient'altro.
        """

        self.sample_clinical_stmt = "M.d., maschio di 9 anni giunge alla nostra osservazione per episodio di macroematuria terminale, con urine color rosso vivo, preceduto da dolore addominale intermittente nelle due settimane precedenti. Una prima ecografia renale eseguita all’ingresso evidenzia reni di normali dimensioni in assenza di calcoli, vie urinarie non dilatate e vescica a contenuto finemente corpuscolato. Gli accertamenti ematologici ed urinari di primo livello hanno permesso di escludere le più comuni cause di macroematuria del bambino, in particolare la glomerulonefrite post-infettiva, la calcolosi renale e l’infezione urinaria. Dopo 2 giorni, per il persistere della macroematuria, ripetiamo un’ecografia renale che mette in evidenza una “idroureteronefrosi dx con materiale ipoecogeno non vascolarizzato a livello del calice inferiore, della pelvi e del tratto iniziale dell’uretere”, interpretati dal radiologo come possibile coagulo ematico. Tuttavia le ecografie ripetute nei giorni successivi hanno mostrato una sostanziale stabilità del quadro, rendendo poco probabile l’ipotesi formulata. Il riscontro di una ipereosinofilia periferica (e 1200/mmc) ci ha fatto ipotizzare una infezione da schistosoma, che raramente può causare nel bambino lesioni polipoidi sanguinanti di pelvi ed uretere; tuttavia la ricerca del parassita nelle urine è risultata negativa. Decidiamo quindi di eseguire una uro-angio-RM che ha permesso di evidenziare a livello della regione papillare del calice inferiore dx una formazione rotondeggiante del diametro di 15 mm ampiamente protrudente nel calice inferiore, con spiccata impregnazione di mdc. L’agobiopsia percutanea ecoguidata e la successiva nefrectomia hanno permesso di porre diagnosi di rabdomiosarcoma embrionale, variante botrioide. La massa neoplastica ha dimensioni di 5x2.5 cm, il restante parenchima renale, il tessuto adiposo ed i linfonodi sono indenni da neoplasia. Gli accertamenti strumentali e le biopsie ossee sono risultati negativi per localizzazioni secondarie di malattia."

        self.one_shot_prompt_sans_new_text = """
        Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco un esempio di testo e output:

        B.M., bambino caucasico di 11 mesi, giunto all’osservazione nel febbraio 2011 per porpora di n.d.d. e febbre (38,5°C) da 3 giorni. Secondogenito di famiglia con basso livello socio-economico e con anamnesi remota e familiare negativa per patologie degne di nota. All’esame obiettivo stato di abbattimento, cute pallida, presenza di petecchie diffuse al tronco, iperemia intensa del faringe e rinite sierosa. Gli esami eseguiti mostravano lieve leucocitosi (12,03 x 103 / mm3), lieve linfocitosi relativa (57%), lieve trombocitosi (538 x 103 / mm3) divenuta moderata durante il ricovero (826 x 103 / mm3), VES mossa (19 mm/sedim; v.n.<10), anticorpi IgG anti-Epstein Barr Virus positivi (VCAIgG> 750 U/ml; negativi i VCA-IgM e gli EBNA-IgG), EBV-DNA positivo in saliva (20,4x106 copie/ml) e negativo nel sangue, moderata leucocituria (500 leucociti/ micrl); nella norma PT e PTT, PCR, indici epato-renali, tampone faringeo, urinocoltura e altre ricerche virologiche. L’esame morfologico del sangue periferico confermava la trombocitosi, senza altre alterazioni degne di nota. Alla dimissione sono stati programmati controlli post-ricovero per la persistenza di trombocitosi (PLT: 735 x 103 / mm3). All’età di 16 mesi, nuovo ricovero per febbre (39°C) e stato di abbattimento. All’EO cute pallida, faringe iperemico, fegato e milza palpabili a 2 cm dall’arco costale, edema periorbitario sinistro e ferita lacero-contusa suppurata in regione frontale, suturata 5 giorni prima in PSP, ove erano stati adottati, tuttavia, gli adeguati protocolli comuni (sutura in ambiente sterile e terapia antibiotica domiciliare con amoxicillina-ac.clavulanico). Dagli esami risultava moderata leucocitosi (32,28 x 103 / mm3), neutrofilia (62,9%), moderata trombocitosi (732 x 103 / mm3), indici di flogosi aumentati (VES: 36 mm/sedim, PCR: 6,26 mg/dl) ed incremento delle GOT (66 UI/dl); nella norma gli altri indici epato-renali, immunoglobuline e sottopopolazioni linfocitarie. L’esame colturale della ferita risultava positivo per Staphilococcus epidermidis, resistente ad amoxicillina-ac.clavulanico e sensibile alle cefalosporine. Gli esami virologici indicavano positività dell’EBV-DNA sia in saliva (1,83x106copie/ml) che nel sangue (6,72x103copie/ml). Le condizioni cliniche del bambino miglioravano prontamente dopo adeguato courettage della FLC e terapia antibiotica con ceftriaxone. Alla dimissione persisteva, tuttavia, moderata trombocitosi (806 x 103 / mm3). Dopo 20 giorni al controllo post-ricovero il bambino presentava gastroenterite acuta (con Rotavirus positivo nelle feci) e persistente trombocitosi (794 x 103 / mm3). Dopo 2 mesi circa, in seguito a nuovo accesso al Pronto Soccorso Pediatrico per gastro-enterite, gli esami ematici evidenziavano il protrarsi della trombocitosi (727 x 103 / mm3), rilevata anche a distanza di circa 1 mese in occasione di controllo in regime di Day-Hospital (PLT: 679 x 103 / mm3; Ab IgG anti-EBV ed EBNA positivi; EBV-DNA positivo in saliva ed urine).

        Output : 

        38,5°C | febbre
        12,03 x 103 / mm3 | leucocitosi
        57% | linfocitosi
        538 x 103 / mm3 | trombocitosi
        19 mm/sedim | VES
        positivi | anticorpi
        > 750 U/ml | VCAIgG
        negativi | EBNA-IgG
        negativi | VCA-IgM
        positivo | EBV-DNA
        20,4x106 copie/ml | EBV-DNA
        negativo | EBV-DNA
        500 leucociti/ micrl | leucocituria
        nella norma | urinocoltura
        nella norma | PCR
        nella norma | indici
        nella norma | ricerche
        nella norma | PTT
        nella norma | tampone
        nella norma | PT
        735 x 103 / mm3 | PLT
        39°C | febbre
        32,28 x 103 / mm3 | leucocitosi
        62,9% | neutrofilia
        732 x 103 / mm3 | trombocitosi
        36 mm/sedim | VES
        6,26 mg/dl | PCR
        66 UI/dl | GOT
        nella norma | immunoglobuline
        nella norma | sottopopolazioni
        nella norma | indici
        positivo | esame
        positivo | Staphilococcus
        positività | EBV-DNA
        1,83x106copie/ml | EBV-DNA
        6,72x103copie/ml | EBV-DNA
        806 x 103 / mm3 | trombocitosi
        positivo | Rotavirus
        794 x 103 / mm3 | trombocitosi
        727 x 103 / mm3 | trombocitosi
        679 x 103 / mm3 | PLT
        positivi | anti-EBV
        positivi | EBNA
        positivo | EBV-DNA

        Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

        Ora dammi l'output per il seguente testo:

        {Text}

        Stampa solo l'output se presente e nient'altro.
        """


        self.examples = [
          {
            "Testo": "B.M., bambino caucasico di 11 mesi, giunto all’osservazione nel febbraio 2011 per porpora di n.d.d. e febbre (38,5°C) da 3 giorni. Secondogenito di famiglia con basso livello socio-economico e con anamnesi remota e familiare negativa per patologie degne di nota. All’esame obiettivo stato di abbattimento, cute pallida, presenza di petecchie diffuse al tronco, iperemia intensa del faringe e rinite sierosa. Gli esami eseguiti mostravano lieve leucocitosi (12,03 x 103 / mm3), lieve linfocitosi relativa (57%), lieve trombocitosi (538 x 103 / mm3) divenuta moderata durante il ricovero (826 x 103 / mm3), VES mossa (19 mm/sedim; v.n.<10), anticorpi IgG anti-Epstein Barr Virus positivi (VCAIgG> 750 U/ml; negativi i VCA-IgM e gli EBNA-IgG), EBV-DNA positivo in saliva (20,4x106 copie/ml) e negativo nel sangue, moderata leucocituria (500 leucociti/ micrl); nella norma PT e PTT, PCR, indici epato-renali, tampone faringeo, urinocoltura e altre ricerche virologiche. L’esame morfologico del sangue periferico confermava la trombocitosi, senza altre alterazioni degne di nota. Alla dimissione sono stati programmati controlli post-ricovero per la persistenza di trombocitosi (PLT: 735 x 103 / mm3). All’età di 16 mesi, nuovo ricovero per febbre (39°C) e stato di abbattimento. All’EO cute pallida, faringe iperemico, fegato e milza palpabili a 2 cm dall’arco costale, edema periorbitario sinistro e ferita lacero-contusa suppurata in regione frontale, suturata 5 giorni prima in PSP, ove erano stati adottati, tuttavia, gli adeguati protocolli comuni (sutura in ambiente sterile e terapia antibiotica domiciliare con amoxicillina-ac.clavulanico). Dagli esami risultava moderata leucocitosi (32,28 x 103 / mm3), neutrofilia (62,9%), moderata trombocitosi (732 x 103 / mm3), indici di flogosi aumentati (VES: 36 mm/sedim, PCR: 6,26 mg/dl) ed incremento delle GOT (66 UI/dl); nella norma gli altri indici epato-renali, immunoglobuline e sottopopolazioni linfocitarie. L’esame colturale della ferita risultava positivo per Staphilococcus epidermidis, resistente ad amoxicillina-ac.clavulanico e sensibile alle cefalosporine. Gli esami virologici indicavano positività dell’EBV-DNA sia in saliva (1,83x106copie/ml) che nel sangue (6,72x103copie/ml). Le condizioni cliniche del bambino miglioravano prontamente dopo adeguato courettage della FLC e terapia antibiotica con ceftriaxone. Alla dimissione persisteva, tuttavia, moderata trombocitosi (806 x 103 / mm3). Dopo 20 giorni al controllo post-ricovero il bambino presentava gastroenterite acuta (con Rotavirus positivo nelle feci) e persistente trombocitosi (794 x 103 / mm3). Dopo 2 mesi circa, in seguito a nuovo accesso al Pronto Soccorso Pediatrico per gastro-enterite, gli esami ematici evidenziavano il protrarsi della trombocitosi (727 x 103 / mm3), rilevata anche a distanza di circa 1 mese in occasione di controllo in regime di Day-Hospital (PLT: 679 x 103 / mm3; Ab IgG anti-EBV ed EBNA positivi; EBV-DNA positivo in saliva ed urine).",
            "Output": 
        """
        38,5°C | febbre
        12,03 x 103 / mm3 | leucocitosi
        57% | linfocitosi
        538 x 103 / mm3 | trombocitosi
        19 mm/sedim | VES
        positivi | anticorpi
        > 750 U/ml | VCAIgG
        negativi | EBNA-IgG
        negativi | VCA-IgM
        positivo | EBV-DNA
        20,4x106 copie/ml | EBV-DNA
        negativo | EBV-DNA
        500 leucociti/ micrl | leucocituria
        nella norma | urinocoltura
        nella norma | PCR
        nella norma | indici
        nella norma | ricerche
        nella norma | PTT
        nella norma | tampone
        nella norma | PT
        735 x 103 / mm3 | PLT
        39°C | febbre
        32,28 x 103 / mm3 | leucocitosi
        62,9% | neutrofilia
        732 x 103 / mm3 | trombocitosi
        36 mm/sedim | VES
        6,26 mg/dl | PCR
        66 UI/dl | GOT
        nella norma | immunoglobuline
        nella norma | sottopopolazioni
        nella norma | indici
        positivo | esame
        positivo | Staphilococcus
        positività | EBV-DNA
        1,83x106copie/ml | EBV-DNA
        6,72x103copie/ml | EBV-DNA
        806 x 103 / mm3 | trombocitosi
        positivo | Rotavirus
        794 x 103 / mm3 | trombocitosi
        727 x 103 / mm3 | trombocitosi
        679 x 103 / mm3 | PLT
        positivi | anti-EBV
        positivi | EBNA
        positivo | EBV-DNA
        """
          },
          {
            "Testo": "Riportiamo il caso clinico di una bambina di 4 anni di origine pakistana, figlia di genitori consanguinei (cugini di primo grado). Nata a termine da parto eutocico in gravidanza normodecorsa, ha presentato sofferenza perinatale (apgar ad 1 minuto: 3) e ha necessitato di intubazione orotracheale. In prima giornata di vita riscontro di grave anemia emolitica e moderata piastrinopenia (Hb 7,8 g/dl, Ptl 76 x 109/l, ldH 14501u/l, CPK 778 u/l e ast 429 u/l) per cui la paziente è stata sottoposta a trasfusione di emazie concentrate e piastrine. In seconda giornata di vita grave ittero a bilirubina indiretta (bilirubina totale massima 21,7 mg/dl) che ha richiesto exanguinotrasfusione con rapido miglioramento clinico e normalizzazione degli indici di emolisi. La paziente è stata estubata in terza giornata di vita e non ha presentato ulteriori complicanze respiratorie. Dimessa in benessere a 2 settimane di vita con buona crasi ematica (Hb 11,8 g/dl, MCv 79,2 fl, Ptl 276000/mmc), la famiglia non si è presentata ai successivi controlli programmati per ulteriori approfondimenti e ha soggiornato per diversi mesi in Pakistan. A 45 mesi di vita per comparsa di grave anemia emolitica in corso di febbre (Hb 6,4 g/dl, MCv 81,8 fl, reticolociti 50,9 x 104/μl, ldH 3250u/l, bilirubina totale 2,90 mg/dl, bilirubina indiretta 2 mg/dl) e modesta splenomegalia (milza palpabile a 2 cm dall’arcata costale) la paziente ha effettuato nuova emotrasfusione. I test di Coombs diretto e indiretto sono risultati negativi; la morfologia eritrocitaria e il tracciato cromatografico hanno evidenziato un quadro suggestivo per emoglobinopatia da Hb H, senza evidenza di emoglobine patologiche. Il dosaggio dell’attività del G6PdH, lo studio delle resistenze osmotiche, il test di lisi al glicerolo ed il Pink test, oltre alle sierologie virali (Citmomegalovirus, epstain barr virus, Parvovirus) e alla ricerca del parassita malarico, sono risultati negativi. Si riscontrava una crescita staturo-ponderale al 3° percentile, regolare lungo la curva di crescita. A distanza di 2 mesi da tale evento, la bambina ha presentato sempre in corso di febbre (tampone nasofaringeo positivo per influenza b) un nuovo episodio di emolisi (Hb 6,0 g/dl, MCv 78,4 fl, reticolociti 12% ldH 1888 u/l) che ha necessitato nuovamente di trasfusione di emazie concentrate per lo scadimento delle condizioni generali. L’analisi molecolare dei geni delle catene emoglobiniche ha evidenziato omozigosi per l’emoglobina sallanches. La bambina si presenta attualmente in buone condizioni generali, con obiettività generale negativa eccetto per polo splenico palpabile a circa 1 cm dall’arcata costale. è seguita con cadenza mensile, salvo comparsa di sintomatologia. Si valuterà nei prossimi mesi l’eventuale necessità di un regime trasfusionale cronico in base all’andamento della malattia (all’ultimo emocromo Hb 8,2 g/dl, MCv 77,7 fl, reticolociti 57,85 x 104/μl). Assume terapia di supporto con acido folico e profilassi antibiotica con amoxicillina orale per ridurre gli eventi infettivi. Adeguate raccomandazioni per evitare alimenti o farmaci e sostanze pro-ossidanti sono state fornite alla famiglia. Risultano tuttora in corso accertamenti dei familiari per una corretta consulenza genetica.",
            "Output": 
        """
        3 | apgar
        7,8 g/dl | Hb
        76 x 109/l | Ptl
        14501u/l | ldH
        778 u/l | CPK
        429 u/l | ast
        21,7 mg/dl | bilirubina
        11,8 g/dl | Hb
        79,2 fl | MCv
        276000/mmc | Ptl
        6,4 g/dl | Hb
        81,8 fl | MCv
        50,9 x 104/μl | reticolociti
        3250u/l | ldH
        2,90 mg/dl | bilirubina
        2 mg/dl | bilirubina
        negativi | Coombs
        negativi | Pink
        negativi | studio
        negativi | sierologie
        negativi | dosaggio
        negativi | ricerca
        negativi | test
        al 3° percentile | crescita
        positivo | influenza
        positivo | tampone
        6,0 g/dl | Hb
        78,4 fl | MCv
        12% | reticolociti
        1888 u/l | ldH
        negativa | obiettività
        8,2 g/dl | Hb
        77,7 fl | MCv
        57,85 x 104/μl | reticolociti
        """
          },
        ]

    def set_Spanish_config(self):
        self.few_shot_doc_ids = ['101184', '101165', '101180', '100998', '101191']

        self.prompt_prefix = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco un esempio di testo e output:"
        self.prompt_prefix_2 = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco due esempi di testo e output:"

        self.prompt_suffix = """
        Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

        Ora dammi l'output per il seguente testo:

        {Text}

        Stampa solo l'output se presente e nient'altro.
        """

        self.sample_it_clinical_stmt = "M.d., maschio di 9 anni giunge alla nostra osservazione per episodio di macroematuria terminale, con urine color rosso vivo, preceduto da dolore addominale intermittente nelle due settimane precedenti. Una prima ecografia renale eseguita all’ingresso evidenzia reni di normali dimensioni in assenza di calcoli, vie urinarie non dilatate e vescica a contenuto finemente corpuscolato. Gli accertamenti ematologici ed urinari di primo livello hanno permesso di escludere le più comuni cause di macroematuria del bambino, in particolare la glomerulonefrite post-infettiva, la calcolosi renale e l’infezione urinaria. Dopo 2 giorni, per il persistere della macroematuria, ripetiamo un’ecografia renale che mette in evidenza una “idroureteronefrosi dx con materiale ipoecogeno non vascolarizzato a livello del calice inferiore, della pelvi e del tratto iniziale dell’uretere”, interpretati dal radiologo come possibile coagulo ematico. Tuttavia le ecografie ripetute nei giorni successivi hanno mostrato una sostanziale stabilità del quadro, rendendo poco probabile l’ipotesi formulata. Il riscontro di una ipereosinofilia periferica (e 1200/mmc) ci ha fatto ipotizzare una infezione da schistosoma, che raramente può causare nel bambino lesioni polipoidi sanguinanti di pelvi ed uretere; tuttavia la ricerca del parassita nelle urine è risultata negativa. Decidiamo quindi di eseguire una uro-angio-RM che ha permesso di evidenziare a livello della regione papillare del calice inferiore dx una formazione rotondeggiante del diametro di 15 mm ampiamente protrudente nel calice inferiore, con spiccata impregnazione di mdc. L’agobiopsia percutanea ecoguidata e la successiva nefrectomia hanno permesso di porre diagnosi di rabdomiosarcoma embrionale, variante botrioide. La massa neoplastica ha dimensioni di 5x2.5 cm, il restante parenchima renale, il tessuto adiposo ed i linfonodi sono indenni da neoplasia. Gli accertamenti strumentali e le biopsie ossee sono risultati negativi per localizzazioni secondarie di malattia."

        self.one_shot_prompt_sans_new_text = """
        Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco un esempio di testo e output:

        B.M., bambino caucasico di 11 mesi, giunto all’osservazione nel febbraio 2011 per porpora di n.d.d. e febbre (38,5°C) da 3 giorni. Secondogenito di famiglia con basso livello socio-economico e con anamnesi remota e familiare negativa per patologie degne di nota. All’esame obiettivo stato di abbattimento, cute pallida, presenza di petecchie diffuse al tronco, iperemia intensa del faringe e rinite sierosa. Gli esami eseguiti mostravano lieve leucocitosi (12,03 x 103 / mm3), lieve linfocitosi relativa (57%), lieve trombocitosi (538 x 103 / mm3) divenuta moderata durante il ricovero (826 x 103 / mm3), VES mossa (19 mm/sedim; v.n.<10), anticorpi IgG anti-Epstein Barr Virus positivi (VCAIgG> 750 U/ml; negativi i VCA-IgM e gli EBNA-IgG), EBV-DNA positivo in saliva (20,4x106 copie/ml) e negativo nel sangue, moderata leucocituria (500 leucociti/ micrl); nella norma PT e PTT, PCR, indici epato-renali, tampone faringeo, urinocoltura e altre ricerche virologiche. L’esame morfologico del sangue periferico confermava la trombocitosi, senza altre alterazioni degne di nota. Alla dimissione sono stati programmati controlli post-ricovero per la persistenza di trombocitosi (PLT: 735 x 103 / mm3). All’età di 16 mesi, nuovo ricovero per febbre (39°C) e stato di abbattimento. All’EO cute pallida, faringe iperemico, fegato e milza palpabili a 2 cm dall’arco costale, edema periorbitario sinistro e ferita lacero-contusa suppurata in regione frontale, suturata 5 giorni prima in PSP, ove erano stati adottati, tuttavia, gli adeguati protocolli comuni (sutura in ambiente sterile e terapia antibiotica domiciliare con amoxicillina-ac.clavulanico). Dagli esami risultava moderata leucocitosi (32,28 x 103 / mm3), neutrofilia (62,9%), moderata trombocitosi (732 x 103 / mm3), indici di flogosi aumentati (VES: 36 mm/sedim, PCR: 6,26 mg/dl) ed incremento delle GOT (66 UI/dl); nella norma gli altri indici epato-renali, immunoglobuline e sottopopolazioni linfocitarie. L’esame colturale della ferita risultava positivo per Staphilococcus epidermidis, resistente ad amoxicillina-ac.clavulanico e sensibile alle cefalosporine. Gli esami virologici indicavano positività dell’EBV-DNA sia in saliva (1,83x106copie/ml) che nel sangue (6,72x103copie/ml). Le condizioni cliniche del bambino miglioravano prontamente dopo adeguato courettage della FLC e terapia antibiotica con ceftriaxone. Alla dimissione persisteva, tuttavia, moderata trombocitosi (806 x 103 / mm3). Dopo 20 giorni al controllo post-ricovero il bambino presentava gastroenterite acuta (con Rotavirus positivo nelle feci) e persistente trombocitosi (794 x 103 / mm3). Dopo 2 mesi circa, in seguito a nuovo accesso al Pronto Soccorso Pediatrico per gastro-enterite, gli esami ematici evidenziavano il protrarsi della trombocitosi (727 x 103 / mm3), rilevata anche a distanza di circa 1 mese in occasione di controllo in regime di Day-Hospital (PLT: 679 x 103 / mm3; Ab IgG anti-EBV ed EBNA positivi; EBV-DNA positivo in saliva ed urine).

        Output : 

        38,5°C | febbre
        12,03 x 103 / mm3 | leucocitosi
        57% | linfocitosi
        538 x 103 / mm3 | trombocitosi
        19 mm/sedim | VES
        positivi | anticorpi
        > 750 U/ml | VCAIgG
        negativi | EBNA-IgG
        negativi | VCA-IgM
        positivo | EBV-DNA
        20,4x106 copie/ml | EBV-DNA
        negativo | EBV-DNA
        500 leucociti/ micrl | leucocituria
        nella norma | urinocoltura
        nella norma | PCR
        nella norma | indici
        nella norma | ricerche
        nella norma | PTT
        nella norma | tampone
        nella norma | PT
        735 x 103 / mm3 | PLT
        39°C | febbre
        32,28 x 103 / mm3 | leucocitosi
        62,9% | neutrofilia
        732 x 103 / mm3 | trombocitosi
        36 mm/sedim | VES
        6,26 mg/dl | PCR
        66 UI/dl | GOT
        nella norma | immunoglobuline
        nella norma | sottopopolazioni
        nella norma | indici
        positivo | esame
        positivo | Staphilococcus
        positività | EBV-DNA
        1,83x106copie/ml | EBV-DNA
        6,72x103copie/ml | EBV-DNA
        806 x 103 / mm3 | trombocitosi
        positivo | Rotavirus
        794 x 103 / mm3 | trombocitosi
        727 x 103 / mm3 | trombocitosi
        679 x 103 / mm3 | PLT
        positivi | anti-EBV
        positivi | EBNA
        positivo | EBV-DNA

        Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

        Ora dammi l'output per il seguente testo:

        {Text}

        Stampa solo l'output se presente e nient'altro.
        """


        self.examples = [
          {
            "Testo": "B.M., bambino caucasico di 11 mesi, giunto all’osservazione nel febbraio 2011 per porpora di n.d.d. e febbre (38,5°C) da 3 giorni. Secondogenito di famiglia con basso livello socio-economico e con anamnesi remota e familiare negativa per patologie degne di nota. All’esame obiettivo stato di abbattimento, cute pallida, presenza di petecchie diffuse al tronco, iperemia intensa del faringe e rinite sierosa. Gli esami eseguiti mostravano lieve leucocitosi (12,03 x 103 / mm3), lieve linfocitosi relativa (57%), lieve trombocitosi (538 x 103 / mm3) divenuta moderata durante il ricovero (826 x 103 / mm3), VES mossa (19 mm/sedim; v.n.<10), anticorpi IgG anti-Epstein Barr Virus positivi (VCAIgG> 750 U/ml; negativi i VCA-IgM e gli EBNA-IgG), EBV-DNA positivo in saliva (20,4x106 copie/ml) e negativo nel sangue, moderata leucocituria (500 leucociti/ micrl); nella norma PT e PTT, PCR, indici epato-renali, tampone faringeo, urinocoltura e altre ricerche virologiche. L’esame morfologico del sangue periferico confermava la trombocitosi, senza altre alterazioni degne di nota. Alla dimissione sono stati programmati controlli post-ricovero per la persistenza di trombocitosi (PLT: 735 x 103 / mm3). All’età di 16 mesi, nuovo ricovero per febbre (39°C) e stato di abbattimento. All’EO cute pallida, faringe iperemico, fegato e milza palpabili a 2 cm dall’arco costale, edema periorbitario sinistro e ferita lacero-contusa suppurata in regione frontale, suturata 5 giorni prima in PSP, ove erano stati adottati, tuttavia, gli adeguati protocolli comuni (sutura in ambiente sterile e terapia antibiotica domiciliare con amoxicillina-ac.clavulanico). Dagli esami risultava moderata leucocitosi (32,28 x 103 / mm3), neutrofilia (62,9%), moderata trombocitosi (732 x 103 / mm3), indici di flogosi aumentati (VES: 36 mm/sedim, PCR: 6,26 mg/dl) ed incremento delle GOT (66 UI/dl); nella norma gli altri indici epato-renali, immunoglobuline e sottopopolazioni linfocitarie. L’esame colturale della ferita risultava positivo per Staphilococcus epidermidis, resistente ad amoxicillina-ac.clavulanico e sensibile alle cefalosporine. Gli esami virologici indicavano positività dell’EBV-DNA sia in saliva (1,83x106copie/ml) che nel sangue (6,72x103copie/ml). Le condizioni cliniche del bambino miglioravano prontamente dopo adeguato courettage della FLC e terapia antibiotica con ceftriaxone. Alla dimissione persisteva, tuttavia, moderata trombocitosi (806 x 103 / mm3). Dopo 20 giorni al controllo post-ricovero il bambino presentava gastroenterite acuta (con Rotavirus positivo nelle feci) e persistente trombocitosi (794 x 103 / mm3). Dopo 2 mesi circa, in seguito a nuovo accesso al Pronto Soccorso Pediatrico per gastro-enterite, gli esami ematici evidenziavano il protrarsi della trombocitosi (727 x 103 / mm3), rilevata anche a distanza di circa 1 mese in occasione di controllo in regime di Day-Hospital (PLT: 679 x 103 / mm3; Ab IgG anti-EBV ed EBNA positivi; EBV-DNA positivo in saliva ed urine).",
            "Output": 
        """
        38,5°C | febbre
        12,03 x 103 / mm3 | leucocitosi
        57% | linfocitosi
        538 x 103 / mm3 | trombocitosi
        19 mm/sedim | VES
        positivi | anticorpi
        > 750 U/ml | VCAIgG
        negativi | EBNA-IgG
        negativi | VCA-IgM
        positivo | EBV-DNA
        20,4x106 copie/ml | EBV-DNA
        negativo | EBV-DNA
        500 leucociti/ micrl | leucocituria
        nella norma | urinocoltura
        nella norma | PCR
        nella norma | indici
        nella norma | ricerche
        nella norma | PTT
        nella norma | tampone
        nella norma | PT
        735 x 103 / mm3 | PLT
        39°C | febbre
        32,28 x 103 / mm3 | leucocitosi
        62,9% | neutrofilia
        732 x 103 / mm3 | trombocitosi
        36 mm/sedim | VES
        6,26 mg/dl | PCR
        66 UI/dl | GOT
        nella norma | immunoglobuline
        nella norma | sottopopolazioni
        nella norma | indici
        positivo | esame
        positivo | Staphilococcus
        positività | EBV-DNA
        1,83x106copie/ml | EBV-DNA
        6,72x103copie/ml | EBV-DNA
        806 x 103 / mm3 | trombocitosi
        positivo | Rotavirus
        794 x 103 / mm3 | trombocitosi
        727 x 103 / mm3 | trombocitosi
        679 x 103 / mm3 | PLT
        positivi | anti-EBV
        positivi | EBNA
        positivo | EBV-DNA
        """
          },
          {
            "Testo": "Riportiamo il caso clinico di una bambina di 4 anni di origine pakistana, figlia di genitori consanguinei (cugini di primo grado). Nata a termine da parto eutocico in gravidanza normodecorsa, ha presentato sofferenza perinatale (apgar ad 1 minuto: 3) e ha necessitato di intubazione orotracheale. In prima giornata di vita riscontro di grave anemia emolitica e moderata piastrinopenia (Hb 7,8 g/dl, Ptl 76 x 109/l, ldH 14501u/l, CPK 778 u/l e ast 429 u/l) per cui la paziente è stata sottoposta a trasfusione di emazie concentrate e piastrine. In seconda giornata di vita grave ittero a bilirubina indiretta (bilirubina totale massima 21,7 mg/dl) che ha richiesto exanguinotrasfusione con rapido miglioramento clinico e normalizzazione degli indici di emolisi. La paziente è stata estubata in terza giornata di vita e non ha presentato ulteriori complicanze respiratorie. Dimessa in benessere a 2 settimane di vita con buona crasi ematica (Hb 11,8 g/dl, MCv 79,2 fl, Ptl 276000/mmc), la famiglia non si è presentata ai successivi controlli programmati per ulteriori approfondimenti e ha soggiornato per diversi mesi in Pakistan. A 45 mesi di vita per comparsa di grave anemia emolitica in corso di febbre (Hb 6,4 g/dl, MCv 81,8 fl, reticolociti 50,9 x 104/μl, ldH 3250u/l, bilirubina totale 2,90 mg/dl, bilirubina indiretta 2 mg/dl) e modesta splenomegalia (milza palpabile a 2 cm dall’arcata costale) la paziente ha effettuato nuova emotrasfusione. I test di Coombs diretto e indiretto sono risultati negativi; la morfologia eritrocitaria e il tracciato cromatografico hanno evidenziato un quadro suggestivo per emoglobinopatia da Hb H, senza evidenza di emoglobine patologiche. Il dosaggio dell’attività del G6PdH, lo studio delle resistenze osmotiche, il test di lisi al glicerolo ed il Pink test, oltre alle sierologie virali (Citmomegalovirus, epstain barr virus, Parvovirus) e alla ricerca del parassita malarico, sono risultati negativi. Si riscontrava una crescita staturo-ponderale al 3° percentile, regolare lungo la curva di crescita. A distanza di 2 mesi da tale evento, la bambina ha presentato sempre in corso di febbre (tampone nasofaringeo positivo per influenza b) un nuovo episodio di emolisi (Hb 6,0 g/dl, MCv 78,4 fl, reticolociti 12% ldH 1888 u/l) che ha necessitato nuovamente di trasfusione di emazie concentrate per lo scadimento delle condizioni generali. L’analisi molecolare dei geni delle catene emoglobiniche ha evidenziato omozigosi per l’emoglobina sallanches. La bambina si presenta attualmente in buone condizioni generali, con obiettività generale negativa eccetto per polo splenico palpabile a circa 1 cm dall’arcata costale. è seguita con cadenza mensile, salvo comparsa di sintomatologia. Si valuterà nei prossimi mesi l’eventuale necessità di un regime trasfusionale cronico in base all’andamento della malattia (all’ultimo emocromo Hb 8,2 g/dl, MCv 77,7 fl, reticolociti 57,85 x 104/μl). Assume terapia di supporto con acido folico e profilassi antibiotica con amoxicillina orale per ridurre gli eventi infettivi. Adeguate raccomandazioni per evitare alimenti o farmaci e sostanze pro-ossidanti sono state fornite alla famiglia. Risultano tuttora in corso accertamenti dei familiari per una corretta consulenza genetica.",
            "Output": 
        """
        3 | apgar
        7,8 g/dl | Hb
        76 x 109/l | Ptl
        14501u/l | ldH
        778 u/l | CPK
        429 u/l | ast
        21,7 mg/dl | bilirubina
        11,8 g/dl | Hb
        79,2 fl | MCv
        276000/mmc | Ptl
        6,4 g/dl | Hb
        81,8 fl | MCv
        50,9 x 104/μl | reticolociti
        3250u/l | ldH
        2,90 mg/dl | bilirubina
        2 mg/dl | bilirubina
        negativi | Coombs
        negativi | Pink
        negativi | studio
        negativi | sierologie
        negativi | dosaggio
        negativi | ricerca
        negativi | test
        al 3° percentile | crescita
        positivo | influenza
        positivo | tampone
        6,0 g/dl | Hb
        78,4 fl | MCv
        12% | reticolociti
        1888 u/l | ldH
        negativa | obiettività
        8,2 g/dl | Hb
        77,7 fl | MCv
        57,85 x 104/μl | reticolociti
        """
          },
        ]

    def set_Basque_config(self):
      self.few_shot_doc_ids = ['101184', '101165', '101180', '100998', '101191']

      self.prompt_prefix = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco un esempio di testo e output:"
      self.prompt_prefix_2 = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco due esempi di testo e output:"

      self.prompt_suffix = """
      Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

      Ora dammi l'output per il seguente testo:

      {Text}

      Stampa solo l'output se presente e nient'altro.
      """

      self.sample_it_clinical_stmt = "M.d., maschio di 9 anni giunge alla nostra osservazione per episodio di macroematuria terminale, con urine color rosso vivo, preceduto da dolore addominale intermittente nelle due settimane precedenti. Una prima ecografia renale eseguita all’ingresso evidenzia reni di normali dimensioni in assenza di calcoli, vie urinarie non dilatate e vescica a contenuto finemente corpuscolato. Gli accertamenti ematologici ed urinari di primo livello hanno permesso di escludere le più comuni cause di macroematuria del bambino, in particolare la glomerulonefrite post-infettiva, la calcolosi renale e l’infezione urinaria. Dopo 2 giorni, per il persistere della macroematuria, ripetiamo un’ecografia renale che mette in evidenza una “idroureteronefrosi dx con materiale ipoecogeno non vascolarizzato a livello del calice inferiore, della pelvi e del tratto iniziale dell’uretere”, interpretati dal radiologo come possibile coagulo ematico. Tuttavia le ecografie ripetute nei giorni successivi hanno mostrato una sostanziale stabilità del quadro, rendendo poco probabile l’ipotesi formulata. Il riscontro di una ipereosinofilia periferica (e 1200/mmc) ci ha fatto ipotizzare una infezione da schistosoma, che raramente può causare nel bambino lesioni polipoidi sanguinanti di pelvi ed uretere; tuttavia la ricerca del parassita nelle urine è risultata negativa. Decidiamo quindi di eseguire una uro-angio-RM che ha permesso di evidenziare a livello della regione papillare del calice inferiore dx una formazione rotondeggiante del diametro di 15 mm ampiamente protrudente nel calice inferiore, con spiccata impregnazione di mdc. L’agobiopsia percutanea ecoguidata e la successiva nefrectomia hanno permesso di porre diagnosi di rabdomiosarcoma embrionale, variante botrioide. La massa neoplastica ha dimensioni di 5x2.5 cm, il restante parenchima renale, il tessuto adiposo ed i linfonodi sono indenni da neoplasia. Gli accertamenti strumentali e le biopsie ossee sono risultati negativi per localizzazioni secondarie di malattia."

      self.one_shot_prompt_sans_new_text = """
      Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco un esempio di testo e output:

      B.M., bambino caucasico di 11 mesi, giunto all’osservazione nel febbraio 2011 per porpora di n.d.d. e febbre (38,5°C) da 3 giorni. Secondogenito di famiglia con basso livello socio-economico e con anamnesi remota e familiare negativa per patologie degne di nota. All’esame obiettivo stato di abbattimento, cute pallida, presenza di petecchie diffuse al tronco, iperemia intensa del faringe e rinite sierosa. Gli esami eseguiti mostravano lieve leucocitosi (12,03 x 103 / mm3), lieve linfocitosi relativa (57%), lieve trombocitosi (538 x 103 / mm3) divenuta moderata durante il ricovero (826 x 103 / mm3), VES mossa (19 mm/sedim; v.n.<10), anticorpi IgG anti-Epstein Barr Virus positivi (VCAIgG> 750 U/ml; negativi i VCA-IgM e gli EBNA-IgG), EBV-DNA positivo in saliva (20,4x106 copie/ml) e negativo nel sangue, moderata leucocituria (500 leucociti/ micrl); nella norma PT e PTT, PCR, indici epato-renali, tampone faringeo, urinocoltura e altre ricerche virologiche. L’esame morfologico del sangue periferico confermava la trombocitosi, senza altre alterazioni degne di nota. Alla dimissione sono stati programmati controlli post-ricovero per la persistenza di trombocitosi (PLT: 735 x 103 / mm3). All’età di 16 mesi, nuovo ricovero per febbre (39°C) e stato di abbattimento. All’EO cute pallida, faringe iperemico, fegato e milza palpabili a 2 cm dall’arco costale, edema periorbitario sinistro e ferita lacero-contusa suppurata in regione frontale, suturata 5 giorni prima in PSP, ove erano stati adottati, tuttavia, gli adeguati protocolli comuni (sutura in ambiente sterile e terapia antibiotica domiciliare con amoxicillina-ac.clavulanico). Dagli esami risultava moderata leucocitosi (32,28 x 103 / mm3), neutrofilia (62,9%), moderata trombocitosi (732 x 103 / mm3), indici di flogosi aumentati (VES: 36 mm/sedim, PCR: 6,26 mg/dl) ed incremento delle GOT (66 UI/dl); nella norma gli altri indici epato-renali, immunoglobuline e sottopopolazioni linfocitarie. L’esame colturale della ferita risultava positivo per Staphilococcus epidermidis, resistente ad amoxicillina-ac.clavulanico e sensibile alle cefalosporine. Gli esami virologici indicavano positività dell’EBV-DNA sia in saliva (1,83x106copie/ml) che nel sangue (6,72x103copie/ml). Le condizioni cliniche del bambino miglioravano prontamente dopo adeguato courettage della FLC e terapia antibiotica con ceftriaxone. Alla dimissione persisteva, tuttavia, moderata trombocitosi (806 x 103 / mm3). Dopo 20 giorni al controllo post-ricovero il bambino presentava gastroenterite acuta (con Rotavirus positivo nelle feci) e persistente trombocitosi (794 x 103 / mm3). Dopo 2 mesi circa, in seguito a nuovo accesso al Pronto Soccorso Pediatrico per gastro-enterite, gli esami ematici evidenziavano il protrarsi della trombocitosi (727 x 103 / mm3), rilevata anche a distanza di circa 1 mese in occasione di controllo in regime di Day-Hospital (PLT: 679 x 103 / mm3; Ab IgG anti-EBV ed EBNA positivi; EBV-DNA positivo in saliva ed urine).

      Output : 

      38,5°C | febbre
      12,03 x 103 / mm3 | leucocitosi
      57% | linfocitosi
      538 x 103 / mm3 | trombocitosi
      19 mm/sedim | VES
      positivi | anticorpi
      > 750 U/ml | VCAIgG
      negativi | EBNA-IgG
      negativi | VCA-IgM
      positivo | EBV-DNA
      20,4x106 copie/ml | EBV-DNA
      negativo | EBV-DNA
      500 leucociti/ micrl | leucocituria
      nella norma | urinocoltura
      nella norma | PCR
      nella norma | indici
      nella norma | ricerche
      nella norma | PTT
      nella norma | tampone
      nella norma | PT
      735 x 103 / mm3 | PLT
      39°C | febbre
      32,28 x 103 / mm3 | leucocitosi
      62,9% | neutrofilia
      732 x 103 / mm3 | trombocitosi
      36 mm/sedim | VES
      6,26 mg/dl | PCR
      66 UI/dl | GOT
      nella norma | immunoglobuline
      nella norma | sottopopolazioni
      nella norma | indici
      positivo | esame
      positivo | Staphilococcus
      positività | EBV-DNA
      1,83x106copie/ml | EBV-DNA
      6,72x103copie/ml | EBV-DNA
      806 x 103 / mm3 | trombocitosi
      positivo | Rotavirus
      794 x 103 / mm3 | trombocitosi
      727 x 103 / mm3 | trombocitosi
      679 x 103 / mm3 | PLT
      positivi | anti-EBV
      positivi | EBNA
      positivo | EBV-DNA

      Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

      Ora dammi l'output per il seguente testo:

      {Text}

      Stampa solo l'output se presente e nient'altro.
      """


      self.examples = [
        {
          "Testo": "B.M., bambino caucasico di 11 mesi, giunto all’osservazione nel febbraio 2011 per porpora di n.d.d. e febbre (38,5°C) da 3 giorni. Secondogenito di famiglia con basso livello socio-economico e con anamnesi remota e familiare negativa per patologie degne di nota. All’esame obiettivo stato di abbattimento, cute pallida, presenza di petecchie diffuse al tronco, iperemia intensa del faringe e rinite sierosa. Gli esami eseguiti mostravano lieve leucocitosi (12,03 x 103 / mm3), lieve linfocitosi relativa (57%), lieve trombocitosi (538 x 103 / mm3) divenuta moderata durante il ricovero (826 x 103 / mm3), VES mossa (19 mm/sedim; v.n.<10), anticorpi IgG anti-Epstein Barr Virus positivi (VCAIgG> 750 U/ml; negativi i VCA-IgM e gli EBNA-IgG), EBV-DNA positivo in saliva (20,4x106 copie/ml) e negativo nel sangue, moderata leucocituria (500 leucociti/ micrl); nella norma PT e PTT, PCR, indici epato-renali, tampone faringeo, urinocoltura e altre ricerche virologiche. L’esame morfologico del sangue periferico confermava la trombocitosi, senza altre alterazioni degne di nota. Alla dimissione sono stati programmati controlli post-ricovero per la persistenza di trombocitosi (PLT: 735 x 103 / mm3). All’età di 16 mesi, nuovo ricovero per febbre (39°C) e stato di abbattimento. All’EO cute pallida, faringe iperemico, fegato e milza palpabili a 2 cm dall’arco costale, edema periorbitario sinistro e ferita lacero-contusa suppurata in regione frontale, suturata 5 giorni prima in PSP, ove erano stati adottati, tuttavia, gli adeguati protocolli comuni (sutura in ambiente sterile e terapia antibiotica domiciliare con amoxicillina-ac.clavulanico). Dagli esami risultava moderata leucocitosi (32,28 x 103 / mm3), neutrofilia (62,9%), moderata trombocitosi (732 x 103 / mm3), indici di flogosi aumentati (VES: 36 mm/sedim, PCR: 6,26 mg/dl) ed incremento delle GOT (66 UI/dl); nella norma gli altri indici epato-renali, immunoglobuline e sottopopolazioni linfocitarie. L’esame colturale della ferita risultava positivo per Staphilococcus epidermidis, resistente ad amoxicillina-ac.clavulanico e sensibile alle cefalosporine. Gli esami virologici indicavano positività dell’EBV-DNA sia in saliva (1,83x106copie/ml) che nel sangue (6,72x103copie/ml). Le condizioni cliniche del bambino miglioravano prontamente dopo adeguato courettage della FLC e terapia antibiotica con ceftriaxone. Alla dimissione persisteva, tuttavia, moderata trombocitosi (806 x 103 / mm3). Dopo 20 giorni al controllo post-ricovero il bambino presentava gastroenterite acuta (con Rotavirus positivo nelle feci) e persistente trombocitosi (794 x 103 / mm3). Dopo 2 mesi circa, in seguito a nuovo accesso al Pronto Soccorso Pediatrico per gastro-enterite, gli esami ematici evidenziavano il protrarsi della trombocitosi (727 x 103 / mm3), rilevata anche a distanza di circa 1 mese in occasione di controllo in regime di Day-Hospital (PLT: 679 x 103 / mm3; Ab IgG anti-EBV ed EBNA positivi; EBV-DNA positivo in saliva ed urine).",
          "Output": 
      """
      38,5°C | febbre
      12,03 x 103 / mm3 | leucocitosi
      57% | linfocitosi
      538 x 103 / mm3 | trombocitosi
      19 mm/sedim | VES
      positivi | anticorpi
      > 750 U/ml | VCAIgG
      negativi | EBNA-IgG
      negativi | VCA-IgM
      positivo | EBV-DNA
      20,4x106 copie/ml | EBV-DNA
      negativo | EBV-DNA
      500 leucociti/ micrl | leucocituria
      nella norma | urinocoltura
      nella norma | PCR
      nella norma | indici
      nella norma | ricerche
      nella norma | PTT
      nella norma | tampone
      nella norma | PT
      735 x 103 / mm3 | PLT
      39°C | febbre
      32,28 x 103 / mm3 | leucocitosi
      62,9% | neutrofilia
      732 x 103 / mm3 | trombocitosi
      36 mm/sedim | VES
      6,26 mg/dl | PCR
      66 UI/dl | GOT
      nella norma | immunoglobuline
      nella norma | sottopopolazioni
      nella norma | indici
      positivo | esame
      positivo | Staphilococcus
      positività | EBV-DNA
      1,83x106copie/ml | EBV-DNA
      6,72x103copie/ml | EBV-DNA
      806 x 103 / mm3 | trombocitosi
      positivo | Rotavirus
      794 x 103 / mm3 | trombocitosi
      727 x 103 / mm3 | trombocitosi
      679 x 103 / mm3 | PLT
      positivi | anti-EBV
      positivi | EBNA
      positivo | EBV-DNA
      """
        },
        {
          "Testo": "Riportiamo il caso clinico di una bambina di 4 anni di origine pakistana, figlia di genitori consanguinei (cugini di primo grado). Nata a termine da parto eutocico in gravidanza normodecorsa, ha presentato sofferenza perinatale (apgar ad 1 minuto: 3) e ha necessitato di intubazione orotracheale. In prima giornata di vita riscontro di grave anemia emolitica e moderata piastrinopenia (Hb 7,8 g/dl, Ptl 76 x 109/l, ldH 14501u/l, CPK 778 u/l e ast 429 u/l) per cui la paziente è stata sottoposta a trasfusione di emazie concentrate e piastrine. In seconda giornata di vita grave ittero a bilirubina indiretta (bilirubina totale massima 21,7 mg/dl) che ha richiesto exanguinotrasfusione con rapido miglioramento clinico e normalizzazione degli indici di emolisi. La paziente è stata estubata in terza giornata di vita e non ha presentato ulteriori complicanze respiratorie. Dimessa in benessere a 2 settimane di vita con buona crasi ematica (Hb 11,8 g/dl, MCv 79,2 fl, Ptl 276000/mmc), la famiglia non si è presentata ai successivi controlli programmati per ulteriori approfondimenti e ha soggiornato per diversi mesi in Pakistan. A 45 mesi di vita per comparsa di grave anemia emolitica in corso di febbre (Hb 6,4 g/dl, MCv 81,8 fl, reticolociti 50,9 x 104/μl, ldH 3250u/l, bilirubina totale 2,90 mg/dl, bilirubina indiretta 2 mg/dl) e modesta splenomegalia (milza palpabile a 2 cm dall’arcata costale) la paziente ha effettuato nuova emotrasfusione. I test di Coombs diretto e indiretto sono risultati negativi; la morfologia eritrocitaria e il tracciato cromatografico hanno evidenziato un quadro suggestivo per emoglobinopatia da Hb H, senza evidenza di emoglobine patologiche. Il dosaggio dell’attività del G6PdH, lo studio delle resistenze osmotiche, il test di lisi al glicerolo ed il Pink test, oltre alle sierologie virali (Citmomegalovirus, epstain barr virus, Parvovirus) e alla ricerca del parassita malarico, sono risultati negativi. Si riscontrava una crescita staturo-ponderale al 3° percentile, regolare lungo la curva di crescita. A distanza di 2 mesi da tale evento, la bambina ha presentato sempre in corso di febbre (tampone nasofaringeo positivo per influenza b) un nuovo episodio di emolisi (Hb 6,0 g/dl, MCv 78,4 fl, reticolociti 12% ldH 1888 u/l) che ha necessitato nuovamente di trasfusione di emazie concentrate per lo scadimento delle condizioni generali. L’analisi molecolare dei geni delle catene emoglobiniche ha evidenziato omozigosi per l’emoglobina sallanches. La bambina si presenta attualmente in buone condizioni generali, con obiettività generale negativa eccetto per polo splenico palpabile a circa 1 cm dall’arcata costale. è seguita con cadenza mensile, salvo comparsa di sintomatologia. Si valuterà nei prossimi mesi l’eventuale necessità di un regime trasfusionale cronico in base all’andamento della malattia (all’ultimo emocromo Hb 8,2 g/dl, MCv 77,7 fl, reticolociti 57,85 x 104/μl). Assume terapia di supporto con acido folico e profilassi antibiotica con amoxicillina orale per ridurre gli eventi infettivi. Adeguate raccomandazioni per evitare alimenti o farmaci e sostanze pro-ossidanti sono state fornite alla famiglia. Risultano tuttora in corso accertamenti dei familiari per una corretta consulenza genetica.",
          "Output": 
      """
      3 | apgar
      7,8 g/dl | Hb
      76 x 109/l | Ptl
      14501u/l | ldH
      778 u/l | CPK
      429 u/l | ast
      21,7 mg/dl | bilirubina
      11,8 g/dl | Hb
      79,2 fl | MCv
      276000/mmc | Ptl
      6,4 g/dl | Hb
      81,8 fl | MCv
      50,9 x 104/μl | reticolociti
      3250u/l | ldH
      2,90 mg/dl | bilirubina
      2 mg/dl | bilirubina
      negativi | Coombs
      negativi | Pink
      negativi | studio
      negativi | sierologie
      negativi | dosaggio
      negativi | ricerca
      negativi | test
      al 3° percentile | crescita
      positivo | influenza
      positivo | tampone
      6,0 g/dl | Hb
      78,4 fl | MCv
      12% | reticolociti
      1888 u/l | ldH
      negativa | obiettività
      8,2 g/dl | Hb
      77,7 fl | MCv
      57,85 x 104/μl | reticolociti
      """
        },
      ]