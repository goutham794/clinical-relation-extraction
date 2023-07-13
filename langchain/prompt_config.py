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
        self.example_in_prompt_template="Testo :\n{Text}\n\nOutput :\n{Output}"

        self.prompt_suffix = """
        Nota: nell'output viene scritto prima il risultato e poi il nome del test. Sono separati da '|'.

Ora dammi l'output per il seguente testo:

{Text}

Stampa solo l'output se presente e nient'altro.
        """

        self.sample_clinical_stmt = "M.d., maschio di 9 anni giunge alla nostra osservazione per episodio di macroematuria terminale, con urine color rosso vivo, preceduto da dolore addominale intermittente nelle due settimane precedenti. Una prima ecografia renale eseguita all’ingresso evidenzia reni di normali dimensioni in assenza di calcoli, vie urinarie non dilatate e vescica a contenuto finemente corpuscolato. Gli accertamenti ematologici ed urinari di primo livello hanno permesso di escludere le più comuni cause di macroematuria del bambino, in particolare la glomerulonefrite post-infettiva, la calcolosi renale e l’infezione urinaria. Dopo 2 giorni, per il persistere della macroematuria, ripetiamo un’ecografia renale che mette in evidenza una “idroureteronefrosi dx con materiale ipoecogeno non vascolarizzato a livello del calice inferiore, della pelvi e del tratto iniziale dell’uretere”, interpretati dal radiologo come possibile coagulo ematico. Tuttavia le ecografie ripetute nei giorni successivi hanno mostrato una sostanziale stabilità del quadro, rendendo poco probabile l’ipotesi formulata. Il riscontro di una ipereosinofilia periferica (e 1200/mmc) ci ha fatto ipotizzare una infezione da schistosoma, che raramente può causare nel bambino lesioni polipoidi sanguinanti di pelvi ed uretere; tuttavia la ricerca del parassita nelle urine è risultata negativa. Decidiamo quindi di eseguire una uro-angio-RM che ha permesso di evidenziare a livello della regione papillare del calice inferiore dx una formazione rotondeggiante del diametro di 15 mm ampiamente protrudente nel calice inferiore, con spiccata impregnazione di mdc. L’agobiopsia percutanea ecoguidata e la successiva nefrectomia hanno permesso di porre diagnosi di rabdomiosarcoma embrionale, variante botrioide. La massa neoplastica ha dimensioni di 5x2.5 cm, il restante parenchima renale, il tessuto adiposo ed i linfonodi sono indenni da neoplasia. Gli accertamenti strumentali e le biopsie ossee sono risultati negativi per localizzazioni secondarie di malattia."

    def set_Spanish_config(self):
        self.few_shot_doc_ids = ['100417', '100631', '100320', '100363', '100937']

        self.prompt_prefix = "Tengo una tarea que consiste en extraer menciones de pruebas de laboratorio y sus resultados de declaraciones clínicas. Aquí hay un ejemplo de texto y salida:"
        # self.prompt_prefix_2 = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco due esempi di testo e output:"
        self.example_in_prompt_template="Texto :\n{Text}\n\nOutput :\n{Output}"

        self.prompt_suffix = """
        Nota: El resultado se escribe primero y luego el nombre de la prueba en la salida. Están separados por '|'.

Ahora dame la salida para el siguiente texto:

{Text}

Imprime solo la salida y si no la hay, no imprimas nada
        """


    def set_Basque_config(self):
      self.few_shot_doc_ids = ['100031', '100017', '100016', '100177', '100009']

      self.prompt_prefix = "Laborategiko proben aipamenak eta haiei dagozkien emaitzak adierazpen klinikoetatik ateratzeko zeregina daukat. Hona hemen testuaren eta irteeraren adibide bat"
    #   self.prompt_prefix_2 = "Ho un compito che è quello di estrarre menzioni di test di laboratorio e dei loro risultati da dichiarazioni cliniche. Ecco due esempi di testo e output:"
      self.example_in_prompt_template="Testua :\n{Text}\n\nIrteera :\n{Output}"

      self.prompt_suffix = """
      Oharra: emaitza idazten da lehenik eta gero probaren izena irteeran. '|'z bereizten dira.

Orain eman iezadazu testu honen irteera:

{Text}

Inprimatu bakarrik irteera existitzen bada eta kito
      """