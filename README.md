# Rankings Esportivos

Portal com rankings de varios esportes (GitHub Pages, atualizado automaticamente).
Estrutura SEM pastas para facilitar o envio pelo navegador.

## Arquivos
- index.html          -> menu inicial (le sports.json)
- sports.json         -> lista de esportes (ativos e "em breve")
- futebol.html        -> ranking de futebol (le futebol-data.json)
- futebol-data.json   -> dados do futebol
- update_futebol.py   -> robo do futebol (grava futebol-data.json)
- .github/workflows/update.yml -> roda, de hora em hora, todos os update_*.py da raiz

## Como adicionar um esporte X
1. Crie X.html (pagina) e X-data.json (dados iniciais).
2. Crie update_X.py, que grava X-data.json.
3. Em sports.json, acrescente/edite a entrada com status "ativo" e path "X.html".
O workflow ja roda qualquer update_*.py automaticamente.
