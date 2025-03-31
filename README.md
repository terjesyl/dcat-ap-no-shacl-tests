# TODO

## Regler

Gi nytt navn til

- `:hasShapeCV-dcatThemeMin0MaxN`

For eksempel `hasNodeKindIRIShape-dcatTheme`


## Alle egenskaper

### Unik per språk

Definere at egenskap skal gjentas kun én gang per språk med `sh:uniqueLang`

Omformulere feilmelding til "There MUST be max. 1 value per language."

### Contact Point

Sjekke at typene til instanser av contactPoint er disjunkte (disjoint) (hvordan?)

### dct:Standard
Sjekke instanser av disse?
Hva om `<dataservice> a dct:Standard` utledes under resonnering? (er rdfs:range-aksiomet definert?)
Ligger dette utenfor scope?

### dcat:theme
Gjør LEAST 1-sjekk (avhengig av SEMICs avgjørelse).
Fiks maxCount 1 feil.

Hvis en URI matcher på data-theme-URI: sjekk inScheme.

For datasett, bør liste opp alle verdiene:
vis match på pattern, så MÅ verdien matche de listede hardkodede verdiene fra Data Theme.

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

### dct:subject

Tillate blanke noder?

### prov:wasGeneratedBy

Tillate blanke noder?
INFO om ikke fra Activity Type?

### dct:identifier (!)

`:hasMin0MaxNShape-dctIdentifier`:

har `sh:nodeKind sh:IRIOrLiteral;`

ikke spec-compliant, skal være `sh:nodeKind sh:Literal;`


### dct:license

Fiks sjekk, krever nå `a dct:LicenseDocument` ...

### conforms To

Skal peke til instanser av dct:Standard


### adms:status / CV Distribution Status

Fix typesjekk, krever `a skos:Concept` nå

### dct:accessRights / CV Access Right

Fiks typesjekk, `a skos:Concept`, hardkode verdiene (?)

### dcatap:applicableLegislation

Avklare: Regex-sjekk på URI?
Gjøre som Warning

### spdx:checksum

TODO: fix: Kan velge flere algoritmer

------------------------------------------------------------------------------------------------

## Kontrollerte vokabular

Skriv `sh:message` i vocabularies.shapes.ttl til engelsk fra norsk.

### Compress Format

Sjekk Pattern på Compress Format. Gi Warning.
Avklare: bruke IANA Media Type eller EUs File Type?

### Package Format

Sjekk Pattern på Package Format. Gi Warning.
Avklare: bruke IANA Media Type eller EUs File Type?

------------------------------------------------------------------------------------------------

## Datasett

Ordne kontrollerte vokabular:
- Spatial
- ...


------------------------------------------------------------------------------------------------

## Spørsmål til avklaring

Hvordan håndtere RECOMMENDED/OPTIONAL LEAST 1 (gjelder dcat:theme på DataService).

Hvem skal reglene være for? Internt i data.norge.no? For datatilbyder/leverandør?

### Instanser vi antar følger med fil (?)

og skal vi tillate blanke noder på disse?

- cv:Cost (cv:hasCost)
- odrs:RightsStatement (dct:rights)
- odrl:Policy (odrl:hasPolicy)
- spdx:Checksum (spdx:checksum)

Hva med:
- adms:Identifier (?)
- dct:Standard (?)
- dct:PeriodOfTime
- dcat:DataService (dcat:accessService)
- dcat:Dataset (dcat:servesDataset)
- prov:Attribution (prov:qualifiedAttribution)
- adms:Identifier (adms:identifier)
- dcat:Relationship (dcat:qualifiedRelation)
- dct:ProvenanceStatement (dct:provenance)
- dcat:Dataset (dct:replaces)
- dcat:Dataset (dcat:prev)
- dcat:Dataset (dcat:hasVersion)
- dqv:QualityAnnotation
- dqv:QualityMeasurement
- dcat:DatasetSeries (dcat:inSeries)
- dcat:Distribution (adms:sample)
- foaf:Agent og subklasser (dct:creator)

### Forslag

TODO (Nice-to-have): Sett `sh:Violation sh:Info` og gi informativ beskjed for alle shapes som ikke matcher på `sh:class <forventet-type-i-range>`


### Class/Range restrictions
class/range restrictions (ex: dcatap:applicableLegislation)

Legge til pattern (for å matche ELI). Hvordan?

Lage "advanced"-regelsett (sjekk av URL-patterns etc.) gi Warnings.


### Hvilke er LEAST 1, hvilke er MUST (closed range)

Forslag (basert på SEMICs forslag):

### LEAST 1

dcat:theme

### MUST (closed range)

Alle andre kontrollerte vokabularer


### Formulering av sh:message i Type-sjekk

"URI" eller "IRI"?

"The value of \[property\] MUST be an \[IRI/URI\]"
Denne formuleringen brukes i [SHACL](https://www.w3.org/TR/shacl/#NodeKindConstraintComponent):
"all values of ex:knows need to be IRIs"

"The value of \[property\] MUST be an \[IRI/URI\] or a Blank Node or a Literal"

"The property \[property\] MUST refer to an \[IRI/URI\]"

"The property \[property\] MUST be an \[IRI/URI\]"



------------------------------------------------------------------------------------------------

## TODO:

### Sjekke skrivefeil i sh:name

Enkelte Shapes har feil navn/name.

### Feilmeldinger
Gå gjennom alle feilmeldinger og omformuler.


------------------------------------------------------------------------------------------------
## Avklaringer Standard

Tydeliggjøre forskjellen dcat:hasVersion og dcat:version
For dcat:version: er dette versjonen for datasettet, eller beskrivelsen?

------------------------------------------------------------------------------------------------

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

## Hva skal reglene kalles?

TODO: Sjekk med SEMICs Guidelines at forslagene her stemmer overens

Sjekk av nodeKind (datatype/objekttype):
`:nodeKindShape-nnnnnn`

Eksempel: `:nodeKindShape-dctReplaces`

Sjekk av kardinalitet
`:minXMaxXShape-nnnnnn`

Eksempel: `:min1MaxNShape-dctTitle`

Sjekk av range (pattern)
`:hasShapeCV-nnnnnnnnPattern` eller `:hasShapeCVPattern-nnnnnnnn`

Eksempel: `:hasShapeCV-licensePattern` `:hasShapeCVPattern-license`

Sjekk av range (skos:inScheme)
`:hasShapeCV-nnnnnnn`

Eksempel: `:hasShapeCV-provWasGeneratedBy`

Og Node-sjekk:
`sh:node :AccrualPeriodicityRestriction` eller `sh:node :AccrualPeriodicityShape` ?