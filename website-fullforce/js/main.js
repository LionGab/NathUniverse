// Configuração - Atualize com suas credenciais
const CONFIG = {
    supabaseUrl: 'https://oprrsfeljeyuebqarhjn.supabase.co',
    supabaseKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9wcnJzZmVsamV5dWVicWFyaGpuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1Mjc3NjgsImV4cCI6MjA3NTEwMzc2OH0.6hQngVyKniCVXHs4C9586yWavPToYZ0XZNuFzfBUFFg',
    whatsappNumber: '5566999999999', // Atualize com o número da academia
    wahaUrl: 'https://your-waha-url.up.railway.app' // Atualize com URL do WAHA
};

// Menu Mobile
function toggleMenu() {
    const navMenu = document.querySelector('.nav-menu');
    navMenu.style.display = navMenu.style.display === 'flex' ? 'none' : 'flex';
}

// Scroll suave para seção de planos
function scrollToPlanos() {
    document.getElementById('planos').scrollIntoView({ behavior: 'smooth' });
}

// Abrir WhatsApp
function openWhatsApp() {
    const message = encodeURIComponent('Olá! Gostaria de agendar minha aula grátis na Full Force Academia.');
    window.open(`https://wa.me/${CONFIG.whatsappNumber}?text=${message}`, '_blank');
}

// Selecionar plano e abrir WhatsApp
function selectPlan(plano) {
    const planos = {
        'mensal': 'Plano Mensal - R$ 149/mês',
        'trimestral': 'Plano Trimestral - R$ 119/mês',
        'anual': 'Plano Anual - R$ 99/mês'
    };

    const message = encodeURIComponent(`Olá! Tenho interesse no ${planos[plano]}. Gostaria de mais informações.`);
    window.open(`https://wa.me/${CONFIG.whatsappNumber}?text=${message}`, '_blank');
}

// Normalizar telefone para formato brasileiro
function normalizarTelefone(telefone) {
    // Remove tudo exceto números
    const numeros = telefone.replace(/\D/g, '');

    // Se começa com 0, remove
    let tel = numeros.replace(/^0+/, '');

    // Se tem 11 dígitos (celular com 9), adiciona +55
    if (tel.length === 11) {
        return `+55${tel}`;
    }

    // Se tem 10 dígitos (fixo ou celular antigo), adiciona +55
    if (tel.length === 10) {
        return `+55${tel}`;
    }

    // Se já tem código do país
    if (tel.length === 13 && tel.startsWith('55')) {
        return `+${tel}`;
    }

    return `+55${tel}`;
}

// Aplicar máscara de telefone em tempo real
function aplicarMascaraTelefone(input) {
    let valor = input.value.replace(/\D/g, '');

    if (valor.length <= 10) {
        valor = valor.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
    } else {
        valor = valor.replace(/^(\d{2})(\d{5})(\d{0,4}).*/, '($1) $2-$3');
    }

    input.value = valor;
}

// Aplicar máscara ao campo de telefone
document.addEventListener('DOMContentLoaded', () => {
    const telefoneInput = document.getElementById('telefone');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', (e) => aplicarMascaraTelefone(e.target));
    }
});

// Processar envio do formulário de leads
async function handleLeadSubmit(event) {
    event.preventDefault();

    const form = document.getElementById('leadForm');
    const submitBtn = form.querySelector('.btn-submit');
    const originalText = submitBtn.textContent;

    // Desabilitar botão durante envio
    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';

    // Coletar dados do formulário
    const nome = document.getElementById('nome').value.trim();
    const telefone = normalizarTelefone(document.getElementById('telefone').value);
    const email = document.getElementById('email').value.trim();
    const objetivo = document.getElementById('objetivo').value;

    try {
        // Salvar lead no Supabase
        const response = await fetch(`${CONFIG.supabaseUrl}/rest/v1/leads`, {
            method: 'POST',
            headers: {
                'apikey': CONFIG.supabaseKey,
                'Authorization': `Bearer ${CONFIG.supabaseKey}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=minimal'
            },
            body: JSON.stringify({
                nome: nome,
                telefone: telefone,
                email: email,
                objetivo: objetivo,
                origem_consentimento: 'formulario_site',
                consentido: true,
                data_consentimento: new Date().toISOString(),
                whatsapp_ativado: false
            })
        });

        if (response.ok) {
            // Sucesso - redirecionar para WhatsApp com mensagem personalizada
            const mensagem = encodeURIComponent(
                `Olá! Acabei de preencher o formulário do site.\n\n` +
                `Nome: ${nome}\n` +
                `Objetivo: ${objetivo}\n\n` +
                `Gostaria de agendar minha semana grátis!`
            );

            // Mostrar mensagem de sucesso
            alert('✅ Cadastro realizado! Você será redirecionado para o WhatsApp.');

            // Limpar formulário
            form.reset();

            // Abrir WhatsApp
            window.open(`https://wa.me/${CONFIG.whatsappNumber}?text=${mensagem}`, '_blank');

            // Enviar notificação automática via WAHA (opcional)
            await enviarNotificacaoWAHA(nome, telefone, objetivo);

        } else {
            throw new Error('Erro ao salvar dados');
        }

    } catch (error) {
        console.error('Erro:', error);
        alert('❌ Erro ao processar cadastro. Tente novamente ou entre em contato pelo WhatsApp.');

        // Fallback: abrir WhatsApp mesmo se falhar
        const mensagemFallback = encodeURIComponent(
            `Olá! Tive problema ao preencher o formulário.\n\n` +
            `Nome: ${nome}\n` +
            `Telefone: ${telefone}\n` +
            `Email: ${email}\n` +
            `Objetivo: ${objetivo}`
        );
        window.open(`https://wa.me/${CONFIG.whatsappNumber}?text=${mensagemFallback}`, '_blank');

    } finally {
        // Reabilitar botão
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

// Enviar notificação automática para a academia via WAHA
async function enviarNotificacaoWAHA(nome, telefone, objetivo) {
    try {
        const mensagem = `🔔 NOVO LEAD DO SITE!\n\n` +
                        `👤 Nome: ${nome}\n` +
                        `📱 Telefone: ${telefone}\n` +
                        `🎯 Objetivo: ${objetivo}\n\n` +
                        `Entre em contato o quanto antes!`;

        // Enviar para número da academia
        await fetch(`${CONFIG.wahaUrl}/api/sendText`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                chatId: `${CONFIG.whatsappNumber}@c.us`,
                text: mensagem,
                session: 'default'
            })
        });

        console.log('Notificação WAHA enviada com sucesso');
    } catch (error) {
        console.error('Erro ao enviar notificação WAHA:', error);
        // Não mostrar erro ao usuário, pois é processo interno
    }
}

// Analytics simples - rastrear eventos
function trackEvent(eventName, eventData = {}) {
    console.log('Event:', eventName, eventData);

    // Aqui você pode integrar com Google Analytics, Meta Pixel, etc
    // Exemplo com gtag (Google Analytics):
    // if (typeof gtag !== 'undefined') {
    //     gtag('event', eventName, eventData);
    // }
}

// Rastrear cliques nos CTAs
document.addEventListener('DOMContentLoaded', () => {
    // Rastrear cliques em botões de plano
    document.querySelectorAll('.btn-plano').forEach(btn => {
        btn.addEventListener('click', () => {
            trackEvent('plano_selecionado', {
                plano: btn.closest('.card-plano').querySelector('h3').textContent
            });
        });
    });

    // Rastrear envio de formulário
    const leadForm = document.getElementById('leadForm');
    if (leadForm) {
        leadForm.addEventListener('submit', () => {
            trackEvent('formulario_enviado', {
                objetivo: document.getElementById('objetivo').value
            });
        });
    }
});

// Lazy loading para imagens (otimização)
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    document.querySelectorAll('img.lazy').forEach(img => imageObserver.observe(img));
}
