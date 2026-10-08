class Strumento:
    def __init__(self, cod, tipo, marca, anno_acquisto, valore):
        self.cod = cod
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = anno_acquisto
        self.valore = valore

    def __str__(self):
        return (
            f"{self.cod}: {self.tipo} {self.marca}, "
            f"anno {self.anno_acquisto}, valore {self.valore:.2f} euro"
        )


class Prestito:
    def __init__(self, cod, data, id_strumento, cognome_allievo):
        self.cod = cod
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo


    def __str__(self):
        return (
            f"{self.cod}: strumento {self.id_strumento}, "
            f"allievo {self.cognome_allievo}, data {self.data}"
        )


class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati."""
        self.nome = nome
        self.responsabile = responsabile
        self.strumenti = []
        self.prestiti = []
        self.contatore_prestiti = 0

    @nome.setter
    def nome(self, value):
        if not value:
            raise ValueError("Errore: il nome del deposito non può essere vuoto")
        self._nome = value


    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file."""

        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                riga = riga.strip()

                cod, tipo, marca, anno_acquisto, valore = riga.split(",")
                cod = cod.strip()
                strumento = Strumento(
                    cod,
                    tipo.strip(),
                    marca.strip(),
                    int(anno_acquisto),
                    float(valore)
                )

                self.strumenti.append(strumento)


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel sistema senza aggiornare il file."""
        numero = max((int(s.cod[1:]) for s in self.strumenti),default=0) + 1

        cod = f"S{numero}"
        strumento = Strumento(cod, tipo, marca, anno_acquisto, valore)

        self.strumenti.append(strumento)
        return strumento

    def strumenti_ordinati_per_marca(self):
        """Restituisce gli strumenti ordinati alfabeticamente per marca."""
        return sorted(self.strumenti, key=lambda s: s.marca)

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito."""
        if not any(s.cod == id_strumento for s in self.strumenti):
            raise ValueError("Errore: strumento non trovato")

        if any(p.id_strumento == id_strumento for p in self.prestiti):
            raise ValueError("Errore: strumento già in prestito")

        self.contatore_prestiti += 1
        cod = f"P{self.contatore_prestiti}"

        prestito = Prestito(cod, data, id_strumento, cognome_allievo)

        self.prestiti.append(prestito)
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito rimuovendolo dal sistema."""
        for prestito in self.prestiti:
            if prestito.cod == id_prestito:
                self.prestiti.remove(prestito)
                return

        raise ValueError("Errore: prestito non trovato")