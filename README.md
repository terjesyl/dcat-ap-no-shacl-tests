# TODO

## Regler

Gi nytt navn til

- `:hasShapeCV-dcatThemeMin0MaxN`

For eksempel `hasNodeKindIRIShape-dcatTheme`


## Alle egenskaper

### Unik per språk

Definere at egenskap skal gjentas kun én gang per språk med `sh:uniqueLang`

### Contact Point

Sjekke at typene til instanser av contactPoint er disjunkte (disjoint) (hvordan?)

### dct:Standard
Sjekke instanser av disse?
Hva om `<dataservice> a dct:Standard` utledes under resonnering? (er rdfs:range-aksiomet definert?)
Ligger dette utenfor scope?

### dcat:theme
Gjør LEAST 1-sjekk (avhengig av SEMICs avgjørelse).
Fiks maxCount 1 feil.

For datasett, bør liste opp alle verdiene.

### cv:hasCost

Implementere sjekk på
- EITHER foaf:page (dokumentasjon)
- OR hasValue AND currency


### dcat:theme (!)

`:hasShapeCV-dcatThemeMin1MaxN`:

```turtle
:hasShapeCV-dcatThemeMin1MaxN a sh:PropertyShape;
  # ...
  sh:maxCount 1; # ??? Skal være minCount ?
  # ...
  .
```

### dct:identifier (!)

`:hasMin0MaxNShape-dctIdentifier`:

har `sh:nodeKind sh:IRIOrLiteral;`

ikke spec-compliant, skal være `sh:nodeKind sh:Literal;`

### dct:license

Fiks sjekk, krever nå `a dct:LicenseDocument` ...

### adms:status / CV Distribution Status

Fix typesjekk, krever `a skos:Concept` nå

### dct:accessRights / CV Access Right

Fiks typesjekk, `a skos:Concept`, hardkode verdiene (?)

### dcatap:applicableLegislation

Avklare: Regex-sjekk på URI?
Gjøre som Warning

## Kontrollerte vokabular

Skriv `sh:message` i vocabularies.shapes.ttl til engelsk fra norsk.

### Compress Format

Sjekk Pattern på Compress Format. Gi Warning.
Avklare: bruke IANA Media Type eller EUs File Type?

### Package Format

Sjekk Pattern på Package Format. Gi Warning.
Avklare: bruke IANA Media Type eller EUs File Type?

------------------------------------------------------------------------------------------------

## Spørsmål til avklaring

Hvordan håndtere RECOMMENDED/OPTIONAL LEAST 1 (gjelder dcat:theme på DataService).

Hvem skal reglene være for? Internt i data.norge.no? For datatilbyder/leverandør?

### Class/Range restrictions
class/range restrictions (ex: dcatap:applicableLegislation)

Legge til pattern (for å matche ELI). Hvordan?

Lage "advanced"-regelsett (sjekk av URL-patterns etc.) gi Warnings.

### cv:Cost

Anta at ligger i fil, eller akseptere URI-er/referanser til eksterne ressurser?

### Rights Statement

Anta at følger med fil?
Tillate blanke noder?

### Hvilke er LEAST 1, hvilke er MUST (closed range)

Forslag (basert på SEMICs forslag):

### LEAST 1

| Egenskap   | SEMICs forslag (hvis tomt = likt) |
| ---------- | --------------------------------- |
| dcat:theme |                                   |

### Optional

### Recommended

??

### MUST (closed range)

Alle andre kontrollerte vokabularer

------------------------------------------------------------------------------------------------

## TODO:

### Sjekke skrivefeil i sh:name

Enkelte Shapes har feil navn/name.

### Bruk av rdfs:label
Bytte ut rdfs:label med sh:name på NodeShapene det gjelder (mange)

### Feilmeldinger
Gå gjennom alle feilmeldinger og omformuler.

### LEAST 1 vs. MUST (closed range)
Må gå gjennom alle regler og sjekke at OR-constraint er riktig for LEAST 1 (HVIS brukes, SÅ MÅ shape validere).

| Klasse      | Egenskap      | Fikset |
| ----------- | ------------- | ------ |
| DataService | theme?        |        |
| DataService | availability? |        |

### Forslag:

Alt som sjekker ressurser fra tredjeparter bør plasseres utenfor Core.

DCAT-AP-NO Mandatory/Minimum Shapes:
- Subsett av (hva? alle de andre?)
- Sjekker at obligatoriske egenskaper fins (Property Shapes)
- Sjekker at klasser datatilbyder kan forventes å ha

DCAT-AP-NO "Core Shapes":
- Obligatoriske og valgfrie egenskaper
- Property shapes: kontrollerer alle obligatoriske egenskaper
- Node shapes: kontroller ressurser **datatilbyder** har ansvar for
  - Ekskluderer sjekk av tredjeparts ressurser

DCAT-AP-NO "Range Shapes" (? jf. DCAT-AP), eller DCAT-AP-NO "External Shapes" "Core Vocab:
- Node shapes på tredjeparts ressurser (EUs kontrollerte vokabularer)


### Skrive om hvordan valideringsreglene funker.

Hvem er reglene ment for/hvem har vi hatt i fokus? Jo, datatilbyder: hvordan lage valideringsregler som *hjelper datatilbyder* med å lage så gode beskrivelser som mulig.

Ikke alt kan sjekkes.
Eksempel: sjekker AT du har brukt en URI og ikke bare en tekst, men kan ikke sjekke at du lenker til riktig ressurs/nettside/API.

Er avhengig av tredjeparter som tilbyr ressurser (f.eks. kodelistene fra EU/SEMIC, referanser til lover/reguleringer hos LovData) selv oppgir typen til ressursen.
Ikke noe poeng å validere mot dette, siden det ikke er datatilbyder sitt ansvar å oppgi typen til ressurser fra tredjeparter. Må nesten anta at de kontrollerte vokabularene vi henviser til er av riktig type, ellers hadde det ikke vært noe poeng at standarden krever at de brukes.

Der hvor det er krav til bruk av kontrollerte vokabularer sjekker vi at URL-en stemmer. Er fortsatt rom for å legge inn feil kode (f.eks. på dcat:theme).

Formulering "Egenskapen dcat:landingPage SKAL referere til en instans av foaf:Document" er ikke så hjelpsom. Hva er et "foaf:Document"?
Tilbyder trenger å vite at de må referere til en URI, f.eks.: "Egenskapen dcat:landingPage SKAL referere til en URI. Eks: dcat:landingPage <https://eksempel.com/landing-page>" (skal vi ta med vinkelparentes <> i tekst?)

------------------------------------------------------------------------------------------------


# Typer sjekk

Vurder å splitte opp i separate filer.

- Range
  - Type på Node som PropertyShape sjekker (sh:class)
  - Kan ikke antas å eksistere i data-graf (eks. typen til Publisher)
- Nodekind
  - kan antas å eksistere i data-grafen
  - kan sjekkes på PropertyShape (sh:nodeKind)
  - eks: skal være URI og ikke rdfs:Literal
- Kardinalitet
  - min og max count + LEAST 1
- Controlled Vocabularies
  - Validere CV som data-grafer
