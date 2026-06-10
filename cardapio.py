import streamlit as st
import urllib.parse

# Configuração inicial da página web do cardápio
st.set_page_config(page_title="Cardápio Digital Interativo", page_icon="🍕", layout="centered")

# Estilo CSS para personalizar as fontes e as cores da interface
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #d32f2f;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .category-header {
        color: #d32f2f;
        border-bottom: 2px solid #d32f2f;
        padding-bottom: 5px;
        margin-top: 30px;
    }
    .price-tag {
        color: #2e7d32;
        font-weight: bold;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🍕 Cantinho do Sabor</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Monte o seu pedido e envie diretamente pelo WhatsApp!</div>", unsafe_allow_html=True)

# Número de telefone do restaurante (Substitua com o DDD + o seu número)
TELEFONE_RESTAURANTE = "5521964988138" 

# Banco de dados com os pratos, preços em R$ e fotos correspondentes
menu = {
    "Hambúrgueres": [
        {
            "item": "Hambúrguer Clássico", 
            "preco": 28.50, 
            "desc": "Blend de carne bovina de 150g, queijo prato, alface, tomate e maionese artesanal da casa.",
            "imagem": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=60"
        },
        {
            "item": "Double Bacon Cheddar", 
            "preco": 38.50, 
            "desc": "Dois blends de carne bovina de 150g, muito bacon crocante e queijo cheddar derretido.",
            "imagem": "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500&auto=format&fit=crop&q=60"
        }
    ],
    "Pizzas Artesanais": [
        {
            "item": "Pizza Margherita", 
            "preco": 32.00, 
            "desc": "Molho de tomate caseiro, muçarela fresca, rodelas de tomate e manjericão fresco.",
            "imagem": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500&auto=format&fit=crop&q=60"
        },
        {
            "item": "Pizza Calabresa Especial", 
            "preco": 35.00, 
            "desc": "Molho de tomate, muçarela, calabresa defumada, cebola roxa e azeitonas pretas.",
            "imagem": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format&fit=crop&q=60"
        }
    ],
    "Bebidas Geladas": [
        {
            "item": "Suco de Laranja Natural", 
            "preco": 9.50, 
            "desc": "Espremido na hora, copo de 400ml bem gelado.",
            "imagem": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=500&auto=format&fit=crop&q=60"
        },
        {
            "item": "Refrigerante em Lata", 
            "preco": 6.00, 
            "desc": "Opções: Coca-Cola, Guaraná Antarctica ou Sprite em lata bem gelada.",
            "imagem": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=60"
        }
    ]
}

# Controle de estado para gerenciar o carrinho do cliente
pedido = {}
total_itens = 0.0

# Renderização dinâmica dos produtos do menu
for categoria, itens in menu.items():
    st.markdown(f"<h3 class='category-header'>📦 {categoria}</h3>", unsafe_allow_html=True)
    
    for i in itens:
        col_foto, col_info, col_qtd = st.columns([1.3, 2.5, 0.8])
        
        with col_foto:
            st.image(i["imagem"], use_container_width=True)
            
        with col_info:
            st.markdown(f"**{i['item']}**")
            st.markdown(f"<span class='price-tag'>R$ {i['preco']:.2f}</span>", unsafe_allow_html=True)
            st.caption(i['desc'])
            
        with col_qtd:
            # Seleção de quantidades pelo cliente
            qtd = st.number_input(f"Qtd", min_value=0, max_value=15, step=1, key=f"qtd_{i['item']}")
            if qtd > 0:
                subtotal = qtd * i['preco']
                pedido[i['item']] = {"qtd": qtd, "preco_unit": i['preco'], "subtotal": subtotal}
                total_itens += subtotal
                
        st.markdown("<div style='margin: 10px 0; border-bottom: 1px solid #f0f0f0;'></div>", unsafe_allow_html=True)

# Seção de Finalização do Pedido (Aparece apenas quando há itens selecionados)
if total_itens > 0:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## 🛒 Finalizar seu Pedido")
    
    # Organização das informações em duas colunas no formulário
    col_dados_1, col_dados_2 = st.columns(2)
    
    with col_dados_1:
        nome_cliente = st.text_input("Seu Nome Completo *", placeholder="Ex: João Silva")
        contato_cliente = st.text_input("Celular de Contato (WhatsApp) *", placeholder="Ex: (11) 99999-9999")
        
    with col_dados_2:
        opcao_entrega = st.radio(
            "Método de Entrega *",
            ["Retirada no Restaurante (Balcão)", "Entrega em Domicílio"]
        )
        
    # Inicialização das variáveis para entrega em domicílio
    taxa_entrega = 0.0
    endereco_cliente = ""
    
    if opcao_entrega == "Entrega em Domicílio":
        endereco_cliente = st.text_input("Endereço de Entrega Completo *", placeholder="Ex: Av. Paulista, 1000 - Apto 42 - Bela Vista")
        taxa_entrega = 7.00
        st.info(f"🛵 Taxa de entrega adicionada: **R$ {taxa_entrega:.2f}**")
        
    # Configuração dos métodos de pagamento
    col_pag_1, col_pag_2 = st.columns(2)
    with col_pag_1:
        metodo_pagamento = st.selectbox(
            "Forma de Pagamento *",
            ["Pix", "Dinheiro", "Cartão de Crédito/Débito"]
        )
    
    troco_para = ""
    if metodo_pagamento == "Dinheiro":
        with col_pag_2:
            precisa_troco = st.radio("Precisa de troco?", ["Não", "Sim"])
            if precisa_troco == "Sim":
                troco_para = st.text_input("Troco para quanto?", placeholder="Ex: R$ 50,00")

    # Observações opcionais para a cozinha
    observacoes = st.text_area("Observações para a cozinha (Opcional)", placeholder="Ex: Hambúrguer bem passado, sem cebola, etc.")

    # Somatório do total geral
    total_geral = total_itens + taxa_entrega
    
    # Exibição do recibo resumido dos valores na tela
    st.markdown("### 📋 Resumo do Pedido")
    st.write(f"**Subtotal dos itens:** R$ {total_itens:.2f}")
    if taxa_entrega > 0:
        st.write(f"**Taxa de Entrega:** R$ {taxa_entrega:.2f}")
    st.markdown(f"### **Total a Pagar: R$ {total_geral:.2f}**")
    
    # Validação simples para conferir se as informações obrigatórias foram inseridas
    dados_validos = len(nome_cliente.strip()) > 0 and len(contato_cliente.strip()) > 0
    if opcao_entrega == "Entrega em Domicílio" and len(endereco_cliente.strip()) == 0:
        dados_validos = False
        
    # Criação e estruturação da mensagem automatizada para envio
    if dados_validos:
        mensagem = f"*Novo Pedido - Cantinho do Sabor* 🍕\n"
        mensagem += f"-----------------------------------------\n"
        mensagem += f"👤 *Cliente:* {nome_cliente}\n"
        mensagem += f"📞 *Contato:* {contato_cliente}\n"
        mensagem += f"-----------------------------------------\n\n"
        
        mensagem += f"🛒 *Itens Pedidos:*\n"
        for item, info in pedido.items():
            mensagem += f"• {info['qtd']}x *{item}* (R$ {info['preco_unit']:.2f}/un) - Subtotal: R$ {info['subtotal']:.2f}\n"
        
        if observacoes.strip():
            mensagem += f"\n📝 *Observações:* {observacoes}\n"
            
        mensagem += f"\n-----------------------------------------\n"
        mensagem += f"🚚 *Entrega:* {opcao_entrega}\n"
        
        if opcao_entrega == "Entrega em Domicílio":
            mensagem += f"📍 *Endereço:* {endereco_cliente}\n"
            mensagem += f"🛵 *Taxa de Entrega:* R$ {taxa_entrega:.2f}\n"
            
        mensagem += f"💳 *Pagamento:* {metodo_pagamento}\n"
        if troco_para:
            mensagem += f"🪙 *Troco para:* {troco_para}\n"
            
        mensagem += f"-----------------------------------------\n"
        mensagem += f"💰 *Total Geral: R$ {total_geral:.2f}*\n"
        
        # Codificação da mensagem para o padrão do link de redirecionamento do WhatsApp
        mensagem_codificada = urllib.parse.quote(mensagem)
        link_whatsapp = f"https://wa.me/{TELEFONE_RESTAURANTE}?text={mensagem_codificada}"
        
        # Botão interativo para enviar as informações coletadas para o WhatsApp do restaurante
        st.link_button("🟢 Enviar Pedido via WhatsApp", link_whatsapp, use_container_width=True)
    else:
        st.warning("⚠️ Por favor, preencha o seu Nome, Celular e Endereço de Entrega (se aplicável) para liberar o envio por WhatsApp.")