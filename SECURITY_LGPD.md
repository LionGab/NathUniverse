# Conformidade LGPD - Política de Tratamento de Dados

## Base Legal

Este sistema processa dados pessoais com base no **Consentimento** (Art. 7º, I, LGPD - Lei nº 13.709/2018).

## Dados Tratados

### Dados Pessoais Coletados
- Nome completo
- Número de telefone (WhatsApp)
- E-mail (opcional)
- Data e origem do consentimento
- Histórico de mensagens enviadas

### Finalidade do Tratamento
Envio de mensagens de ativação via WhatsApp para leads que consentiram explicitamente em receber comunicações.

---

## Consentimento Explícito

### Requisitos Obrigatórios
1. **Transparência**: O titular deve ser informado sobre:
   - Quais dados serão coletados
   - Finalidade do uso
   - Possibilidade de revogar consentimento

2. **Clareza**: Linguagem simples e acessível

3. **Granularidade**: Consentimento específico para envio via WhatsApp

### Exemplo de Termo de Consentimento
```
[ ] Autorizo o recebimento de mensagens via WhatsApp para ativação
    e comunicações relacionadas ao serviço [NOME DA EMPRESA].

    Estou ciente de que posso cancelar a qualquer momento respondendo
    "PARAR" ou solicitando via [EMAIL DE CONTATO].

    Li e aceito a Política de Privacidade.
```

### Registro no Sistema
```sql
INSERT INTO public.leads (
    nome,
    telefone,
    consentido,
    data_consentimento,
    origem_consentimento
) VALUES (
    'Nome do Lead',
    '+5565999999999',
    true,
    NOW(),
    'formulario_site' -- ou 'evento', 'whatsapp', etc
);
```

---

## Direitos do Titular (Art. 18, LGPD)

### 1. Confirmação e Acesso
**Consultar dados armazenados:**
```sql
SELECT
    nome,
    telefone,
    email,
    consentido,
    data_consentimento,
    whatsapp_ativado,
    opt_out
FROM public.leads
WHERE telefone = '+5565999999999';
```

### 2. Correção
**Atualizar dados incorretos:**
```sql
UPDATE public.leads
SET
    nome = 'Nome Corrigido',
    email = 'novo@email.com'
WHERE telefone = '+5565999999999';
```

### 3. Anonimização/Bloqueio/Eliminação
**Excluir completamente:**
```sql
DELETE FROM public.leads WHERE telefone = '+5565999999999';
-- Cascata automática remove logs em whatsapp_envios
```

**Anonimizar (alternativa):**
```sql
UPDATE public.leads
SET
    nome = 'ANONIMIZADO',
    email = NULL,
    telefone = 'REMOVED',
    opt_out = true
WHERE telefone = '+5565999999999';
```

### 4. Portabilidade
**Exportar dados em JSON:**
```sql
SELECT row_to_json(t)
FROM (
    SELECT l.*,
           (SELECT json_agg(e) FROM public.whatsapp_envios e WHERE e.lead_id = l.id) AS envios
    FROM public.leads l
    WHERE l.telefone = '+5565999999999'
) t;
```

### 5. Revogação de Consentimento (Opt-Out)
**Procedimento padrão:**
```sql
SELECT opt_out_lead('+5565999999999');
```

**Efeito:**
- `opt_out = true`
- `data_opt_out = NOW()`
- `data_exclusao_programada = NOW() + 30 dias`
- Lead não aparece mais em `leads_para_ativar`

---

## Opt-Out Automático via WhatsApp

### Implementação Recomendada

1. **Criar webhook no WAHA** para receber mensagens
2. **Filtrar palavra-chave** ("PARAR", "CANCELAR", "SAIR")
3. **Executar opt-out** automaticamente

### Exemplo de Endpoint (Node.js/Express)
```javascript
app.post('/webhook/waha', async (req, res) => {
    const { from, body } = req.body;

    if (body.toUpperCase().includes('PARAR')) {
        await supabase.rpc('opt_out_lead', {
            p_telefone: `+${from.replace('@c.us', '')}`
        });

        // Enviar confirmação
        await waha.sendText({
            chatId: from,
            text: 'Você foi removido da lista. Seus dados serão excluídos em 30 dias.'
        });
    }

    res.sendStatus(200);
});
```

---

## Retenção e Descarte de Dados

### Política de Retenção
- **Leads ativos**: mantidos enquanto `consentido = true`
- **Leads opt-out**: agendados para exclusão em 30 dias
- **Logs de envio**: mantidos por 90 dias (auditoria)

### Exclusão Automática (Job Mensal)
```sql
-- Excluir leads com data_exclusao_programada vencida
DELETE FROM public.leads
WHERE data_exclusao_programada IS NOT NULL
  AND data_exclusao_programada < NOW();

-- Limpar logs antigos
DELETE FROM public.whatsapp_envios
WHERE enviado_em < NOW() - INTERVAL '90 days';
```

### Agendar no Cron (Linux)
```bash
# Executar todo dia 1º às 02:00
0 2 1 * * psql $DATABASE_URL -c "DELETE FROM public.leads WHERE data_exclusao_programada < NOW();"
```

---

## Segurança Técnica

### 1. Controle de Acesso (RLS - Row Level Security)
```sql
ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.whatsapp_envios ENABLE ROW LEVEL SECURITY;

-- Somente service_role pode acessar
CREATE POLICY "service_role_all_access"
ON public.leads FOR ALL
TO service_role
USING (true);
```

### 2. Criptografia
- **Em trânsito**: HTTPS obrigatório (Supabase padrão)
- **Em repouso**: Criptografia AES-256 (Supabase padrão)

### 3. Logs de Auditoria
Tabela `whatsapp_envios` registra:
- Quem recebeu (`lead_id`)
- Quando (`enviado_em`)
- Resultado (`status_envio`, `resposta`)

### 4. Credenciais
- **Nunca** commitar `.env` com credenciais
- Usar variáveis de ambiente
- Rotacionar `service_role` periodicamente

---

## Documentação Obrigatória

### Registro de Atividades de Tratamento (ROPA)
**Agente de tratamento**: [NOME DA EMPRESA]
**DPO/Encarregado**: [NOME E CONTATO]

| Campo | Informação |
|-------|-----------|
| Dados tratados | Nome, telefone, e-mail |
| Finalidade | Envio de mensagens de ativação WhatsApp |
| Base legal | Consentimento (Art. 7º, I) |
| Categorias de titulares | Leads/prospects |
| Compartilhamento | WAHA (processador), Supabase (subprocessador) |
| Prazo de retenção | Até revogação + 30 dias |
| Medidas de segurança | HTTPS, RLS, logs de auditoria |

---

## Avisos de Privacidade

### Texto Sugerido nas Mensagens WhatsApp
```
Você autorizou o recebimento desta mensagem em [DATA_CONSENTIMENTO].
Para cancelar, responda PARAR.
```

### Link para Política de Privacidade
Inclua em todas as comunicações:
```
📄 Política de Privacidade: https://seusite.com/privacidade
```

---

## Checklist de Conformidade

- [ ] Termo de consentimento claro e específico
- [ ] Registro de data e origem do consentimento
- [ ] Procedimento de opt-out implementado
- [ ] Exclusão automática após opt-out (30 dias)
- [ ] RLS habilitado no Supabase
- [ ] Logs de auditoria configurados
- [ ] ROPA documentado e atualizado
- [ ] DPO/Encarregado designado
- [ ] Política de Privacidade publicada
- [ ] Treinamento de equipe sobre LGPD

---

## Contato DPO

**E-mail**: [dpo@suaempresa.com]
**Telefone**: [XX XXXXX-XXXX]

Titulares podem exercer seus direitos enviando solicitação formal para este contato.

---

## Referências Legais

- **Lei nº 13.709/2018** - Lei Geral de Proteção de Dados
- **Art. 7º, I** - Consentimento
- **Art. 18** - Direitos do titular
- **Art. 37** - Segurança e registro de operações
- **Art. 46** - Retenção mínima de dados

**Última atualização**: 2025-01-03
