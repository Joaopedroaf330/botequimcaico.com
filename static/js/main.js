// ============================================================================
// BOTEQUIM CAICÓ - INTERATIVIDADE DA COMANDA E CARDÁPIO
// ============================================================================

let comanda = JSON.parse(localStorage.getItem('botequim_caico_comanda') || '[]');
let categoriaAtual = 'todos';

document.addEventListener('DOMContentLoaded', () => {
    atualizarUI();

    const selectModalidade = document.getElementById('cliente-modalidade');

    if (selectModalidade) {
        selectModalidade.addEventListener('change', () => {
            const labelEnd = document.getElementById('label-endereco-mesa');
            const inputEnd = document.getElementById('cliente-endereco');
            const extrasEntrega = document.getElementById('campos-entrega-extras');
            const compEntrega = document.getElementById('campos-entrega-complemento');
            if (selectModalidade.value === 'mesa') {
                labelEnd.textContent = 'Número da Mesa no Botequim *';
                inputEnd.placeholder = 'Ex: Mesa 07 (Calçada do Botequim)';
                if (extrasEntrega) extrasEntrega.style.display = 'none';
                if (compEntrega) compEntrega.style.display = 'none';
            } else if (selectModalidade.value === 'retirada') {
                labelEnd.textContent = 'Observação para Retirada no Balcão';
                inputEnd.placeholder = 'Ex: Passo aí em 20 minutinhos!';
                if (extrasEntrega) extrasEntrega.style.display = 'none';
                if (compEntrega) compEntrega.style.display = 'none';
            } else {
                labelEnd.textContent = 'Endereço de Entrega (Rua) *';
                inputEnd.placeholder = 'Nome da Rua / Avenida...';
                if (extrasEntrega) extrasEntrega.style.display = 'grid';
                if (compEntrega) compEntrega.style.display = 'grid';
            }
            atualizarUI();
        });
    }
});

function filtrarCategoria(cat, btnElement) {
    categoriaAtual = cat;
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    if (btnElement) btnElement.classList.add('active');
    aplicarFiltrosCardapio();
}

function aplicarFiltrosCardapio() {
    const termo = (document.getElementById('busca-espeto')?.value || '').trim().toLowerCase();
    const cards = document.querySelectorAll('.menu-card');

    cards.forEach(card => {
        const cat = card.dataset.categoria;
        const nome = (card.dataset.nome || '').toLowerCase();
        const desc = (card.dataset.desc || '').toLowerCase();

        const bateCategoria = categoriaAtual === 'todos' || cat === categoriaAtual;
        const bateBusca = !termo || nome.includes(termo) || desc.includes(termo);

        card.style.display = (bateCategoria && bateBusca) ? 'flex' : 'none';
    });
}

function atualizarPrecoOpcao(id, selectEl) {
    const opt = selectEl.options[selectEl.selectedIndex];
    const precoEl = document.getElementById(`preco-card-${id}`);
    if (opt && opt.dataset.preco && precoEl) {
        const novoPreco = parseFloat(opt.dataset.preco);
        precoEl.textContent = `R$ ${novoPreco.toFixed(2).replace('.', ',')}`;
    }
}

function adicionarNaComanda(id, nome, preco, temPonto) {
    let pontoSelecionado = 'Padrão do Botequim';
    let precoFinal = parseFloat(preco);
    const selectPonto = document.getElementById(`ponto-${id}`);
    if (temPonto && selectPonto) {
        pontoSelecionado = selectPonto.value;
        const opt = selectPonto.options[selectPonto.selectedIndex];
        if (opt && opt.dataset.preco) {
            precoFinal = parseFloat(opt.dataset.preco);
        }
    }

    const chaveUnica = `${id}__${pontoSelecionado}`;
    const existente = comanda.find(item => item.chave === chaveUnica);

    if (existente) {
        existente.quantidade += 1;
    } else {
        comanda.push({
            chave: chaveUnica,
            id: id,
            nome: nome,
            preco: precoFinal,
            ponto: pontoSelecionado,
            quantidade: 1
        });
    }

    salvarComanda();
    atualizarUI();
    mostrarToast(`🔥 +1 ${nome} anotado na comanda!`);
}

function alterarQuantidade(chave, delta) {
    const idx = comanda.findIndex(item => item.chave === chave);
    if (idx === -1) return;

    comanda[idx].quantidade += delta;
    if (comanda[idx].quantidade <= 0) {
        comanda.splice(idx, 1);
    }
    salvarComanda();
    atualizarUI();
}

function salvarComanda() {
    localStorage.setItem('botequim_caico_comanda', JSON.stringify(comanda));
}

function atualizarUI() {
    const totalItens = comanda.reduce((acc, item) => acc + item.quantidade, 0);
    const badge = document.getElementById('comanda-count');
    if (badge) badge.textContent = totalItens;

    const listaEl = document.getElementById('comanda-items-list');
    const formCheckout = document.getElementById('checkout-form-section');
    if (!listaEl) return;

    if (comanda.length === 0) {
        listaEl.innerHTML = `
            <div class="comanda-empty">
                <div style="font-size: 2.6rem; margin-bottom: 0.5rem;">🍢</div>
                <p><strong>Sua comanda ainda está vazia!</strong></p>
                <p style="font-size: 0.85rem; margin-top: 0.3rem;">Escolha seus espetinhos bem assadinhos com farofa e vinagrete.</p>
            </div>
        `;
        if (formCheckout) formCheckout.style.display = 'none';
    } else {
        if (formCheckout) formCheckout.style.display = 'grid';
        listaEl.innerHTML = comanda.map(item => `
            <div class="comanda-item">
                <div class="comanda-item-info">
                    <strong>${item.nome}</strong>
                    <small>${item.ponto}</small>
                    <span>R$ ${(item.preco * item.quantidade).toFixed(2).replace('.', ',')}</span>
                </div>
                <div class="comanda-item-controls">
                    <button class="qty-btn" onclick="alterarQuantidade('${item.chave}', -1)">-</button>
                    <span style="min-width: 22px; text-align: center; font-weight: 800;">${item.quantidade}</span>
                    <button class="qty-btn" onclick="alterarQuantidade('${item.chave}', 1)">+</button>
                </div>
            </div>
        `).join('');
    }

    const subtotal = comanda.reduce((acc, item) => acc + item.preco * item.quantidade, 0);
    const modalidade = document.getElementById('cliente-modalidade')?.value || 'entrega';
    const taxa = (comanda.length > 0 && modalidade === 'entrega') ? 8.00 : 0.00;
    const total = subtotal + taxa;

    const elSub = document.getElementById('resumo-subtotal');
    const elTaxa = document.getElementById('resumo-taxa');
    const elTotal = document.getElementById('resumo-total');

    if (elSub) elSub.textContent = `R$ ${subtotal.toFixed(2).replace('.', ',')}`;
    if (elTaxa) elTaxa.textContent = taxa > 0 ? `R$ ${taxa.toFixed(2).replace('.', ',')}` : 'Grátis';
    if (elTotal) elTotal.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
}

function toggleComanda(abrir) {
    const overlay = document.getElementById('drawer-overlay');
    const drawer = document.getElementById('comanda-drawer');
    if (!overlay || !drawer) return;

    if (abrir) {
        overlay.classList.add('open');
        drawer.classList.add('open');
    } else {
        overlay.classList.remove('open');
        drawer.classList.remove('open');
    }
}

async function enviarPedidoBotequim(event) {
    if (event) event.preventDefault();
    if (comanda.length === 0) {
        mostrarToast('⚠️ Adicione pelo menos um espetinho na comanda!');
        return;
    }

    const nome = document.getElementById('cliente-nome').value.trim();
    const telefone = document.getElementById('cliente-telefone').value.trim();
    const modalidade = document.getElementById('cliente-modalidade').value;
    const regiao = (document.getElementById('cliente-regiao')?.value || '').trim();
    const endereco = document.getElementById('cliente-endereco').value.trim();
    const numeroApto = (document.getElementById('cliente-numero-apto')?.value || '').trim();
    const referencia = (document.getElementById('cliente-referencia')?.value || '').trim();
    const pagamento = document.getElementById('cliente-pagamento').value;
    const observacoes = document.getElementById('cliente-obs').value.trim();

    if (!nome) {
        mostrarToast('⚠️ Informe seu nome pra gente chamar na comanda!');
        document.getElementById('cliente-nome').focus();
        return;
    }

    if (modalidade === 'entrega') {
        if (!regiao) {
            mostrarToast('⚠️ Selecione a região/bairro de entrega!');
            document.getElementById('cliente-regiao')?.focus();
            return;
        }
        if (!endereco) {
            mostrarToast('⚠️ Informe a rua de entrega!');
            document.getElementById('cliente-endereco').focus();
            return;
        }
        if (!numeroApto) {
            mostrarToast('⚠️ Informe o número e apartamento/complemento!');
            document.getElementById('cliente-numero-apto')?.focus();
            return;
        }
        if (!referencia) {
            mostrarToast('⚠️ Informe um ponto de referência para entrega!');
            document.getElementById('cliente-referencia')?.focus();
            return;
        }
    }

    const enderecoFinal = modalidade === 'entrega'
        ? `${regiao} — ${endereco}, Nº/Apto: ${numeroApto} | Ref: ${referencia}`
        : endereco;

    const btn = document.getElementById('btn-submit-pedido');
    const textoOriginal = btn.textContent;
    btn.disabled = true;
    btn.textContent = 'Sopra a brasa... Enviando pedido 🔥';

    try {
        const resp = await fetch('/api/pedidos', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                cliente_nome: nome,
                cliente_telefone: telefone,
                modalidade: modalidade,
                regiao_entrega: regiao,
                endereco_ou_mesa: enderecoFinal,
                pagamento: pagamento,
                observacoes: observacoes,
                itens: comanda
            })
        });

        const data = await resp.json();
        if (!resp.ok) {
            mostrarToast(`❌ ${data.erro || 'Erro ao anotar pedido'}`);
            return;
        }

        // Limpa a comanda e exibe o Cupom de Botequim
        comanda = [];
        salvarComanda();
        atualizarUI();
        toggleComanda(false);
        exibirCupomConfirmacao(data.pedido);
    } catch (err) {
        mostrarToast('❌ Erro de conexão com o Botequim. Tente novamente!');
    } finally {
        btn.disabled = false;
        btn.textContent = textoOriginal;
    }
}

function exibirCupomConfirmacao(pedido) {
    const modal = document.getElementById('modal-confirmacao');
    const container = document.getElementById('cupom-confirmacao-conteudo');
    if (!modal || !container) return;

    const linhasItens = pedido.itens.map(i =>
        `<div style="display:flex;justify-content:space-between;margin:4px 0;font-size:0.88rem;">
            <span>${i.quantidade}x ${i.nome} <br><small>(${i.ponto})</small></span>
            <strong>R$ ${i.total_item.toFixed(2).replace('.', ',')}</strong>
        </div>`
    ).join('');

    const textoZap = encodeURIComponent(
        `🔥 *PEDIDO BOTEQUIM CAICÓ - ${pedido.codigo}* 🔥\n` +
        `👤 *Cliente:* ${pedido.cliente_nome}\n` +
        `📍 *Modalidade:* ${pedido.modalidade.toUpperCase()} (${pedido.endereco_ou_mesa})\n` +
        `💳 *Pagamento:* ${pedido.pagamento.toUpperCase()}\n\n` +
        `*ITENS NA BRASA:*\n` +
        pedido.itens.map(i => `- ${i.quantidade}x ${i.nome} (${i.ponto})`).join('\n') +
        `\n\n🛵 *Frete:* R$ ${pedido.taxa_entrega.toFixed(2).replace('.', ',')}` +
        `\n💰 *Total:* R$ ${pedido.total.toFixed(2).replace('.', ',')}`
    );

    container.innerHTML = `
        <div class="cupom-botequim">
            <h4>★ BOTEQUIM CAICÓ ★</h4>
            <p style="text-align:center;font-size:0.78rem;margin-bottom:0.65rem;">
                O Autêntico Espetinho do Seridó<br>
                Comanda: <strong>#${pedido.codigo}</strong> • ${pedido.criado_em}
            </p>
            <hr style="border:none;border-top:1px dashed #78350f;margin:0.55rem 0;">
            <p style="font-size:0.85rem;"><strong>Cliente:</strong> ${pedido.cliente_nome}</p>
            <p style="font-size:0.85rem;"><strong>Entrega/Mesa:</strong> ${pedido.modalidade.toUpperCase()} - ${pedido.endereco_ou_mesa}</p>
            <p style="font-size:0.85rem;"><strong>Pagamento:</strong> ${pedido.pagamento.toUpperCase()}</p>
            <hr style="border:none;border-top:1px dashed #78350f;margin:0.55rem 0;">
            ${linhasItens}
            <hr style="border:none;border-top:1px dashed #78350f;margin:0.55rem 0;">
            <div style="display:flex;justify-content:space-between;font-size:0.86rem;margin-bottom:0.25rem;">
                <span>Taxa de Entrega:</span>
                <strong>R$ ${pedido.taxa_entrega.toFixed(2).replace('.', ',')}</strong>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:1.05rem;font-weight:800;">
                <span>TOTAL DA COMANDA:</span>
                <span>R$ ${pedido.total.toFixed(2).replace('.', ',')}</span>
            </div>
            <p style="text-align:center;font-size:0.78rem;margin-top:0.7rem;color:#9a3412;font-weight:700;">
                STATUS: ${pedido.status} (Servido com farofa e vinagrete!)
            </p>
        </div>
        <div style="display:flex;gap:0.75rem;flex-wrap:wrap;">
            <a href="https://wa.me/5583987623386?text=${textoZap}" target="_blank" rel="noopener"
               class="btn-finalizar" style="text-decoration:none;text-align:center;flex:1;">
               📲 Enviar Comanda no WhatsApp (83) 98762-3386
            </a>
            <button onclick="fecharModalConfirmacao()" class="btn-secondary-botequim" style="cursor:pointer;">
               Voltar ao Cardápio
            </button>
        </div>
    `;

    modal.classList.add('open');
}

function fecharModalConfirmacao() {
    document.getElementById('modal-confirmacao')?.classList.remove('open');
}

async function abrirPainelBrasa() {
    const modal = document.getElementById('modal-brasa');
    const lista = document.getElementById('lista-pedidos-brasa');
    if (!modal || !lista) return;

    modal.classList.add('open');
    lista.innerHTML = '<p style="text-align:center;padding:1.5rem;">Olhando a churrasqueira... 🔥</p>';

    try {
        const resp = await fetch('/api/pedidos');
        const pedidos = await resp.json();

        if (!pedidos.length) {
            lista.innerHTML = `
                <div style="text-align:center;padding:2rem;color:#bba58b;">
                    <p style="font-size:2rem;margin-bottom:0.4rem;">🔥</p>
                    <p>A brasa já está acesa! Faça o primeiro pedido da noite.</p>
                </div>
            `;
            return;
        }

        lista.innerHTML = pedidos.map(p => `
            <div class="pedido-live-card">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                    <strong style="color:#fbbf24;">#${p.codigo} — ${p.cliente_nome}</strong>
                    <span class="card-selo">${p.status}</span>
                </div>
                <p style="font-size:0.82rem;color:#e5d5bc;margin-bottom:0.45rem;">
                    📍 ${p.modalidade.toUpperCase()} (${p.endereco_ou_mesa}) • 🕒 ${p.criado_em}
                </p>
                <div style="font-size:0.85rem;color:#fdf6e9;">
                    ${p.itens.map(i => `• ${i.quantidade}x ${i.nome} <em>(${i.ponto})</em>`).join('<br>')}
                </div>
                <div style="text-align:right;margin-top:0.45rem;font-weight:800;color:#fbbf24;">
                    Total: R$ ${p.total.toFixed(2).replace('.', ',')}
                </div>
            </div>
        `).join('');
    } catch (e) {
        lista.innerHTML = '<p>Erro ao carregar os pedidos na brasa.</p>';
    }
}

function fecharPainelBrasa() {
    document.getElementById('modal-brasa')?.classList.remove('open');
}

let toastTimer = null;
function mostrarToast(msg) {
    const toast = document.getElementById('toast-botequim');
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}
