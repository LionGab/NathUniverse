-- LGPD compliant schema for WhatsApp lead activation
-- Base legal: Consentimento (Art. 7º, I, LGPD)

-- Table: leads
-- Purpose: Store lead data with explicit consent tracking
CREATE TABLE IF NOT EXISTS public.leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome TEXT NOT NULL,
    telefone TEXT NOT NULL UNIQUE,
    email TEXT,
    -- LGPD: explicit consent fields
    consentido BOOLEAN DEFAULT false NOT NULL,
    data_consentimento TIMESTAMPTZ,
    origem_consentimento TEXT, -- 'formulario_site', 'whatsapp', 'evento', etc
    -- WhatsApp activation tracking
    whatsapp_ativado BOOLEAN DEFAULT false NOT NULL,
    -- Opt-out tracking
    opt_out BOOLEAN DEFAULT false NOT NULL,
    data_opt_out TIMESTAMPTZ,
    -- Metadata
    criado_em TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    atualizado_em TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    -- Retention control (LGPD Art. 16)
    data_exclusao_programada TIMESTAMPTZ
);

COMMENT ON TABLE public.leads IS 'Leads com controle de consentimento LGPD';
COMMENT ON COLUMN public.leads.consentido IS 'Consentimento explícito para tratamento de dados pessoais';
COMMENT ON COLUMN public.leads.telefone IS 'Formato: +5565999999999 (DDI+DDD+número)';
COMMENT ON COLUMN public.leads.data_exclusao_programada IS 'Data para exclusão automática (retenção mínima)';

-- Table: whatsapp_envios
-- Purpose: Log all WhatsApp message attempts (LGPD audit trail)
CREATE TABLE IF NOT EXISTS public.whatsapp_envios (
    id SERIAL PRIMARY KEY,
    lead_id UUID NOT NULL REFERENCES public.leads(id) ON DELETE CASCADE,
    mensagem TEXT NOT NULL,
    status_envio TEXT NOT NULL, -- 'sucesso', 'falha', 'pendente'
    codigo_erro TEXT,
    resposta TEXT, -- response from WAHA API
    tentativa INTEGER DEFAULT 1,
    enviado_em TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    -- Metadata for audit
    workflow_execution_id TEXT,
    ip_origem INET
);

COMMENT ON TABLE public.whatsapp_envios IS 'Log de envios WhatsApp (LGPD Art. 37 - registro de operações)';
COMMENT ON COLUMN public.whatsapp_envios.status_envio IS 'Status: sucesso, falha, pendente';

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_leads_telefone ON public.leads(telefone);
CREATE INDEX IF NOT EXISTS idx_leads_consentido ON public.leads(consentido) WHERE consentido = true;
CREATE INDEX IF NOT EXISTS idx_leads_ativacao ON public.leads(whatsapp_ativado) WHERE whatsapp_ativado = false;
CREATE INDEX IF NOT EXISTS idx_leads_opt_out ON public.leads(opt_out) WHERE opt_out = true;
CREATE INDEX IF NOT EXISTS idx_envios_lead_id ON public.whatsapp_envios(lead_id);
CREATE INDEX IF NOT EXISTS idx_envios_status ON public.whatsapp_envios(status_envio);
CREATE INDEX IF NOT EXISTS idx_envios_data ON public.whatsapp_envios(enviado_em DESC);

-- Trigger: Update atualizado_em timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_leads_updated_at
    BEFORE UPDATE ON public.leads
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function: Normalize phone number to E.164 format
CREATE OR REPLACE FUNCTION normalize_telefone()
RETURNS TRIGGER AS $$
BEGIN
    -- Remove all non-numeric characters
    NEW.telefone := regexp_replace(NEW.telefone, '[^0-9]', '', 'g');

    -- Add +55 if not present (Brazilian DDI)
    IF NEW.telefone !~ '^\+?55' THEN
        IF length(NEW.telefone) = 11 THEN
            NEW.telefone := '+55' || NEW.telefone;
        ELSIF length(NEW.telefone) = 10 THEN
            NEW.telefone := '+55' || NEW.telefone;
        END IF;
    ELSE
        -- Ensure + prefix
        NEW.telefone := '+' || regexp_replace(NEW.telefone, '^\+', '', 'g');
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER normalize_telefone_trigger
    BEFORE INSERT OR UPDATE ON public.leads
    FOR EACH ROW
    EXECUTE FUNCTION normalize_telefone();

-- View: Leads ready for activation (LGPD compliant)
CREATE OR REPLACE VIEW public.leads_para_ativar AS
SELECT
    id,
    nome,
    telefone,
    email,
    data_consentimento,
    origem_consentimento
FROM public.leads
WHERE
    consentido = true
    AND whatsapp_ativado = false
    AND opt_out = false
    AND (data_exclusao_programada IS NULL OR data_exclusao_programada > NOW())
ORDER BY data_consentimento ASC
LIMIT 20;

COMMENT ON VIEW public.leads_para_ativar IS 'Leads prontos para ativação via WhatsApp (max 20/dia)';

-- Row Level Security (RLS) - Enable for production
-- ALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE public.whatsapp_envios ENABLE ROW LEVEL SECURITY;

-- Example RLS policy (adjust as needed):
-- CREATE POLICY "Service role can manage all leads"
-- ON public.leads FOR ALL
-- TO service_role
-- USING (true);

-- Function: Mark lead as opted out (LGPD compliance)
CREATE OR REPLACE FUNCTION opt_out_lead(p_telefone TEXT)
RETURNS void AS $$
BEGIN
    UPDATE public.leads
    SET
        opt_out = true,
        data_opt_out = NOW(),
        data_exclusao_programada = NOW() + INTERVAL '30 days'
    WHERE telefone = p_telefone;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION opt_out_lead IS 'Marca lead como opt-out e agenda exclusão (LGPD Art. 18, VI)';

-- Sample data for testing (optional - remove in production)
-- INSERT INTO public.leads (nome, telefone, email, consentido, data_consentimento, origem_consentimento)
-- VALUES
--     ('Lead Teste 1', '+5565999990001', 'teste1@example.com', true, NOW(), 'formulario_teste'),
--     ('Lead Teste 2', '+5565999990002', 'teste2@example.com', true, NOW(), 'formulario_teste'),
--     ('Lead Sem Consentimento', '+5565999990003', 'teste3@example.com', false, NULL, NULL);
