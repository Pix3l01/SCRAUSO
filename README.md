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

### Configurazione
Il file di configurazione è scritto in [TOML](https://toml.io/)<br>
Al momento è necessario inserire e inizializzare tutti i parametri indipendentemente dal metodo utilizzato
```
[general]
db = "string" # Path del file database
port = int # Porta utilizzata dal submitter per ricevere le flag da inviare

[sender]
sender = "string" # Tipo di sender da utilizzare. Al momento: "forcADsender" e "ncsender"
link = "string" # link del submission server (inizializzarlo anche se non utilizzato)
token = "string" # Token (inizializzarlo anche se non utilizzato)
ip = "string" # ip del submission server (inizializzarlo anche se non utilizzato)
port = int # Porta del submission server (inizializzarlo anche se non utilizzato)
```

## Status codes
- 0: flag non ancora submittata
- 1: flag submittata e accettata
- 2: flag submittata e respinta (vecchia)
- 3: flag submittata e respinta (non valida)
- 4: flag submittata e respinta (già inviata) 
