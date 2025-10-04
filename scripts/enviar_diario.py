#!/usr/bin/env python3
"""
Script para envio diário de mensagens WhatsApp via WAHA
Alternativa simples ao n8n para até 30 leads/dia
LGPD compliant - requer consentimento prévio
"""

import os
import sys
from datetime import datetime
import requests
from supabase import create_client, Client

# Configuração via variáveis de ambiente
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_ROLE')
WAHA_URL = os.getenv('WAHA_BASE_URL', 'http://localhost:3000')
WAHA_PATH = os.getenv('WAHA_SEND_TEXT_PATH', '/api/sendText')
WAHA_SESSION = os.getenv('WAHA_SESSION', 'default')
WAHA_API_KEY = os.getenv('WAHA_API_KEY')
LIMITE_DIARIO = int(os.getenv('LIMITE_DIARIO', '30'))

# Template de mensagem (personalizável)
MENSAGEM_TEMPLATE = """Olá {nome}! 👋

Notamos que você está inativo há algum tempo. Estamos com novidades e gostaríamos de reconectá-lo!

Para cancelar mensagens futuras, responda PARAR.

---
Você autorizou o recebimento em {data_consentimento}."""


def validar_ambiente():
    """Valida se as variáveis de ambiente estão configuradas"""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ ERRO: Configure SUPABASE_URL e SUPABASE_SERVICE_ROLE")
        sys.exit(1)

    if not WAHA_URL:
        print("❌ ERRO: Configure WAHA_BASE_URL")
        sys.exit(1)

    print("✅ Variáveis de ambiente validadas")


def inicializar_supabase() -> Client:
    """Inicializa cliente Supabase"""
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conectado ao Supabase")
        return supabase
    except Exception as e:
        print(f"❌ Erro ao conectar Supabase: {e}")
        sys.exit(1)


def buscar_leads(supabase: Client) -> list:
    """Busca leads prontos para ativação (LGPD compliant)"""
    try:
        # Query usando a view otimizada
        response = supabase.table('leads_para_ativar').select('*').limit(LIMITE_DIARIO).execute()

        leads = response.data
        print(f"📋 {len(leads)} leads encontrados para envio")
        return leads

    except Exception as e:
        print(f"❌ Erro ao buscar leads: {e}")
        return []


def normalizar_chat_id(telefone: str) -> str:
    """
    Converte telefone para formato WAHA
    Input: +5565999999999
    Output: 5565999999999@c.us
    """
    # Remove + e adiciona sufixo WAHA
    return telefone.replace('+', '') + '@c.us'


def enviar_whatsapp(lead: dict) -> dict:
    """Envia mensagem via WAHA API"""
    chat_id = normalizar_chat_id(lead['telefone'])

    # Formatar data de consentimento
    data_consent = lead.get('data_consentimento', 'data não registrada')
    if data_consent:
        try:
            dt = datetime.fromisoformat(data_consent.replace('Z', '+00:00'))
            data_consent = dt.strftime('%d/%m/%Y')
        except:
            pass

    # Gerar mensagem personalizada
    mensagem = MENSAGEM_TEMPLATE.format(
        nome=lead['nome'],
        data_consentimento=data_consent
    )

    payload = {
        'chatId': chat_id,
        'text': mensagem,
        'session': WAHA_SESSION
    }

    try:
        url = f"{WAHA_URL}{WAHA_PATH}"
        headers = {'X-Api-Key': WAHA_API_KEY} if WAHA_API_KEY else {}
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        print(f"✅ Enviado para {lead['nome']} ({lead['telefone']})")
        return {
            'sucesso': True,
            'resposta': response.json(),
            'status': 'sucesso'
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao enviar para {lead['nome']}: {e}")
        return {
            'sucesso': False,
            'erro': str(e),
            'status': 'falha'
        }


def registrar_envio(supabase: Client, lead: dict, resultado: dict):
    """Registra log de envio no Supabase (auditoria LGPD)"""
    try:
        log_data = {
            'lead_id': lead['id'],
            'mensagem': MENSAGEM_TEMPLATE.format(
                nome=lead['nome'],
                data_consentimento='...'
            ),
            'status_envio': resultado['status'],
            'resposta': str(resultado.get('resposta', resultado.get('erro', ''))),
            'codigo_erro': resultado.get('erro', None)
        }

        supabase.table('whatsapp_envios').insert(log_data).execute()
        print(f"📝 Log registrado para {lead['nome']}")

    except Exception as e:
        print(f"⚠️  Erro ao registrar log: {e}")


def marcar_como_ativado(supabase: Client, lead_id: str):
    """Marca lead como whatsapp_ativado=true"""
    try:
        supabase.table('leads').update({
            'whatsapp_ativado': True
        }).eq('id', lead_id).execute()

        print(f"✅ Lead {lead_id} marcado como ativado")

    except Exception as e:
        print(f"⚠️  Erro ao marcar lead: {e}")


def main():
    """Fluxo principal de execução"""
    print("🚀 Iniciando envio diário de WhatsApp")
    print(f"⏰ Timestamp: {datetime.now().isoformat()}")
    print(f"🎯 Limite: {LIMITE_DIARIO} mensagens\n")

    # 1. Validar ambiente
    validar_ambiente()

    # 2. Conectar Supabase
    supabase = inicializar_supabase()

    # 3. Buscar leads
    leads = buscar_leads(supabase)

    if not leads:
        print("ℹ️  Nenhum lead para enviar hoje")
        return

    # 4. Processar cada lead
    sucesso_count = 0
    erro_count = 0

    for i, lead in enumerate(leads, 1):
        print(f"\n📤 [{i}/{len(leads)}] Processando {lead['nome']}...")

        # Enviar WhatsApp
        resultado = enviar_whatsapp(lead)

        # Registrar log (sempre, sucesso ou erro)
        registrar_envio(supabase, lead, resultado)

        # Marcar como ativado apenas se sucesso
        if resultado['sucesso']:
            marcar_como_ativado(supabase, lead['id'])
            sucesso_count += 1
        else:
            erro_count += 1

    # 5. Resumo final
    print("\n" + "="*50)
    print(f"✅ Concluído!")
    print(f"📊 Sucessos: {sucesso_count}")
    print(f"❌ Erros: {erro_count}")
    print(f"📝 Total processado: {len(leads)}")
    print("="*50)


if __name__ == '__main__':
    main()
