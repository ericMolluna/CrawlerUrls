# Web Crawler per a Errors 4XX

Aquest projecte és un crawler web que explora un lloc per detectar enllaços amb errors 4XX (errors de client). Quan troba un error, registra l'URL amb l'error i la referència en un fitxer CSV.

## Com funciona?

1. **Exploració de Pàgines**  
   El crawler recorre les pàgines de manera recursiva i busca tots els enllaços. Quan troba un, comprova si té algun error 4XX (com 404, 403, etc.).

2. **Comprovació d'Errors**  
   Per cada enllaç trobat, es fa una petició per veure si retorna un error 4XX. Si és així, s'afegeix a la llista d'errors.

3. **Informe d'Errors**  
   Els errors es guarden en un fitxer CSV amb l'URL erroni, el codi d'error i la URL d'on prové.

## Requisits

- Python 3.x
- Firefox i GeckoDriver
- Llibreries:
  - `selenium`
  - `beautifulsoup4`
  - `requests`
  - `csv`

## Instal·lació

1. Instal·la les dependències:
    ```bash
    pip install selenium beautifulsoup4 requests
    ```

2. Descarrega i configura [GeckoDriver](https://github.com/mozilla/geckodriver) per a Firefox.

## Ús

1. Executa el script. El crawler començarà a explorar des de la URL inicial.
   
2. Quan acabi, generarà un fitxer `errors_4xx_report.csv` amb tots els errors trobats.

## Decisions de Disseny

- **Selenium amb Firefox**: Es fa servir per carregar pàgines amb JavaScript i obtenir els enllaços.
- **Exploració Recursiva**: El crawler segueix els enllaços fins a una profunditat màxima o fins a arribar al nombre límit de pàgines.
- **Concorrent**: Per millorar la velocitat, es fa servir múltiples fils per verificar els enllaços.

## Limitacions

- El nombre de pàgines explorades és limitat (50 per defecte).
- El crawler no gestiona bé alguns errors de xarxa.
