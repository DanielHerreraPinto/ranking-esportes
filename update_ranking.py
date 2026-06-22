#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Busca o ranking FIFA mais recente em football-ranking.com e regrava data.json.
Roda automaticamente no GitHub Actions. Se a fonte mudar de layout, este programa
pode precisar de ajuste — nesse caso, o robo falha de proposito e o data.json antigo
e mantido (nada e sobrescrito com dados incompletos)."""
import json, re, sys, datetime, urllib.request
try:
    import requests
except ImportError:
    requests = None
from bs4 import BeautifulSoup

PAGES = [
    "https://football-ranking.com/fifa-world-rankings",
    "https://football-ranking.com/fifa-rankings?page=2",
    "https://football-ranking.com/fifa-rankings?page=3",
    "https://football-ranking.com/fifa-rankings?page=4",
    "https://football-ranking.com/fifa-rankings?page=5",
]
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ranking-fifa-bot/1.0)"}

PT_NAMES = {"ARG": "Argentina", "FRA": "França", "ESP": "Espanha", "ENG": "Inglaterra", "BRA": "Brasil", "MAR": "Marrocos", "NED": "Países Baixos", "GER": "Alemanha", "POR": "Portugal", "BEL": "Bélgica", "MEX": "México", "COL": "Colômbia", "USA": "Estados Unidos", "ITA": "Itália", "CRO": "Croácia", "SEN": "Senegal", "JPN": "Japão", "URU": "Uruguai", "SUI": "Suíça", "DEN": "Dinamarca", "AUT": "Áustria", "IRN": "Irã", "KOR": "Coreia do Sul", "NGA": "Nigéria", "AUS": "Austrália", "NOR": "Noruega", "CAN": "Canadá", "ECU": "Equador", "EGY": "Egito", "ALG": "Argélia", "CIV": "Costa do Marfim", "TUR": "Turquia", "UKR": "Ucrânia", "RUS": "Rússia", "POL": "Polônia", "SWE": "Suécia", "PAR": "Paraguai", "WAL": "País de Gales", "HUN": "Hungria", "PAN": "Panamá", "SCO": "Escócia", "SRB": "Sérvia", "COD": "RD Congo", "CZE": "Tchéquia", "CMR": "Camarões", "SVK": "Eslováquia", "GRE": "Grécia", "VEN": "Venezuela", "CHI": "Chile", "PER": "Peru", "CRC": "Costa Rica", "ROU": "Romênia", "MLI": "Mali", "TUN": "Tunísia", "UZB": "Uzbequistão", "IRL": "Irlanda", "SVN": "Eslovênia", "QAT": "Catar", "KSA": "Arábia Saudita", "IRQ": "Iraque", "RSA": "África do Sul", "BFA": "Burkina Faso", "CPV": "Cabo Verde", "BIH": "Bósnia e Herzegovina", "GHA": "Gana", "HON": "Honduras", "ALB": "Albânia", "JOR": "Jordânia", "UAE": "Emirados Árabes Unidos", "MKD": "Macedônia do Norte", "NIR": "Irlanda do Norte", "JAM": "Jamaica", "GEO": "Geórgia", "ISL": "Islândia", "FIN": "Finlândia", "ISR": "Israel", "BOL": "Bolívia", "KOS": "Kosovo", "OMA": "Omã", "MNE": "Montenegro", "GUI": "Guiné", "NZL": "Nova Zelândia", "CUW": "Curaçao", "SYR": "Síria", "GAB": "Gabão", "BUL": "Bulgária", "HAI": "Haiti", "ANG": "Angola", "UGA": "Uganda", "ZAM": "Zâmbia", "CHN": "China", "BHR": "Bahrein", "BEN": "Benin", "THA": "Tailândia", "PLE": "Palestina", "BLR": "Belarus", "GUA": "Guatemala", "LUX": "Luxemburgo", "VIE": "Vietnã", "SLV": "El Salvador", "TJK": "Tajiquistão", "TRI": "Trinidad e Tobago", "MOZ": "Moçambique", "MAD": "Madagascar", "EQG": "Guiné Equatorial", "KGZ": "Quirguistão", "ARM": "Armênia", "COM": "Comores", "KEN": "Quênia", "LBY": "Líbia", "KAZ": "Cazaquistão", "TAN": "Tanzânia", "MTN": "Mauritânia", "NIG": "Níger", "LBN": "Líbano", "GAM": "Gâmbia", "SDN": "Sudão", "IDN": "Indonésia", "TOG": "Togo", "PRK": "Coreia do Norte", "NAM": "Namíbia", "SLE": "Serra Leoa", "FRO": "Ilhas Faroé", "CYP": "Chipre", "SUR": "Suriname", "AZE": "Azerbaijão", "EST": "Estônia", "RWA": "Ruanda", "MWI": "Malawi", "ZIM": "Zimbábue", "NCA": "Nicarágua", "GNB": "Guiné-Bissau", "KUW": "Kuwait", "CGO": "Congo", "PHI": "Filipinas", "MAS": "Malásia", "LVA": "Letônia", "IND": "Índia", "CTA": "República Centro-Africana", "LBR": "Libéria", "TKM": "Turcomenistão", "BDI": "Burundi", "ETH": "Etiópia", "DOM": "República Dominicana", "YEM": "Iêmen", "LES": "Lesoto", "BOT": "Botsuana", "SGP": "Singapura", "LTU": "Lituânia", "GUY": "Guiana", "NCL": "Nova Caledônia", "SKN": "São Cristóvão e Névis", "SOL": "Ilhas Salomão", "PUR": "Porto Rico", "FIJ": "Fiji", "HKG": "Hong Kong", "TAH": "Taiti", "MYA": "Mianmar", "MDA": "Moldávia", "VAN": "Vanuatu", "MLT": "Malta", "ATG": "Antígua e Barbuda", "GRN": "Granada", "CUB": "Cuba", "SWZ": "Essuatíni", "LCA": "Santa Lúcia", "BER": "Bermudas", "PNG": "Papua-Nova Guiné", "SSD": "Sudão do Sul", "VIN": "São Vicente e Granadinas", "AFG": "Afeganistão", "AND": "Andorra", "MDV": "Maldivas", "TPE": "Taipé Chinesa", "CAM": "Camboja", "MSR": "Montserrat", "NEP": "Nepal", "MRI": "Maurício", "BRB": "Barbados", "BLZ": "Belize", "BAN": "Bangladesh", "DMA": "Dominica", "CHA": "Chade", "ERI": "Eritreia", "LAO": "Laos", "COK": "Ilhas Cook", "SRI": "Sri Lanka", "SAM": "Samoa", "ARU": "Aruba", "MNG": "Mongólia", "ASA": "Samoa Americana", "BHU": "Butão", "MAC": "Macau", "BRU": "Brunei", "STP": "São Tomé e Príncipe", "DJI": "Djibuti", "CAY": "Ilhas Cayman", "PAK": "Paquistão", "SOM": "Somália", "TGA": "Tonga", "TLS": "Timor-Leste", "GIB": "Gibraltar", "GUM": "Guam", "SEY": "Seicheles", "TCA": "Ilhas Turcas e Caicos", "LIE": "Liechtenstein", "BAH": "Bahamas", "VIR": "Ilhas Virgens Americanas", "VGB": "Ilhas Virgens Britânicas", "AIA": "Anguilla", "SMR": "San Marino"}


def fetch(url):
    if requests is not None:
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.text
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "replace")

def parse_page(html):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for tr in soup.find_all("tr"):
        tds = tr.find_all("td")
        if len(tds) < 3:
            continue
        team_text = tds[1].get_text(" ", strip=True)
        mc = re.search(r"\(([A-Z]{2,3})\)", team_text)
        if not mc:
            continue
        code = mc.group(1)
        name_src = team_text[:mc.start()].strip()
        mp = re.search(r"(\d[\d.,]*\.\d{2})", tds[2].get_text(" ", strip=True))
        if not mp:
            continue
        pts = float(mp.group(1).replace(",", ""))
        rows.append((code, name_src, pts))
    return rows

def main():
    teams = {}
    for url in PAGES:
        for code, name_src, pts in parse_page(fetch(url)):
            teams[code] = (name_src, pts)  # dedupe por codigo
    if len(teams) < 150:
        sys.stderr.write("ERRO: apenas %d selecoes lidas - provavel mudanca no site. data.json NAO foi alterado.\n" % len(teams))
        sys.exit(1)
    ordered = sorted(teams.items(), key=lambda kv: kv[1][1], reverse=True)
    out_teams = [{"name": PT_NAMES.get(code, name_src), "code": code, "points": round(pts, 2)}
                 for code, (name_src, pts) in ordered]
    data = {
        "updated": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3))).strftime("%d/%m/%Y %H:%M (horário de Brasília)"),
        "source": "football-ranking.com",
        "teams": out_teams,
    }
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("OK: %d selecoes gravadas (topo %.2f)." % (len(out_teams), out_teams[0]["points"]))

if __name__ == "__main__":
    main()
