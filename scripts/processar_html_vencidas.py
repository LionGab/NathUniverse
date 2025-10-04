#!/usr/bin/env python3
"""
Processa arquivo HTML com tabela de matrículas vencidas
Gera SQL para inserir no Supabase
"""

import sys
import re
from datetime import datetime
from html.parser import HTMLParser

class TabelaHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_header = False
        self.in_cell = False
        self.headers = []
        self.rows = []
        self.current_row = []
        self.current_cell = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr':
            self.in_row = True
            self.current_row = []
        elif tag in ['th', 'td']:
            self.in_cell = True
            self.current_cell = ""
            if tag == 'th':
                self.in_header = True

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr':
            if self.in_row:
                if self.in_header and self.current_row:
                    self.headers = self.current_row.copy()
                    self.in_header = False
                elif self.current_row:
                    self.rows.append(self.current_row.copy())
                self.in_row = False
        elif tag in ['th', 'td']:
            if self.in_cell:
                self.current_row.append(self.current_cell.strip())
                self.current_cell = ""
                self.in_cell = False

    def handle_data(self, data):
        if self.in_cell:
            self.current_cell += data

def normalizar_telefone(telefone) -> str:
    """Normaliza telefone para +5565XXXXXXXXX"""
    if not telefone:
        return None

    # Remover formatação
    tel = re.sub(r'[^0-9]', '', telefone)

    # Adicionar DDI 55 se não tiver
    if not tel.startswith('55'):
        # Assumir DDD 65 (Mato Grosso) se não tiver
        if len(tel) == 8:
            tel = '65' + tel
        if len(tel) == 9:
            tel = '65' + tel
        tel = '55' + tel

    return '+' + tel

def processar_html(caminho: str):
    """Processa HTML e extrai dados"""
    print(f"Processando: {caminho}")

    try:
        with open(caminho, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()
    except Exception as e:
        print(f"ERRO ao ler arquivo: {e}")
        sys.exit(1)

    # Parsear HTML
    parser = TabelaHTMLParser()
    parser.feed(html_content)

    print(f"{len(parser.rows)} linhas encontradas")
    print(f"\nColunas: {', '.join(parser.headers)}")

    return parser.headers, parser.rows

def gerar_sql(headers, rows, arquivo_saida='inserir_vencidas.sql'):
    """Gera SQL para inserir no Supabase"""

    # Mapear colunas (assumindo estrutura típica)
    idx_nome = next((i for i, h in enumerate(headers) if 'nome' in h.lower()), 0)
    idx_celular = next((i for i, h in enumerate(headers) if 'celular' in h.lower()), 1)
    idx_email = next((i for i, h in enumerate(headers) if 'mail' in h.lower()), 2)

    print(f"\nMapeamento de colunas:")
    print(f"  Nome: coluna {idx_nome} ({headers[idx_nome]})")
    print(f"  Celular: coluna {idx_celular} ({headers[idx_celular]})")
    print(f"  Email: coluna {idx_email} ({headers[idx_email]})")

    sql_lines = [
        "-- SQL gerado automaticamente para inserir matrículas vencidas",
        f"-- Gerado em: {datetime.now().isoformat()}",
        f"-- Total de registros: {len(rows)}",
        "",
        "-- IMPORTANTE: Ajustar origem_consentimento conforme base legal real",
        ""
    ]

    processados = 0
    for row in rows:
        if len(row) <= max(idx_nome, idx_celular, idx_email):
            continue

        nome = row[idx_nome].replace("'", "''").strip()
        telefone_raw = row[idx_celular].strip() if idx_celular < len(row) else ""
        email = row[idx_email].replace("'", "''").strip() if idx_email < len(row) else ""

        # Normalizar telefone
        telefone = normalizar_telefone(telefone_raw)

        if not nome or not telefone:
            continue

        sql = f"""INSERT INTO public.leads (nome, telefone, email, consentido, data_consentimento, origem_consentimento)
VALUES ('{nome}', '{telefone}', '{email}', true, NOW(), 'sistema_matriculas_vencidas')
ON CONFLICT (telefone) DO UPDATE SET
    nome = EXCLUDED.nome,
    email = EXCLUDED.email,
    consentido = EXCLUDED.consentido,
    data_consentimento = EXCLUDED.data_consentimento;
"""
        sql_lines.append(sql)
        processados += 1

    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines))

    print(f"\nSQL gerado: {arquivo_saida}")
    print(f"{processados} registros prontos para inserir")
    return arquivo_saida

def gerar_preview(headers, rows, limite=10):
    """Exibe preview dos dados"""
    print("\n" + "="*80)
    print(f"PREVIEW - Primeiras {limite} matrículas vencidas")
    print("="*80)

    idx_nome = next((i for i, h in enumerate(headers) if 'nome' in h.lower()), 0)
    idx_celular = next((i for i, h in enumerate(headers) if 'celular' in h.lower()), 1)
    idx_email = next((i for i, h in enumerate(headers) if 'mail' in h.lower()), 2)

    for i, row in enumerate(rows[:limite], 1):
        if len(row) <= max(idx_nome, idx_celular):
            continue

        nome = row[idx_nome] if idx_nome < len(row) else 'N/A'
        telefone_raw = row[idx_celular] if idx_celular < len(row) else 'N/A'
        telefone = normalizar_telefone(telefone_raw)

        print(f"{i}. {nome} | {telefone} | {telefone_raw}")

    print("="*80)
    print(f"\nTotal: {len(rows)} registros")
    print()

def main():
    # Caminho padrão
    caminho = r"C:\Users\User\Downloads\ModeloVencidas.xlsx"

    if len(sys.argv) > 1:
        caminho = sys.argv[1]

    print("Processador de Matriculas Vencidas (HTML)")
    print(f"Arquivo: {caminho}\n")

    # Processar HTML
    headers, rows = processar_html(caminho)

    if not rows:
        print("Nenhuma linha de dados encontrada")
        return

    # Preview
    gerar_preview(headers, rows)

    # Gerar SQL
    sql_file = gerar_sql(headers, rows, 'inserir_vencidas.sql')

    print("\nPROXIMOS PASSOS:")
    print("1. Revise o arquivo gerado: inserir_vencidas.sql")
    print("2. Acesse o Supabase SQL Editor")
    print("3. Cole e execute o SQL")
    print("4. Verifique: SELECT * FROM leads WHERE origem_consentimento = 'sistema_matriculas_vencidas';")
    print()
    print("IMPORTANTE LGPD: Confirme que esses alunos consentiram receber mensagens!")

if __name__ == '__main__':
    main()
