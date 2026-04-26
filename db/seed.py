import sqlite3, json
from pathlib import Path

DB_PATH = Path(__file__).parent / "permits.db"

PERMITS = [
    ("BG-2024-0001","Thomas Müller","Hauptstraße 12, 04109 Leipzig","Neubau","genehmigt","2024-01-15","2024-04-15","[]","Sabine Koch","Einfamilienhaus, 2 Geschosse, 180 m²"),
    ("BG-2024-0002","Petra Hoffmann","Schillerstraße 5, 04109 Leipzig","Umbau","in_bearbeitung","2024-02-01","2024-05-01",'["Statiknachweis","Brandschutznachweis"]',"Martin Weber","Dachgeschoss zu Wohnnutzung"),
    ("BG-2024-0003","Klaus Schmidt","Goethestraße 28, 04105 Leipzig","Abriss","ausstehend","2024-02-15","2024-05-15",'["Lageplan (amtl. beglaubigt)","Katasterauszug"]',"Anna Hoffmann","Abriss Altbau, 3 Geschosse"),
    ("BG-2024-0004","Maria Weber","Bahnhofstraße 44, 04109 Leipzig","Nutzungsänderung","überfällig","2024-01-20","2024-03-20",'["Brandschutznachweis","Entwässerungsplan"]',"Klaus Richter","Büro zu Wohnung"),
    ("BG-2024-0005","Andreas Fischer","Lindenallee 7, 04229 Leipzig","Neubau","in_bearbeitung","2024-03-01","2024-06-01",'["Energieausweis (EnEV)"]',"Jana Schmidt","Doppelhaushälfte, 2 Geschosse"),
    ("BG-2024-0006","Sabine Braun","Rosenstraße 19, 04103 Leipzig","Umbau","genehmigt","2024-01-10","2024-04-10","[]","Sabine Koch","Fassadensanierung EG+OG"),
    ("BG-2024-0007","Günter Lehmann","Kastanienallee 3, 04105 Leipzig","Neubau","überfällig","2023-12-01","2024-03-01",'["Bauzeichnung (Grundriss)","Abstandsflächennachweis","Unterschriftenblatt"]',"Martin Weber","Garage und Carport"),
    ("BG-2024-0008","Ingrid Schulz","Friedrichstraße 88, 04107 Leipzig","Nutzungsänderung","genehmigt","2024-02-20","2024-05-20","[]","Anna Hoffmann","Laden zu Restaurant"),
    ("BG-2024-0009","Werner Becker","Südstraße 15, 04277 Leipzig","Umbau","in_bearbeitung","2024-03-10","2024-06-10",'["Statiknachweis"]',"Klaus Richter","Balkonsanierung, 4-geschossig"),
    ("BG-2024-0010","Hannelore Neumann","Weststraße 42, 04229 Leipzig","Neubau","ausstehend","2024-04-01","2024-07-01",'["Lageplan (amtl. beglaubigt)","Bauzeichnung","Energieausweis (EnEV)"]',"Jana Schmidt","Reihenendhaus, 3 Geschosse"),
    ("BG-2024-0011","Bernd Zimmermann","Nordstraße 6, 04105 Leipzig","Abriss","genehmigt","2024-01-25","2024-04-25","[]","Sabine Koch","Industriehalle, 1.200 m²"),
    ("BG-2024-0012","Claudia Wagner","Eisenbahnstraße 77, 04315 Leipzig","Neubau","abgelehnt","2024-02-10","2024-05-10","[]","Martin Weber","GRZ überschritten"),
    ("BG-2024-0013","Rolf Hartmann","Plagwitzer Straße 21, 04229 Leipzig","Umbau","überfällig","2024-01-05","2024-03-05",'["Baulastenauskunft","Entwässerungsplan"]',"Anna Hoffmann","Keller zu Gewerbe"),
    ("BG-2024-0014","Monika Klein","Bornaische Straße 34, 04277 Leipzig","Nutzungsänderung","in_bearbeitung","2024-03-15","2024-06-15",'["Brandschutznachweis"]',"Klaus Richter","Praxis zu Büro, 3. OG"),
    ("BG-2024-0015","Hans-Peter Voigt","Karl-Liebknecht-Str. 50, 04107 Leipzig","Neubau","in_bearbeitung","2024-03-20","2024-06-20",'["Katasterauszug","Abstandsflächennachweis"]',"Jana Schmidt","MFH, 5 Wohneinheiten"),
    ("BG-2024-0016","Elke Bergmann","Koburger Straße 8, 04277 Leipzig","Umbau","ausstehend","2024-04-05","2024-07-05",'["Statiknachweis","Brandschutznachweis","Energieausweis (EnEV)"]',"Sabine Koch","Wintergarten EG"),
    ("BG-2024-0017","Dieter Krause","Oststraße 103, 04315 Leipzig","Neubau","genehmigt","2024-01-18","2024-04-18","[]","Martin Weber","Bürogebäude, 3 Geschosse"),
    ("BG-2024-0018","Ute Herrmann","Zschochersche Str. 56, 04229 Leipzig","Abriss","in_bearbeitung","2024-02-28","2024-05-28",'["Katasterauszug"]',"Anna Hoffmann","Nebengebäude Abbruch"),
    ("BG-2024-0019","Frank Dietrich","Gerichtsweg 4, 04103 Leipzig","Nutzungsänderung","ausstehend","2024-04-10","2024-07-10",'["Lageplan (amtl. beglaubigt)","Unterschriftenblatt"]',"Klaus Richter","Lager zu Wohnen, OG"),
    ("BG-2024-0020","Renate Schreiber","Härtelstraße 8, 04107 Leipzig","Neubau","überfällig","2023-11-15","2024-02-15",'["Bauzeichnung (Grundriss)","Statiknachweis","Lageplan"]',"Jana Schmidt","Carport und Gartenhaus"),
    ("BG-2024-0021","Otto Schäfer","Josephstraße 12, 04177 Leipzig","Umbau","genehmigt","2024-01-30","2024-04-30","[]","Sabine Koch","Dachabdichtung"),
    ("BG-2024-0022","Margot König","Lützner Straße 88, 04177 Leipzig","Neubau","in_bearbeitung","2024-03-25","2024-06-25",'["Energieausweis (EnEV)","Entwässerungsplan"]',"Martin Weber","Wohnhaus mit Einliegerwohnung"),
    ("BG-2024-0023","Jürgen Bauer","Mockauer Straße 55, 04357 Leipzig","Umbau","ausstehend","2024-04-12","2024-07-12",'["Statiknachweis","Abstandsflächennachweis"]',"Anna Hoffmann","Terrassenüberdachung"),
    ("BG-2024-0024","Hildegard Richter","Torgauer Straße 20, 04318 Leipzig","Nutzungsänderung","genehmigt","2024-02-05","2024-05-05","[]","Klaus Richter","Kita-Umbau"),
    ("BG-2024-0025","Volker Pfeiffer","Wurzner Straße 14, 04318 Leipzig","Neubau","abgelehnt","2024-02-22","2024-05-22","[]","Jana Schmidt","Parkplatznachweise fehlen"),
    ("BG-2024-0026","Brigitte Lorenz","Engelsdorfer Straße 7, 04319 Leipzig","Umbau","überfällig","2024-01-02","2024-03-02",'["Brandschutznachweis","Baulastenauskunft"]',"Sabine Koch","Heizanlage Keller"),
    ("BG-2024-0027","Manfred Krüger","Holzhäuser Straße 33, 04299 Leipzig","Neubau","genehmigt","2024-01-08","2024-04-08","[]","Martin Weber","EFH, Massivbau, 220 m²"),
    ("BG-2024-0028","Elfriede Sommer","Probstheidaer Str. 4, 04299 Leipzig","Abriss","in_bearbeitung","2024-03-08","2024-06-08",'["Katasterauszug","Unterschriftenblatt"]',"Anna Hoffmann","Teilabriss Wirtschaftsgebäude"),
    ("BG-2024-0029","Herbert Lange","Stötteritzer Straße 91, 04299 Leipzig","Nutzungsänderung","ausstehend","2024-04-15","2024-07-15",'["Lageplan","Brandschutznachweis","Entwässerungsplan"]',"Klaus Richter","Arztpraxis zu Büro"),
    ("BG-2024-0030","Waltraud Fuchs","Windmühlenstraße 17, 04107 Leipzig","Neubau","in_bearbeitung","2024-03-18","2024-06-18",'["Abstandsflächennachweis"]',"Jana Schmidt","Wintergarten EG, 28 m²"),
    ("BG-2024-0031","Lothar Stein","Connewitzer Straße 45, 04277 Leipzig","Umbau","genehmigt","2024-02-14","2024-05-14","[]","Sabine Koch","Fenstererneuerung gesamt"),
    ("BG-2024-0032","Adelheid Möller","Meusdorfer Straße 3, 04277 Leipzig","Neubau","überfällig","2023-12-10","2024-03-10",'["Bauzeichnung (Grundriss)","Katasterauszug"]',"Martin Weber","Tiny House auf Eigengrund"),
    ("BG-2024-0033","Gerd Wolff","Raschwitzer Straße 22, 04207 Leipzig","Abriss","ausstehend","2024-04-18","2024-07-18",'["Statiknachweis","Baulastenauskunft"]',"Anna Hoffmann","Stallgebäude, Dorfkern"),
    ("BG-2024-0034","Hilde Brandt","Grünauer Allee 60, 04207 Leipzig","Nutzungsänderung","genehmigt","2024-01-22","2024-04-22","[]","Klaus Richter","Supermarkt zu Fitnessstudio"),
    ("BG-2024-0035","Siegfried Kramer","Ratzelstraße 8, 04207 Leipzig","Neubau","in_bearbeitung","2024-03-28","2024-06-28",'["Energieausweis (EnEV)","Brandschutznachweis"]',"Jana Schmidt","MFH, 8 WE, KfW 55"),
    ("BG-2024-0036","Christiane Henkel","Georg-Schwarz-Str. 100, 04179 Leipzig","Umbau","ausstehend","2024-04-20","2024-07-20",'["Statiknachweis","Unterschriftenblatt","Entwässerungsplan"]',"Sabine Koch","Industriehalle zu Loft"),
    ("BG-2024-0037","Rudolf Koch","Luisenstraße 14, 04315 Leipzig","Neubau","genehmigt","2024-01-28","2024-04-28","[]","Martin Weber","Fertiggarage"),
    ("BG-2024-0038","Anneliese Becker","Rietzschkestraße 29, 04347 Leipzig","Abriss","genehmigt","2024-02-08","2024-05-08","[]","Anna Hoffmann","Scheune, baufällig"),
    ("BG-2024-0039","Norbert Hahn","Portitzer Allee 5, 04356 Leipzig","Nutzungsänderung","abgelehnt","2024-03-03","2024-06-03","[]","Klaus Richter","Kurzzeitvermietung"),
    ("BG-2024-0040","Margit Schulze","Permoserstraße 11, 04318 Leipzig","Neubau","in_bearbeitung","2024-03-22","2024-06-22",'["Lageplan (amtl. beglaubigt)"]',"Jana Schmidt","EFH mit Einliegerwohnung"),
    ("BG-2024-0041","Eberhard Naumann","Mockauer Straße 3, 04357 Leipzig","Umbau","überfällig","2024-01-03","2024-03-03",'["Bauzeichnung","Abstandsflächennachweis","Brandschutznachweis"]',"Sabine Koch","EG barrierefrei"),
    ("BG-2024-0042","Rosemarie Pohl","Kieler Straße 66, 04357 Leipzig","Neubau","ausstehend","2024-04-22","2024-07-22",'["Statiknachweis","Katasterauszug","Energieausweis (EnEV)"]',"Martin Weber","Bürogebäude, 2 Geschosse"),
    ("BG-2024-0043","Wilhelmine Dressler","Heiterblickallee 30, 04349 Leipzig","Abriss","genehmigt","2024-02-12","2024-05-12","[]","Anna Hoffmann","Gartenlaube >24 m²"),
    ("BG-2024-0044","Friedhelm Möbius","Schönefelder Allee 4, 04356 Leipzig","Nutzungsänderung","in_bearbeitung","2024-03-30","2024-06-30",'["Brandschutznachweis","Entwässerungsplan"]',"Klaus Richter","Lager zu KFZ-Werkstatt"),
    ("BG-2024-0045","Konstanze Müller-Braun","Seehausener Allee 7, 04356 Leipzig","Neubau","genehmigt","2024-01-12","2024-04-12","[]","Jana Schmidt","Supermarkt, 800 m²"),
    ("BG-2024-0046","Theodor Buchholz","Quelle 4, 04356 Leipzig","Umbau","in_bearbeitung","2024-03-05","2024-06-05",'["Statiknachweis"]',"Sabine Koch","Aufstockung, 1 Geschoss"),
    ("BG-2024-0047","Walburga Günther","Dieskaustraße 44, 04249 Leipzig","Neubau","ausstehend","2024-04-25","2024-07-25",'["Lageplan","Bauzeichnung","Unterschriftenblatt","Energieausweis"]',"Martin Weber","EFH, Holzrahmenbau"),
    ("BG-2024-0048","Reinhold Kraft","Knautnaundorfer Str. 2, 04249 Leipzig","Abriss","ausstehend","2024-04-28","2024-07-28",'["Katasterauszug","Baulastenauskunft"]',"Anna Hoffmann","Plattenbau, Teilrückbau"),
    ("BG-2024-0049","Ingeborg Seidel","Ratsholzstraße 7, 04207 Leipzig","Nutzungsänderung","genehmigt","2024-02-18","2024-05-18","[]","Klaus Richter","Wohnhaus zu Pflegeheim"),
    ("BG-2024-0050","Berthold Arndt","Tarostraße 15, 04105 Leipzig","Neubau","in_bearbeitung","2024-04-02","2024-07-02",'["Abstandsflächennachweis","Entwässerungsplan"]',"Jana Schmidt","Parkhaus, 120 Stellplätze"),
]

def seed():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS permits;
        CREATE TABLE permits (
            id                TEXT PRIMARY KEY,
            applicant         TEXT NOT NULL,
            address           TEXT NOT NULL,
            type              TEXT NOT NULL,
            status            TEXT NOT NULL,
            submitted_date    TEXT NOT NULL,
            deadline          TEXT NOT NULL,
            missing_documents TEXT NOT NULL DEFAULT '[]',
            assigned_clerk    TEXT NOT NULL,
            note              TEXT
        );
    """)
    cur.executemany(
        "INSERT INTO permits VALUES (?,?,?,?,?,?,?,?,?,?)",
        PERMITS
    )
    con.commit()
    con.close()
    print(f"✓ Seeded {len(PERMITS)} permits → {DB_PATH}")

if __name__ == "__main__":
    seed()
