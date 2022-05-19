# S.C.R.A.U.S.O.

><strong>S.</strong>C.R.A.U.S.O.<br>
**C**ontorto  
**R**affazzonato  
**A**bbastanza  
**U**tilizzabile  
**S**ubmitter  
**O**ligominerale  

- Penso il nome sia abbastanza esplicativo
- Sono accettati suggerimenti per la "O"

## Utilizzo

### Setup
```
git clone https://github.com/Pix3l01/SCRAUSO.git
cd SCRAUSO/
pip3 install -r requirements.txt
```

### Avvio
```
python3 main.py "path/to/config"
```

### Docker
```
docker-compose up -d
```
Per modificare la porta esposta dal docker nel file ```docker-compose.yaml``` 
modificare il campo ```ports``` da ```5000:5000``` a ```NUOVA_PORTA:5000``` 
(non modificarla nel file di configurazione)

### Configurazione
Il file di configurazione è scritto in [TOML](https://toml.io/) <br>
Al momento è necessario inserire e inizializzare tutti i parametri indipendentemente dal metodo utilizzato
```
[general]
db = "string" # Path del file database
ip = "string" # IP of flask server
port = int # Porta utilizzata dal submitter per ricevere le flag da inviare
scheduled_check = int # seconds of interval between checks for leftovers flags

[sender]
sender = "string" # Tipo di sender da utilizzare. Al momento: "forcADsender" e "ncsender"
link = "string" # link del submission server
token = "string" # Token (inizializzarlo anche se non utilizzato)
ip = "string" # ip del submission server
host = "string" # IP o url del submission server
port = int # Porta del submission server
```

## Status codes
- 0: flag non ancora submittata
- 1: flag submittata e accettata
- 2: flag submittata e respinta (vecchia)
- 3: flag submittata e respinta (non valida)
- 4: flag submittata e respinta (già inviata)
- 5: flag submittata e respinta (NOP team)
- 6: flag submittata e respinta (flag del tuo team)
- 99: flag submittata e respinta (altro aka malissimo) 
