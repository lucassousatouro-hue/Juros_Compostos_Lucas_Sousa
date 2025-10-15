import streamlit as st
import pandas as pd

# Título e autoria
st.title("💰 Calculadora de Juros Compostos")
st.caption("Desenvolvido por **Lucas Sousa** 🧠💻")
st.write("Simule o crescimento do seu investimento mês a mês, veja a evolução anual e o desconto de imposto de renda conforme a lei vigente.")

# Entradas do usuário
aporte_inicial = st.number_input("Aporte inicial (R$):", min_value=0.0, value=0.0)
aporte_mensal = st.number_input("Aporte mensal (R$):", min_value=0.0, value=0.0)
taxa = st.number_input("Rendimento mensal (%):", min_value=0.0, value=1.0)
meses = st.number_input("Período (em meses):", min_value=1, value=12, step=1)

if st.button("Calcular"):
    saldo = aporte_inicial
    taxa_decimal = taxa / 100
    evolucao = []

    for mes in range(1, meses + 1):
        juros = saldo * taxa_decimal
        saldo += juros + aporte_mensal
        ano = mes // 12  # cálculo do ano (ex: mês 12 = 1 ano)
        label_ano = f" ({ano} ano{'s' if ano > 1 else ''})" if mes % 12 == 0 else ""
        evolucao.append({
            "Mês": f"{mes}{label_ano}",
            "Aporte": aporte_mensal if mes > 1 or aporte_inicial == 0 else aporte_inicial,
            "Juros": round(juros, 2),
            "Saldo Total": round(saldo, 2)
        })

    df = pd.DataFrame(evolucao)

    # Exibe tabela
    st.subheader("📊 Evolução mês a mês")
    st.dataframe(df)

    # Cálculos finais
    total_aportes = aporte_inicial + (aporte_mensal * meses)
    total_juros = saldo - total_aportes

    # Imposto de renda conforme tempo de aplicação
    dias = meses * 30  # aproximação (1 mês = 30 dias)
    if dias <= 180:
        aliquota = 22.5
    elif dias <= 360:
        aliquota = 20.0
    elif dias <= 720:
        aliquota = 17.5
    else:
        aliquota = 15.0

    imposto = total_juros * (aliquota / 100)
    saldo_liquido = saldo - imposto

    # Exibe resultados
    st.subheader("📈 Resultado final")
    st.write(f"**Total investido:** R$ {total_aportes:,.2f}")
    st.write(f"**Total de juros:** R$ {total_juros:,.2f}")
    st.write(f"**Imposto de renda ({aliquota:.1f}%):** R$ {imposto:,.2f}")
    st.write(f"**Valor final bruto:** R$ {saldo:,.2f}")
    st.success(f"**Valor final líquido (após IR): R$ {saldo_liquido:,.2f}**")

    # Gráfico de crescimento
    st.subheader("📈 Gráfico de Crescimento do Investimento")
    st.line_chart(df[["Saldo Total"]])

    # Detalhamento adicional
    st.markdown("---")
    st.markdown("### 📘 Detalhamento do Imposto de Renda")
    st.write("""
    O cálculo do imposto de renda segue a tabela regressiva da renda fixa no Brasil:
    - **Até 180 dias:** 22,5%  
    - **De 181 a 360 dias:** 20%  
    - **De 361 a 720 dias:** 17,5%  
    - **Acima de 720 dias:** 15%
    """)

# Rodapé
st.markdown("---")
st.markdown("💡 *Aplicativo criado para fins educacionais por Lucas Sousa.*")
