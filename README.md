# Fantacitorio Telegram bot

@fantacitorio_bot

Dovevo imparare a usare python e ho pensato di fare questo bot. Il codice non è ottimizzato, ma funziona (solo per la nostra fantalega, se qualcun altro volesse utilizzarlo dovrebbe clonarlo e creare un nuovo bot, a meno che non modifichi questo).

Il programma legge le squadre da tre diversi file.txt, legge `punteggio.txt` con tutti i punteggi assegnati da [Propaganda Live](https://www.la7.it/propagandalive/video/fantacitorio-16-02-2022-423442). Il bot ha i comandi per mostrare le squadre, i punteggi di ogni politico e la classifica in ordine con i punteggi delle squadre.

## To Do
- far si che funzioni per qualsiasi fantalega e qualsiasi squadra singola

```
snscrape --jsonl --progress --max-results 4 twitter-search "from:Fanta_citorio" > tweets.json && cat tweets.json | jq '.content' > data.txt
```
