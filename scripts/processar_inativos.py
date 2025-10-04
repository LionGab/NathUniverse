#!/usr/bin/env python3
"""
Processa planilha waha-n8n-stackModeloVencidas.xlsx e cria lista priorizada
Gera SQL para inserir no Supabase
"""

import sys
import os
from datetime import datetime
from pathlib import Path

try:
    import openpyxl
    import pandas as pd
except ImportError:
    print("❌ ERRO: Instale as dependências primeiro:")
    print("pip install openpyxl pandas")
    sys.exit(1)


def normalizar_telefone(telefone) -> str:
    """Normaliza telefone para +5565XXXXXXXXX"""
    if pd.isna(telefone):
        return None

    # Converter para string e remover formatação
    tel = str(telefone).strip()
    tel = ''.join(filter(str.isdigit, tel))

    # Adicionar DDI 55 se não tiver
    if not tel.startswith('55'):
        # Assumir DDD 65 (Mato Grosso) se não tiver
        if len(tel) == 8:
            tel = '65' + tel
        if len(tel) == 9:
            tel = '65' + tel
        tel = '55' + tel

    return '+' + tel


def calcular_prioridade(row) -> int:
    """
    Calcula prioridade de reativação (1-5, sendo 5 mais urgente)
    Critérios:
    - Última atividade (mais recente = maior prioridade)
    - Número de aulas feitas (mais aulas = maior prioridade)
    - Valor do plano (maior valor = maior prioridade)
    """
    score = 0

    # Critério 1: Última atividade (assumindo coluna "Ultima_Atividade" ou similar)
    # (ajuste conforme colunas reais da planilha)

    # Critério 2: Engajamento anterior
    # (ajuste conforme dados disponíveis)

    # Por enquanto, retorna aleatório para exemplo
    # AJUSTAR após ver estrutura real da planilha
    return 3


def processar_planilha(caminho_xlsx: str) -> pd.DataFrame:
    """Processa planilha e retorna DataFrame priorizado"""

    if not os.path.exists(caminho_xlsx):
        print(f"❌ Arquivo não encontrado: {caminho_xlsx}")
        sys.exit(1)

    print(f"📂 Processando: {caminho_xlsx}")

    # Ler Excel
    try:
        df = pd.read_excel(caminho_xlsx)
        print(f"✅ {len(df)} linhas carregadas")
    except Exception as e:
        print(f"❌ Erro ao ler Excel: {e}")
        sys.exit(1)

    # Exibir colunas disponíveis
    print(f"\n📋 Colunas encontradas:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")

    # AJUSTAR AQUI: Mapear colunas reais
    # Assumindo colunas padrão (ajuste conforme sua planilha)
    coluna_nome = df.columns[0] if len(df.columns) > 0 else None
    coluna_telefone = df.columns[1] if len(df.columns) > 1 else None
    coluna_email = df.columns[2] if len(df.columns) > 2 else None

    print(f"\n🔍 Mapeamento assumido:")
    print(f"  Nome: {coluna_nome}")
    print(f"  Telefone: {coluna_telefone}")
    print(f"  Email: {coluna_email}")

    # Normalizar telefones
    if coluna_telefone:
        df['telefone_normalizado'] = df[coluna_telefone].apply(normalizar_telefone)

    # Calcular prioridade
    df['prioridade'] = df.apply(calcular_prioridade, axis=1)

    # Ordenar por prioridade (maior primeiro)
    df = df.sort_values('prioridade', ascending=False)

    # Limitar a 30 (conforme solicitado)
    df_top = df.head(30)

    print(f"\n✅ Top 30 inativos priorizados")
    return df_top


def gerar_sql(df: pd.DataFrame, arquivo_saida: str = 'inserir_inativos.sql'):
    """Gera arquivo SQL para inserir no Supabase"""

    sql_lines = [
        "-- SQL gerado automaticamente para inserir alunos inativos",
        f"-- Gerado em: {datetime.now().isoformat()}",
        "-- Total de registros: {}".format(len(df)),
        "",
        "-- IMPORTANTE: Ajustar origem_consentimento conforme base legal real",
        ""
    ]

    for idx, row in df.iterrows():
        # Pegar nome da primeira coluna (ajustar conforme planilha real)
        nome = str(row[df.columns[0]]).replace("'", "''") if not pd.isna(row[df.columns[0]]) else 'N/A'
        telefone = row.get('telefone_normalizado', None)
        email = str(row[df.columns[2]]).replace("'", "''") if len(df.columns) > 2 and not pd.isna(row[df.columns[2]]) else None

        if not telefone:
            continue

        sql = f"""INSERT INTO public.leads (nome, telefone, email, consentido, data_consentimento, origem_consentimento)
VALUES ('{nome}', '{telefone}', '{"" if not email else email}', true, NOW(), 'planilha_inativos')
ON CONFLICT (telefone) DO UPDATE SET
    nome = EXCLUDED.nome,
    email = EXCLUDED.email,
    consentido = EXCLUDED.consentido,
    data_consentimento = EXCLUDED.data_consentimento;
"""
        sql_lines.append(sql)

    # Salvar arquivo
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sql_lines))

    print(f"\n✅ SQL gerado: {arquivo_saida}")
    print(f"📊 {len(df)} registros prontos para inserir")
    return arquivo_saida


def gerar_preview(df: pd.DataFrame):
    """Exibe preview dos dados"""
    print("\n" + "="*80)
    print("PREVIEW - Top 10 Alunos Inativos Priorizados")
    print("="*80)

    for idx, row in df.head(10).iterrows():
        nome = row[df.columns[0]]
        telefone = row.get('telefone_normalizado', 'N/A')
        prioridade = row.get('prioridade', 0)

        print(f"{idx+1}. {nome} | {telefone} | Prioridade: {prioridade}")

    print("="*80)
    print(f"\nTotal selecionado: {len(df)} alunos")
    print()


def main():
    # Caminho padrão (ajustar se necessário)
    caminho_xlsx = r"C:\Users\User\Downloads\waha-n8n-stackModeloVencidas.xlsx"

    if len(sys.argv) > 1:
        caminho_xlsx = sys.argv[1]

    print("🚀 Processador de Alunos Inativos")
    print(f"📁 Arquivo: {caminho_xlsx}\n")

    # Processar
    df = processar_planilha(caminho_xlsx)

    # Preview
    gerar_preview(df)

    # Gerar SQL
    sql_file = gerar_sql(df, 'inserir_inativos.sql')

    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Revise o arquivo gerado: inserir_inativos.sql")
    print("2. Acesse o Supabase SQL Editor")
    print("3. Cole e execute o SQL")
    print("4. Verifique: SELECT * FROM leads WHERE origem_consentimento = 'planilha_inativos';")
    print()
    print("⚠️  IMPORTANTE LGPD: Confirme que esses alunos consentiram receber mensagens!")


if __name__ == '__main__':
    main()
