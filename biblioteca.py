from csv import writer

def carica_da_file(file_path):
    """Carica i libri dal file CSV e restituisce una lista di dizionari"""

    try:
        file_input = open(file_path, "r", encoding="utf-8")
        record = []  # lista di dizionari

        for righe in file_input:
            riga = righe.strip()  # rimuove \n e spazi
            if riga == "":   # se la riga è vuota, salto
                continue

            lista = riga.split(",")  # divide la riga in parti

            if len(lista) < 5:   #se non ci sono abbastanza colonne (da titolo a sezione), salto.
                print("Riga ignorata perché incompleta:", riga)
                continue

            try:
                record.append({
                    "Titolo Libro": lista[0],
                    "Autore": lista[1],
                    "Anno": int(lista[2]),
                    "Numero Pagine": int(lista[3]),
                    "Sezione": int(lista[4])
                })
            except ValueError:
                # Se non riesco a convertire i numeri → salto la riga
                print("Riga ignorata perché ha valori non validi:", riga)
                pass

        return record

    except FileNotFoundError:
        print("Il nome del file sorgente inserito non è corretto.")
        return None

    finally:
        try:
            file_input.close()
        except:
            pass




def aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path):
    """Aggiunge un libro nella biblioteca"""
    aggiungo_nuovo_libro = True
    for elemento in biblioteca:
        if (elemento["Titolo Libro"].lower() == titolo.lower() and elemento["Autore"].lower() == autore.lower()):
            print("Questo libro è già presente nella biblioteca")
            print(f"Eccolo: {elemento}")
            aggiungo_nuovo_libro = False
            break #se trovo il libro già presente smetto di iterare
        elif sezione < 1 or sezione > 5:
            print("Questa sezione non è disponibile (range 1-5)")
            aggiungo_nuovo_libro = False
            break #non posso aggiungere un libro con sezione sbagliata

    if aggiungo_nuovo_libro: #cioè se ha passato tutti i controlli precedenti
        """Aggiunge il libro nella lista di dizionari direttamente qui ma poteva esser fatto dopo il try richiamando la funzione 
        carica da file che sovrascriveva tutti i vecchi dati già presenti aggiungendo anche il nuovo libro"""
        biblioteca.append({
            "Titolo Libro": titolo,
            "Autore": autore,
            "Anno": anno,
            "Numero Pagine": pagine,
            "Sezione": sezione})
        try:
            with open(file_path, "a",newline='', encoding="utf-8") as fileaperto:
                csvWriter = writer(fileaperto)
                csvWriter.writerow([titolo, autore, anno, pagine, sezione]) #non necessario fare controllo sulla pulizia o su conversione int perchè già fatta nel main
                print(f"Riferimenti libro:\t\n Titolo: {titolo} \t\n Autore: {autore}\t\n Anno: {anno} \t\n Numero Pagine: {pagine} \t\n Sezione: {sezione}")
        except Exception: #eccezione generale
            print("Errore durante l'aggiunta del nuovo libro nel file")

    return aggiungo_nuovo_libro #variabile boolena vera se agggiungo, falso se non aggiungo



def cerca_libro(biblioteca, titolo):
    """Cerca un libro nella biblioteca dato il titolo"""
    for elemento in biblioteca:
        if elemento["Titolo Libro"].lower()== titolo.lower(): #prevede inserimento della ricerca tutto in minuscolo
            return elemento

    # TODO


def elenco_libri_sezione_per_titolo(biblioteca, sezione):
    """Ordina i titoli di una data sezione della biblioteca in ordine alfabetico"""
    libri_di_sezione=[]
    procedi_con_ordinamento= True
    while procedi_con_ordinamento: #variabile di tipo bool così da controllare range (1-5) di sezione
        if sezione > 0 and sezione < 6:
            for elemento in biblioteca:
                if elemento["Sezione"] == sezione:
                    libri_di_sezione.append(elemento)
            procedi_con_ordinamento= False
        else:
            print("Hai inserito una sezione non presente nella biblioteca\n")
            sezione = int(input("Inserisci una sezione (1-5): "))

    lista_ordinata_per_nome = sorted(libri_di_sezione, key=lambda libro: libro['Titolo Libro'])
    return lista_ordinata_per_nome

def main():
    biblioteca = []
    file_path = "biblioteca.csv"

    while True:
        print("\n--- MENU BIBLIOTECA ---")
        print("1. Carica biblioteca da file")
        print("2. Aggiungi un nuovo libro")
        print("3. Cerca un libro per titolo")
        print("4. Ordina titoli di una sezione")
        print("5. Esci")

        scelta = input("Scegli un'opzione >> ").strip()

        if scelta == "1":
            while True:
                file_path = input("Inserisci il path del file da caricare: ").strip()
                biblioteca = carica_da_file(file_path)
                if biblioteca is not None:
                    break

        elif scelta == "2":
            if not biblioteca:
                print("Prima carica la biblioteca da file.")
                continue

            titolo = input("Titolo del libro: ").strip()
            autore = input("Autore: ").strip()
            try:
                anno = int(input("Anno di pubblicazione: ").strip())
                pagine = int(input("Numero di pagine: ").strip())
                sezione = int(input("Sezione: ").strip())
            except ValueError:
                print("Errore: inserire valori numerici validi per anno, pagine e sezione.")
                continue

            libro = aggiungi_libro(biblioteca, titolo, autore, anno, pagine, sezione, file_path)
            if libro:
                print(f"Libro aggiunto con successo!")
            else:
                print("Non è stato possibile aggiungere il libro.")

        elif scelta == "3":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            titolo = input("Inserisci il titolo del libro da cercare: ").strip()
            risultato = cerca_libro(biblioteca, titolo)
            if risultato:
                print(f"Libro trovato: {risultato}")
            else:
                print("Libro non trovato.")

        elif scelta == "4":
            if not biblioteca:
                print("La biblioteca è vuota.")
                continue

            try:
                sezione = int(input("Inserisci numero della sezione da ordinare: ").strip())
            except ValueError:
                print("Errore: inserire un valore numerico valido.")
                continue

            titoli = elenco_libri_sezione_per_titolo(biblioteca, sezione)
            if titoli is not None:
                print(f'\nSezione {sezione} ordinata:')
                print("\n".join([f"- {titolo}" for titolo in titoli]))

        elif scelta == "5":
            print("Uscita dal programma...")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    main()

