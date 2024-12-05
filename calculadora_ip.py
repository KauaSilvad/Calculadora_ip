import ipaddress
import streamlit as st

def calcular_detalhes_ip(ip_str, mascara_str):
    try:
        rede = ipaddress.IPv4Network(f"{ip_str}/{mascara_str}", strict=False)
        endereco_rede = str(rede.network_address)
        broadcast = str(rede.broadcast_address)
        primeiro_host = str(list(rede.hosts())[0]) if len(list(rede.hosts())) > 0 else "N/A"
        ultimo_host = str(list(rede.hosts())[-1]) if len(list(rede.hosts())) > 0 else "N/A"
        total_hosts = rede.num_addresses - 2
        classe_ip = determinar_classe(ip_str)
        publico_privado = "Privado" if rede.is_private else "Público"
        mascara_original = rede.prefixlen
        bits_emprestados = int(mascara_str) - mascara_original
        quantidade_sub_redes = 2 ** bits_emprestados if bits_emprestados >= 0 else 0
        return {
            "Endereço de Rede": endereco_rede,
            "Primeiro Host": primeiro_host,
            "Último Host": ultimo_host,
            "Endereço de Broadcast": broadcast,
            "Classe do IP": classe_ip,
            "Quantidade de Hosts por Sub-rede": total_hosts,
            "Quantidade de Sub-redes": quantidade_sub_redes,
            "Endereço Público/Privado": publico_privado
        }
    except Exception as e:
        return {"Erro": str(e)}

def determinar_classe(ip_str):
    primeiro_octeto = int(ip_str.split(".")[0])
    if 1 <= primeiro_octeto <= 126:
        return "A"
    elif 128 <= primeiro_octeto <= 191:
        return "B"
    elif 192 <= primeiro_octeto <= 223:
        return "C"
    else:
        return "Desconhecida"

st.set_page_config(page_title="Calculadora de IP", layout="centered")
st.markdown(
    """
    <style>
        /* Fundo roxo claro no app principal */
        [data-testid="stAppViewContainer"] {
            background-color: #e9e3ff; /* Roxo claro e suave */
            color: #6200ea; /* Define a cor padrão do texto como branco */
        }

        /* Fundo da barra lateral (opcional) */
        [data-testid="stSidebar"] {
            background-color: #d8c9ff; 
        }

        /* Botões */
        .stButton>button {
            background-color: #ffffff; 
            color: #6200ea; 
            border: 2px solid 	#000000; 
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px; 
        }

        .stButton>button:hover {
            background-color: #6200ea; /* Fundo roxo ao passar o mouse */
            color: #ffffff; /* Texto branco ao passar o mouse */
        }

        /* Títulos e textos em branco */
        h1, h2, h3, h4, h5, h6, p {
            color: #6200ea; /* Texto principal branco */
        }

        /* Cards e caixas de resultados */
        .stMarkdown {
            background-color: #ffffff; /* Fundo branco nos cards */
            color: #6200ea; /* Texto roxo */
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1); /* Sombra leve */
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("📊 Calculadora de IP")
st.write("Insira o endereço IP e a máscara de sub-rede para calcular os detalhes.")

with st.form("form_calculadora"):
    ip_input = st.text_input("Endereço IP", value="192.168.1.1")
    mascara_input = st.text_input("Máscara de Sub-rede", value="24")
    calcular = st.form_submit_button("Calcular")

if calcular:
    resultados = calcular_detalhes_ip(ip_input, mascara_input)
    if "Erro" in resultados:
        st.error(f"Erro: {resultados['Erro']}")
    else:
        st.success("Resultados calculados com sucesso!")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Endereço de Rede:** {resultados['Endereço de Rede']}")
            st.write(f"**Primeiro Host:** {resultados['Primeiro Host']}")
            st.write(f"**Último Host:** {resultados['Último Host']}")
            st.write(f"**Endereço de Broadcast:** {resultados['Endereço de Broadcast']}")
        with col2:
            st.write(f"**Classe do IP:** {resultados['Classe do IP']}")
            st.write(f"**Quantidade de Hosts por Sub-rede:** {resultados['Quantidade de Hosts por Sub-rede']}")
            st.write(f"**Quantidade de Sub-redes:** {resultados['Quantidade de Sub-redes']}")
            st.write(f"**Endereço Público/Privado:** {resultados['Endereço Público/Privado']}")
