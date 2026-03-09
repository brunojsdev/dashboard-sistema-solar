# 🪐 Painel Analítico do Sistema Solar

Este projeto consiste em um dashboard de Business Intelligence (BI) focado na análise quantitativa e visualização de dados astronômicos. A aplicação processa variáveis físicas e orbitais dos corpos celestes, oferecendo uma interface técnica para exploração científica de alta performance.

## 🛠️ Stack Tecnológica

* **Linguagem:** Python 3.x
* **Framework Web:** [Streamlit](https://streamlit.io/)
* **Manipulação de Dados:** [Pandas](https://pandas.pydata.org/)
* **Visualização:** [Plotly Express](https://plotly.com/python/) & Graph Objects
* **Estilização:** CSS3 Customizado para interface de alto contraste

## 📊 Funcionalidades Principais

* **Navegação Modular:** Sistema de filtragem lateral para alternância entre tipos de planetas (Rochosos, Gasosos e Gelo).
* **Indicadores de Performance (KPIs):** Visualização em tempo real de gravidade média, diâmetro equatorial e contagem de satélites.
* **Análises Gráficas:**
    * Comparativo de escalas entre planetas e o Sol.
    * Gráficos de dispersão correlacionando temperatura e distância orbital.
    * Medidores (Gauges) de potencial gravitacional com escalas normalizadas.
* **UX Otimizada:** Implementação de modo de interação *Pan* nos gráficos para navegação precisa sem distorções de zoom.

## ⚙️ Configuração e Execução

1. **Instalação de Dependências:**
   ```bash
   pip install -r requirements.txt
   ```
2. Execução da Aplicação:
   ```bash
   streamlit run app.py
   ```
## 📁 Estrutura de Arquivos

* `app.py`: Lógica principal e interface do dashboard.
* `requirements.txt`: Lista de bibliotecas necessárias.
* `fi-port.png`: Favicon e identidade visual.
* `.streamlit/config.toml`: Configurações de tema.
