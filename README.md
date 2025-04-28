# Nye SHACL-regler for DCAT-AP-NO

## Gjenstår å sjekke

- [ ] odrs:RightsStatement
  - I Core, Ranges, Vocabularies
- [ ] dct:Standard
  - I Core, Ranges, Vocabularies
- [ ] spdx:Checksum
  - I Ranges og Vocabularies

Jeg vil prioritere å få ut beta-versjon. Disse klassene er i lite bruk (53 instanser av dct:Standard, 0 på de andre), vil vente med å lage regler, ev. prioritere det om det dukker opp konkrete behov.

**AVKLARING:** OK å avvente disse?

## Oppslitting i flere regelsett

Har delt opp i flere regelsett, for å øke gjenbrukbarheten i ulike sammenhenger:

- "Core"/hovedregler: sjekker kardinalitet, og at verdi- og datatype er riktig (Literal, URI, Blank Node). Sjekker også Data Theme for Datasett
- Ranges: Sjekker noen klasser (de som er antatt embedded), og sjekker match av kontrollerte vokabularer med Pattern match (er ikke eksakt)
- Vocabularies: Sjekker eksakt match på verdier fra eksterne vokabularer (kodene fra vokabularene må lastes inn)

Les mer lenger ned under *Utdypende om oppsplitting i Regelsett (Core/Ranges/Vocabularies)*

**AVKLARING:** Enig med tilnærmingen og oppsplitting i flere regelsett?

Neste steg: hvordan gjøre reglene enda mer gjenbrukbare/modulære, slik at de kan brukes for validering av også andre spesifikasjoner (SKOS-AP-NO, CPSV-AP-NO, ModellDCAT-AP-NO).

## Konsekvenser av resonnering, og hva som sjekkes

Reglene antar per nå at dersom typen deklareres i filen som valideres (datagrafen), altså med `rdf:type Class`, så kjøres validering for den klassen. Med andre ord vil all resonnering som utleder `rdf:type Class` aksiomer føre til at instansen valideres.

**AVKLARING:**

- Holder denne antakelsen?
- Vil det ha utilsiktede konsekvenser?
- Har vi definert `rdfs:domain` og `rdfs:range` aksiomer i noen sammenheng?

## Regelnavn

Er noe inkonsekvent nå.

**AVKLARING**: Hva tenker dere om navneutformingen? Forslag til alternativer?

### Regler for Klasser (NodeShapes):

I Core:
  
  `*_Shape`
  
  Eksempel: `Dataset_Shape`

I Range checks:
 
  `*RangesShape`

  Eksempel: `AgentRangesShape`

I Controlled Vocabularies checks:
  
  `*Shape-CV`
  
  Eksempel: `AgentShape-CV`

### Sjekk av egenskaper (PropertyShapes):

I Core:
  
  `hasNodeKindShape-*`
  
  `hasMinXMaxYShape-*`
  
  Eksempel: `hasNodeKindShape-dctAccrualPeriodicity` og `hasMin1MaxNShape-dctDescription`

I Range checks:

  `hasShapeCV-*Pattern`

  Eksempel: `hasShapeCV-languagePattern`

  `hasRangeShape-*` (disse sjekker typen med `sh:class`)

  Eksempel: `hasRangeShape-rights`

I Vocabularies checks:

  `hasShapeCV-*`

  Eksempel: `hasShapeCV-dctFormat`

I tillegg er det noen corner cases (f.eks. `dcat:theme`, hvor regelen `DataServiceShape-theme` sjekker at minimum én verdi er fra Data Theme dersom egenskapen brukes).

NodeKind-sjekk er egentlig upresist for regler som sjekker `sh:datatype`, gjør det noe?

## Formulering av feilmelding for nodeKind-sjekk

Jeg har prøvd å være konsekvent i feilmeldingene og brukt to mønstre:

`"The property xxxx may/MUST have min./max. X value"`

`"The value of property xxxx must be a Blank Node/URI/Literal"`

Denne formuleringen brukes i [SHACL](https://www.w3.org/TR/shacl/#NodeKindConstraintComponent):
"all values of ex:knows need to be IRIs"

Skal vi kalle det IRI eller URI?

Jeg foreslår URI, jeg tror det er mer intuitivt og velkjent enn "IRI". Jeg vil at de ansvarlige for beskrivelsen skal slippe å søke opp hva en IRI er om de får denne feilmeldingen, men umiddelbart skjønne at de må skrive en gyldig URI (eller URL). En URI er også en IRI. De svært RDF-kyndige som potensielt reagerer på dette kan dobbeltsjekke SHACL-reglene og se at den faktiske sjekken bruker IRI.

**AVKLARING:** Kalle det URI eller IRI i feilmeldingene?

## Alternativ til sh:class-sjekk

Jeg har fjernet svært mange av `sh:class <Class>`-sjekkene, siden disse kan være mer forvirrende enn til hjelp for bruker.
Særlig gjelder dette for eksterne ressurser man bare skal peke til (enheter i Brreg, dokumentasjonssider etc.).

Et alternativ er å gi Info om at klassen/typen ikke matcher som forventet. Men bør først avklare hva vi skal anta er inkludert (embedded) i filen og hva som ikke er inkludert.

## Ulike navn for egenskaper avhengig av klassen de er definert for

F.eks. heter `adms:status` "status" for Distribusjon, men "change type" for Catalogue Record. Men regelen gjenbrukes i begge. Hvilket navn (`sh:name`) skal regelen ha?


## Unik per språk (beskrivelse av Gebyr)

I spec'en står ingenting om at cv:Cost (Gebyr) må ha unik per språk, `sh:uniqueLang` på dct:description. Men den valideres nå med en regel som krever unik per språk.

**AVKLARING:** Er dette OK, eller har den ulik semantikk (ikke unik per språk)?

Skal `adms:VersionNotes` være unik per språk? Ikke definert i standarden nå.

## Blanke noder

Generelt har jeg vært noe mer restriktiv på blanke noder. I noen sammenhenger (f.eks. der dcat:Datasett relateres til andre dcat:Datasett) gir reglene feilmelding om man bruker blanke noder, selv om spesifikasjonene strengt tatt tillatter det. Bruk av blanke noder kompliserer implementering og bruk av metadataen.

**AVKLARING:** Enig i å være noe mer restriktiv på bruk av blanke noder?

**AVKLARING:** Skal vi tillate blanke noder for egenskapene listet under? (lurer særlig på dct:subject og prov:wasGeneratedBy)

| Egenskap                  | Tillate Blank Node (ja/nei) |
| ------------------------- | --------------------------- |
| dct:subject               | Ja?                         |
| prov:wasGeneratedBy       | Ja?                         |
| dct:type                  | Ja                          |
| dcat:distribution         | Ja                          |
| dcat:hadRole              | Ja                          |
| dcat:qualifiedRelation    | Ja                          |
| dct:provenance            | Ja                          |
| dct:rights                | Ja                          |
| dct:temporal              | Ja                          |
| prov:qualifiedAttribution | Ja                          |
| spdx:checksum             | Ja                          |


## Egenskapen prov:wasGeneratedBy og kontrollert vokabular

Hva hvis kode ikke er fra Proveniensaktivitetstype? Dette er potensielt en viktig egenskap for de som vurderer datasettene.

**AVKLARING:** Gi INFO eller WARNING om ikke fra Provenance Activity Type?

## Legal Resource

Er Legal Resource Type `dct:type` på eli:LegalResource egentlig et BØR-krav? I [spec'en](https://data.norge.no/specification/dcat-ap-no#RegulativRessurs-type) er formuleringen "Hvis verdien fins i vokabularet skal den brukes"?

## Contact Point

Skal vi sjekke at typen kan være kun en av Organization, Group eller Individual, men ikke flere av dem? Altså at kontaktpunkttypen er er disjunkt ("disjoint")?

### dcat:theme

Sjekker eksakt match på Data Theme i Core for Datasett. Jeg mener dette vil gjøre reglene mer brukervennlige. Om du skriver riktig rot path `http://publications.europa.eu/resource/authority/data-theme` men bommer på koden (f.eks. `http://publications.europa.eu/resource/authority/data-theme/WRONG`) bør du få tidlig beskjed om det. Listen er kort og krever per nå ikke mye vedlikehold å hardkode i reglene. Gir Warning nå.

**AVKLARING:** Enig eller uenig?

**AVKLARING:** (nummer 2) skal vi også gi advarsel om folk bruker `https://...` i koden? Per nå vil det ikke fanges opp.

## Type/nodeKind for dct:identifier

`dct:identifier` tillot tidligere sh:IRIOrLiteral. Har endret til `sh:nodeKind sh:Literal`

## Egenskapen dcatap:applicableLegislation

**AVKLARING:** `dcatap:applicableLegislation` skal vi gjøre Pattern-sjekk/Regex på at URI-en til ELI-ressursen er korrekt? F.eks. som Warning.

## Komplett conformance av SHACL-regler

Vil vi at SHACL-reglene skal være i komplett conformance med EU sin SHACL Shapes-validator (som validerer regelsettet)? Må legge til sh:name, sh:description og rdfs:comment på flere av NodeShapesene, og PropertyShapesene da, for å unngå Warnings.

**AVKLARING:** Komplett conformance på SHACL-reglene?

------------------------------------------------------------------------------------------------

## SPESIFIKASJONSRELATERT (DCAT-AP-NO v3)

### Vokabular Compress Format og Package Format (på Distribusjon)

DCAT og DCAT-AP sier at IANA Media Type skal brukes for egenskapene dcat:compressFormat og dcat:packageFormat. DCAT-AP-NO sier File Type.

**AVKLARE:** Skal vi bruke IANA Media Type eller EUs File Type?

### spatial - konflikt med DCAT-AP sin definisjon av egenskap

Vi tillater bruk av vokabularet Administrative Enheter. Gitt DCAT-AP sin klargjøring av semantikken, hvor dct:spatial er lukket under de angitte vokabularene (man kan KUN bruke koder fra vokabularene listet i DCAT-AP) er DCAT-AP-NO i konflikt med DCAT-AP.

### Forskjellen på dcat:hasVersion og dcat:version

Hva er forskjellen på `dcat:hasVersion` og `dcat:version` ? Tydeliggjøre i standarden.
For dcat:version: er dette versjonen for datasettet, eller beskrivelsen?

------------------------------------------------------------------------------------------------

## TILLEGGSINFORMASJON

### Utdypende om oppsplitting i Regelsett (Core/Ranges/Vocabularies)

Alt som sjekker ressurser fra tredjeparter bør plasseres utenfor Core.
Formål: Metadatatilbyder bør kunne validere beskrivelsen sin, f.eks. i eget system, og få feilmeldinger kun for de tingene tilbyder selv er ansvarlig for.

DCAT-AP-NO Core Shapes:
- Sjekker at obligatoriske egenskaper fins (minimums-kardinalitet).
- Sjekker at egenskaper ikke brukes for mange ganger (maksimums-kardinalitet).
- Sjekker at språk er unik for gitte egenskaper (sh:uniqueLang)
- Sjekker riktig verdi- og datatype (nodekind IRI/Blank Node/Literal eller sh:datatype for visse egenskaper)

DCAT-AP-NO Ranges Shapes:
- Sjekker at riktig vokabular brukes (ved hjelp av pattern. Trenger ikke laste inn eksterne ressurser)
  - Ikke fullstendig nøyaktig
- Sjekker typen til visse egenskaper (sh:class)
  - De klassene vi antar er inkludert (embedded) i datagrafen/filen som valideres.

DCAT-AP-NO Vocabularies Shapes:
- Sjekker kodene til de kontrollerte vokabularene som brukes (skos:inScheme)
  - Antakelig relevant kun for høstere som sammenstiller beskrivelsene med eksterne ressurser.


------------------------------------------------------------------------------------------------

## "Innenfor" og "utenfor" fil som valideres: Entity Types

Se til DCAT-AP Feeds' [definisjon](https://semiceu.github.io/LDES-DCAT-AP-feeds/index.html#types), de har definert tre typer entititer:

- Standalone entities
- Embedded entities
- Referenced entities

SHACL-reglene for DCAT-AP-NO v3 baserer seg også på denne distinksjonen. De ulike regelsettene gjør ulike antakelser om hva som er inkludert i filen/datagrafen som valideres.

DCAT-AP-NO sin kategorisering stemmer i stor grad overens med DCAT-AP Feeds sin kategorisering, med noen unntak (f.eks. dct:publiser -> foaf:Agent).

DCAT-AP Feeds sin kategorisering:

### Standalone entities

- dcat:Catalog
- dcat:Dataset
- dcat:Distribution
- dcat:DataService
- foaf:Agent (dct:publisher -> foaf:Agent er **Referenced** i DCAT-AP-NO!)
- vcard:Kind
- (dcterms:LicenseDocument) - only use this when you need to define licenses that are not well known.

### Embedded entities

- spdx:Checksum
- dcterms:Location (**Referenced?**)
- locn:Geometry
- dcat:Relationship
- prov:Activity (**Referenced** BØR-krav på prov:wasGeneratedBy -> prov:ActivityType i DCAT-AP-NO)
- dcat:Attribution
- spdx:ChecksumAlgorithm
- foaf:Document (??? Forstår ikke hvorfor denne er embedded)
- adms:Identifier

### Referenced entities

- dct:license pointing to entities that are expected to be typed as dcterms:LicenseDocument.
- a range of different properties pointing to skos:Concept (TODO, check which)
- dcat:themeTaxonomy pointing to an instance of skos:ConceptScheme
- dcterms:accrualPeriodicity pointing to dcterms:Frequency (or just a skos:Concept)
- dcterm:language pointing to an instance of dcterms:LinguisticSystem
- dcterms:format, dcat:mediaType, dcat:packageFormat or dcat:compressFormat pointing to a dcterms:MediaType instance
- dcterms:temporal pointing to a dcterms:PeriodOrTime instance
- odrl:hasPolicy pointing to a odrl:Policy instance
- dcterms:provenance pointing to a dcterms:ProvenanceStatement instance
- dcterms:rights pointing to an instance of dcterms:RightsStatement
- dcat:hadRole pointing to a dcat:Role instance
- dcterms:conformsTo pointing to a dcterms:Standard instance

## Skrive om hvordan valideringsreglene funker.

Har forsøkt å ha datatilbyder i fokus når vi har skrevet reglene. Reglene og feilmeldingene skal hjelpe datatilbyder å lage så gode beskrivelser som mulig.

Men det betyr at vi ikke får sjekket alt. Om du skriver feil URI til en ekstern ressurs, er ikke det noe SHACL-reglene kan finne ut av.

Reglene er altså *ikke komplett*, de fanger ikke opp alle feil. Men vi har forsøkt å gjøre de så konsistent som mulig, altså at de kun gir feilmelding når det er en reell feil.

For eksempel er det flere sjekker vi ikke gjør lenger, f.eks. `<dataset> foaf:page <http://example.com/datasett-dokumentasjon> .` Før sjekket vi at ressursen det ble pekt til var av type `foaf:Document`, men det er strengt tatt nettsiden ansvar selv å angi at det er av typen foaf:Document, ikke datatilbyder. Så dette sjekker vi ikke lenger.

Eksempel: sjekker AT du har brukt en URI og ikke bare en tekst, men kan ikke sjekke at du lenker til riktig ressurs/nettside/API.

Er avhengig av tredjeparter som tilbyr ressurser (f.eks. kodelistene fra EU/SEMIC, referanser til lover/reguleringer hos LovData) selv oppgir typen til ressursen.
Ikke noe poeng å validere mot dette, siden det ikke er datatilbyder sitt ansvar å oppgi typen til ressurser fra tredjeparter. Må nesten anta at de kontrollerte vokabularene vi henviser til er av riktig type, ellers hadde det ikke vært noe poeng at standarden krever at de brukes.

Der hvor det er krav til bruk av kontrollerte vokabularer sjekker vi at URL-en stemmer. Er fortsatt rom for å legge inn feil kode (f.eks. på dct:format).

### Vanlige feil:

Bør beskrives i dokumentasjon.

"Must be of type URI": har skrevet verdi med hermetegn `"` istedetfor som URI `< >` i Turtle, eller som `"@value"` i stedet for `"@id"` i JSON-LD.

## (IKKE OPPDATERT!) Instanser vi antar følger med fil (?)

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
- dcat:Catalog (for dct:hasPart)
- dcat:CatalogRecord (for dcat:record)
- dcat:CatalogRecord (for dct:source på CatalogRecord)
