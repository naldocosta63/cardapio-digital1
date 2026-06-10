import streamlit as st

# Configuração inicial da página web
st.set_page_config(page_title="Menu Digital", page_icon="🍕", layout="centered")

st.title("🍕 Menu Digital")
st.write("Crie a sua encomenda selecionando os artigos abaixo:")

# Base de dados do menu atualizada com imagens públicas e estáveis do Unsplash
menu = {
    "Hambúrgueres": [
        {
            "item": "Hambúrguer Clássico", 
            "preco": 28.00, 
            "desc": "Blend de 150g, queijo prato, alface, tomate e maionese artesanal.",
            "imagem": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=60"
        },
        {
            "item": "Double Bacon", 
            "preco": 38.00, 
            "desc": "Dois blends de 150g, bastante bacon estaladiço e cheddar derretido.",
            "imagem": "https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500&auto=format&fit=crop&q=60"
        }
    ],
    "Pizzas (Individual)": [
        {
            "item": "Margherita", 
            "preco": 32.00, 
            "desc": "Molho de tomate caseiro, mozzarella, rodelas de tomate e manjericão fresco.",
            "imagem": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=500&auto=format&fit=crop&q=60"
        },
        {
            "item": "Calabresa Especial", 
            "preco": 35.00, 
            "desc": "Mozzarella, chouriço calabresa fumado, cebola roxa e azeitonas pretas.",
            "imagem": "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500&auto=format&fit=crop&q=60"
        }
    ],
    "Bebidas": [
        {
            "item": "Sumo de Laranja Natural", 
            "preco": 9.00, 
            "desc": "Espremido na hora, copo de 400ml super fresco.",
            "imagem": "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=500&auto=format&fit=crop&q=60"
        },
        {
            "item": "Refrigerante em Lata", 
            "preco": 6.00, 
            "desc": "Opções: Coca-Cola, Guaraná ou Sprite em lata bem fria.",
            "imagem": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=60"
        }
    ]
}

# Dicionário para armazenar as escolhas do utilizador
pedido = {}
total_geral = 0.0

# Apresentação das categorias e respetivos artigos
for categoria, itens in menu.items():
    st.markdown(f"### 📦 {categoria}")
    
    for i in itens:
        # Divisão do ecrã em 3 colunas: Imagem, Detalhes do Artigo e Quantidade
        col_foto, col_info, col_qtd = st.columns([1.2, 2.5, 0.8])
        
        with col_foto:
            # Apresenta a imagem do prato de forma responsiva
            st.image(i["imagem"], use_container_width=True)
            
        with col_info:
            st.markdown(f"**{i['item']}**")
            st.markdown(f"<span style='color: #2e7d32; font-weight: bold;'>R$ {i['preco']:.2f}</span>", unsafe_allow_html=True)
            st.caption(i['desc'])
            
        with col_qtd:
            # Seleção de quantidade por parte do cliente
            qtd = st.number_input(f"Qtd", min_value=0, max_value=10, step=1, key=i['item'])
            if qtd > 0:
                subtotal = qtd * i['preco']
                pedido[i['item']] = {"qtd": qtd, "subtotal": subtotal}
                total_geral += subtotal
                
        # Linha de divisão elegante entre produtos
        st.markdown("<div style='margin: 15px 0; border-bottom: 1px solid #eeeeee;'></div>", unsafe_allow_html=True)

# Se existirem artigos selecionados, apresenta o resumo do carrinho de compras
if total_geral > 0:
    st.markdown("---")
    st.subheader("🛒 Resumo da sua Encomenda")
    
    for nome_item, detalhes in pedido.items():
        st.write(f"• {detalhes['qtd']}x **{nome_item}** — R$ {detalhes['subtotal']:.2f}")
        
    st.markdown(f"### **Total da Encomenda: R$ {total_geral:.2f}**")