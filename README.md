# Ranking FIFA — Simulador de Confronto

Site que mostra o Ranking Mundial FIFA (masculino) e simula, para qualquer confronto,
quantos pontos e quantas posicoes cada selecao ganha ou perde em cada resultado.

## Como se mantem atualizado
- Os dados ficam no arquivo `data.json`.
- Uma rotina automatica do GitHub (`.github/workflows/update.yml`) roda uma vez por dia,
  executa `update_ranking.py`, busca o ranking mais recente e regrava `data.json`.
- A pagina (`index.html`) le esse arquivo toda vez que e aberta.

## Arquivos
- `index.html` — a pagina do simulador.
- `data.json` — os dados do ranking (atualizados pela rotina).
- `update_ranking.py` — o programa que busca os dados.
- `.github/workflows/update.yml` — o agendamento da rotina.

## Observacoes
- Os dados vem de football-ranking.com. Se o site de origem mudar de layout, a rotina
  pode falhar e `update_ranking.py` precisara de um pequeno ajuste.
- As variacoes de posicao sao estimativas; a pontuacao oficial da FIFA so muda nas datas
  de atualizacao do orgao.
