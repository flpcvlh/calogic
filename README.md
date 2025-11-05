<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
</head>
<body>

<h1 align="center">FECAP - Fundação de Comércio Álvares Penteado</h1>

<p align="center">
  <a href="https://www.fecap.br/">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRhZPrRa89Kma0ZZogxm0pi-tCn_TLKeHGVxywp-LXAFGR3B1DPouAJYHgKZGV0XTEf4AE&usqp=CAU" alt="FECAP - Fundação de Comércio Álvares Penteado" width="200">
  </a>
</p>

<h1 align="center">🍋 CALOGIC</h1>
<h3 align="center">Sistema Analítico Integrado de Segmentação de Clientes com Machine Learning</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/PostgreSQL-Neon-green?style=for-the-badge&logo=postgresql" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Machine_Learning-K--Means-orange?style=for-the-badge" alt="ML">
</p>

<hr>

<h2>👥 Equipe</h2>

<h3>👨‍💻 Integrantes:</h3>
<ul>
  <li><b><a href="https://www.linkedin.com/in/luizfelipegcarvalho/">Luiz Felipe Galdino de Carvalho</a></b> – RA: 24026568</li>
  <li><b><a href="https://www.linkedin.com/in/gabriel-pires-2082b473/">Gabriel Gonçalves Pires</a></b> – RA: 24026518</li>
  <li><b><a href="https://www.linkedin.com/in/isabela-nunes-zeferino/">Isabela Nunes Zeferino</a></b> – RA: 24026460</li>
  <li><b><a href="https://www.linkedin.com/in/kaique-neres-0413a8265/">Kaique Neres de Oliveira</a></b> – RA: 24026134</li>
  <li><b><a href="https://www.linkedin.com/in/luizfelipegcarvalho/">Luiz Felipe Galdino de Carvalho</a></b> – RA: 24026568</li>
</ul>

<h3>🧑‍🏫 Professores Orientadores:</h3>
<ul>
  <li>Prof. Aimar Martins Lopes</li>
  <li>Prof. Edson Barbero</li>
  <li>Prof. Eduardo Savino</li>
  <li>Prof. Lucy Mari</li>
  <li>Prof. Ronaldo Araujo</li>
</ul>

<hr>

<h2>📝 Descrição do Projeto</h2>
<p>
O <b>CALOGIC</b> é uma plataforma de <b>inteligência de dados</b> desenvolvida para a <b>Cannoli</b> e seus restaurantes parceiros, com foco em <b>segmentação inteligente de clientes</b> usando análise RFM (Recency, Frequency, Monetary) e <b>Machine Learning</b>.
</p>

<h3>🎯 Principais Funcionalidades:</h3>
<ul>
  <li>🤖 <b>Segmentação automática</b> de clientes em 4 clusters usando K-Means:</li>
  <ul>
    <li>🏆 <b>Campeões</b>: Clientes de alto valor, alta frequência e recentes</li>
    <li>💎 <b>Fiéis</b>: Clientes leais com bom histórico</li>
    <li>⚠️ <b>Em Risco</b>: Clientes se afastando que precisam de atenção</li>
    <li>💔 <b>Perdidos</b>: Clientes inativos há muito tempo</li>
  </ul>
  <li>📊 <b>Dashboards interativos 3D</b> com visualização avançada dos clusters</li>
  <li>📈 <b>Análise RFM completa</b> para identificar padrões de comportamento</li>
  <li>💡 <b>Campanhas de marketing personalizadas</b> para cada cluster</li>
  <li>📧 <b>Gerador automático de campanhas</b> (Email, WhatsApp, SMS, Push)</li>
  <li>💰 <b>Cálculo de ROI</b> estimado para cada campanha</li>
  <li>🔐 <b>Sistema de autenticação seguro</b> com login e senha</li>
</ul>

<p align="center">
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSyZhoGmwbbRJXqM8VcWHd-5nlbf7SAFGNJEQ&s" alt="CALOGIC Dashboard" width="600">
</p>

<hr>

<h2>🎯 Objetivos e Metas</h2>
<ul>
  <li>✅ Segmentar clientes automaticamente usando Machine Learning</li>
  <li>✅ Fornecer insights acionáveis sobre comportamento de clientes</li>
  <li>✅ Aumentar a retenção de clientes através de campanhas direcionadas</li>
  <li>✅ Reduzir churn identificando clientes em risco</li>
  <li>✅ Maximizar o LTV (Lifetime Value) dos clientes</li>
  <li>✅ Criar uma plataforma intuitiva e acessível para gestores</li>
  <li>✅ Entregar análises em tempo real com atualização automática</li>
</ul>

<hr>

<h2>📁 Estrutura do Projeto</h2>

<pre>
Raiz/
│
├── 📂 documentos/
│   ├── Entrega 1/
│   ├── Entrega 2/
│   └── Documentação.docx
│
├── 📂 executáveis/
│   └── src/
│       ├── backend/
│       └── frontend/
│
├── 📂 imagens/
│
├── 📂 src/
│   │
│   ├── 📂 Backend/calogic/
│   │   │
│   │   ├── 📄 app.py                      # Dashboard principal (login + 3D)
│   │   ├── 📄 setup_db.py                 # ETL - CSV → PostgreSQL
│   │   ├── 📄 ml_engine.py                # Motor ML (RFM + K-Means)
│   │   ├── 📄 verificar_clusters.py       # Validação dos clusters
│   │   ├── 📄 style.css                   # Estilos customizados
│   │   ├── 📄 requirements.txt            # Dependências Python
│   │   │
│   │   ├── 📂 pages/                      # Páginas por cluster
│   │   │   ├── 1_🏆_Campeoes.py
│   │   │   ├── 2_💎_Fieis.py
│   │   │   ├── 3_⚠️_Em_Risco.py
│   │   │   └── 4_💔_Perdidos.py
│   │   │
│   │   ├── 📂 data/
│   │   │   └── mock_orders_for_rfm.csv    # Dados de pedidos
│   │   │
│   │   └── 📂 .streamlit/
│   │       ├── config.toml                # Config visual
│   │       └── secrets.toml               # Credenciais (não versionar!)
│   │
│   └── 📂 Frontend/
│       └── (Em desenvolvimento)
│
└── 📄 README.md                            # Este arquivo
</pre>

<hr>

<h2>🚀 Como Executar o Projeto</h2>

<h3>📋 Pré-requisitos</h3>
<ul>
  <li>Python 3.11 ou superior</li>
  <li>Conta no <a href="https://neon.tech">Neon PostgreSQL</a> (banco de dados cloud gratuito)</li>
  <li>Git instalado</li>
</ul>

<h3>⚙️ Instalação</h3>

<h4>1️⃣ Clone o repositório:</h4>
<pre>
git clone https://github.com/seu-usuario/calogic.git
cd calogic
</pre>

<h4>2️⃣ Crie um ambiente virtual:</h4>
<pre>
python -m venv venv

# No Windows:
venv\Scripts\activate

# No Mac/Linux:
source venv/bin/activate
</pre>

<h4>3️⃣ Instale as dependências:</h4>
<pre>
pip install -r requirements.txt
</pre>

<h4>4️⃣ Configure as credenciais:</h4>
<p>Crie o arquivo <code>.streamlit/secrets.toml</code>:</p>
<pre>
NEON_DB_URL = "postgresql://usuario:senha@host/database?sslmode=require"
APP_USER = "admin"
APP_PASSWORD = "admin123"
</pre>

<h4>5️⃣ Execute a ETL (Carrega dados no banco):</h4>
<pre>
python setup_db.py
</pre>

<h4>6️⃣ Execute o Motor de ML (Segmentação):</h4>
<pre>
python ml_engine.py
</pre>

<h4>7️⃣ Verifique os clusters:</h4>
<pre>
python verificar_clusters.py
</pre>

<h4>8️⃣ Execute o dashboard:</h4>
<pre>
streamlit run app.py
</pre>

<h4>9️⃣ Acesse no navegador:</h4>
<pre>
http://localhost:8501
</pre>

<p><b>Login:</b> <code>admin</code> / <code>admin123</code></p>

<hr>

<h2>🔐 Credenciais de Acesso</h2>
<table>
  <tr>
    <th>Ambiente</th>
    <th>Usuário</th>
    <th>Senha</th>
  </tr>
  <tr>
    <td>Dashboard</td>
    <td><code>admin</code></td>
    <td><code>admin123</code></td>
  </tr>
</table>

<hr>

<h2>📊 Tecnologias Utilizadas</h2>

<h3>🐍 Backend & Machine Learning</h3>
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" width="50" height="50" alt="Python" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/05/Scikit_learn_logo_small.svg" width="80" height="50" alt="Scikit-learn" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/e/ed/Pandas_logo.svg" width="80" height="50" alt="Pandas" />
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/31/NumPy_logo_2020.svg" width="80" height="50" alt="NumPy" />
</div>

<h3>🎨 Frontend & Visualização</h3>
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://streamlit.io/images/brand/streamlit-mark-color.png" width="50" height="50" alt="Streamlit" />
  <img src="https://images.plot.ly/logo/new-branding/plotly-logomark.png" width="50" height="50" alt="Plotly" />
</div>

<h3>💾 Banco de Dados</h3>
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" width="50" height="50" alt="PostgreSQL" />
  <img src="https://ml.globenewswire.com/Resource/Download/82e79fc7-1654-41e7-af70-f5857596743c" width="50" height="50" alt="Neon" />
</div>

<h3>🛠 Ferramentas & DevOps</h3>
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" width="50" height="50" alt="Git" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vscode/vscode-original.svg" width="50" height="50" alt="VS Code" />
</div>

<hr>

<h2>🤖 Algoritmo de Machine Learning</h2>

<h3>📐 Análise RFM (Recency, Frequency, Monetary)</h3>
<ul>
  <li><b>Recency (R)</b>: Dias desde a última compra</li>
  <li><b>Frequency (F)</b>: Número total de pedidos</li>
  <li><b>Monetary (M)</b>: Valor total gasto</li>
</ul>

<h3>🎯 K-Means Clustering</h3>
<ul>
  <li><b>Algoritmo:</b> K-Means++ (inicialização inteligente)</li>
  <li><b>Número de clusters:</b> 4 (determinado pelo método do cotovelo)</li>
  <li><b>Normalização:</b> StandardScaler</li>
  <li><b>Score de classificação:</b> Baseado em RFM invertido</li>
</ul>

<h3>📊 Clusters Resultantes:</h3>
<table>
  <tr>
    <th>Cluster</th>
    <th>Nome</th>
    <th>Características</th>
    <th>Estratégia</th>
  </tr>
  <tr>
    <td>0</td>
    <td>🏆 Campeões</td>
    <td>R: Baixa, F: Alta, M: Alto</td>
    <td>Programa VIP, retenção máxima</td>
  </tr>
  <tr>
    <td>1</td>
    <td>💎 Fiéis</td>
    <td>R: Média, F: Boa, M: Bom</td>
    <td>Upgrade para Campeões</td>
  </tr>
  <tr>
    <td>2</td>
    <td>⚠️ Em Risco</td>
    <td>R: Alta, F: Média, M: Médio</td>
    <td>Winback urgente</td>
  </tr>
  <tr>
    <td>3</td>
    <td>💔 Perdidos</td>
    <td>R: Muito Alta, F: Baixa, M: Variado</td>
    <td>Última tentativa de reativação</td>
  </tr>
</table>

<hr>

<h2>📈 Exemplos de Insights Gerados</h2>

<h3>🏆 Campeões</h3>
<ul>
  <li>68 clientes (15.4%)</li>
  <li>Recência média: 59 dias</li>
  <li>Frequência média: 12.3 pedidos</li>
  <li>Valor médio: R$ 2,329.68</li>
  <li><b>Ação:</b> Programa VIP com 20% OFF permanente</li>
</ul>

<h3>💔 Perdidos</h3>
<ul>
  <li>46 clientes (10.4%)</li>
  <li>Recência média: 354 dias</li>
  <li>Frequência média: 3.9 pedidos</li>
  <li>Valor médio: R$ 690.42</li>
  <li><b>Ação:</b> Vale R$ 50 + 30% OFF (última chance)</li>
</ul>

<hr>

<h2>📱 Funcionalidades do Dashboard</h2>

<h3>🏠 Visão Geral</h3>
<ul>
  <li>Gráfico 3D interativo dos clusters</li>
  <li>Método do cotovelo para validação do K</li>
  <li>Métricas globais da base de clientes</li>
  <li>Distribuição percentual por cluster</li>
</ul>

<h3>📊 Páginas Individuais por Cluster</h3>
<ul>
  <li>Diagnóstico detalhado do comportamento</li>
  <li>Gráficos de linha suaves (Recência, Frequência, Valor)</li>
  <li>Mapa de oportunidades dinâmico</li>
  <li>Top 30 clientes do cluster</li>
  <li>Gerador de campanhas de marketing</li>
  <li>Cálculo de ROI estimado</li>
</ul>

<hr>

<h2>🎨 Design e UX</h2>
<ul>
  <li>🍋 <b>Tema Calogic:</b> Verde limão (#a3ff12) + Dark mode</li>
  <li>🎭 <b>Animações:</b> Transições suaves e hover effects</li>
  <li>📱 <b>Responsivo:</b> Adaptado para desktop, tablet e mobile</li>
  <li>🔐 <b>Login elegante:</b> Tela de autenticação com logo animado</li>
  <li>📊 <b>Visualizações:</b> Plotly 3D interativo</li>
</ul>

<hr>

<h2>📋 Licença</h2>
<p>
Este projeto está licenciado sob a licença <b>MIT</b>.<br>
Consulte o arquivo <code>LICENSE</code> para mais detalhes.
</p>

<hr>

<h2>🤝 Contribuindo</h2>
<p>Contribuições são bem-vindas! Para contribuir:</p>
<ol>
  <li>Fork o projeto</li>
  <li>Crie uma branch para sua feature (<code>git checkout -b feature/NovaFeature</code>)</li>
  <li>Commit suas mudanças (<code>git commit -m 'Adiciona NovaFeature'</code>)</li>
  <li>Push para a branch (<code>git push origin feature/NovaFeature</code>)</li>
  <li>Abra um Pull Request</li>
</ol>

<hr>

<h2>📞 Contato</h2>
<p>Para dúvidas ou sugestões, entre em contato com a equipe:</p>
<ul>
  <li>📧 Email: calogic@fecap.edu.br</li>
  <li>🏫 Instituição: FECAP - Fundação de Comércio Álvares Penteado</li>
</ul>

<hr>

<h2>🎓 Referências</h2>
<ol>
  <li><a href="https://scikit-learn.org/stable/modules/clustering.html#k-means">Scikit-learn K-Means Documentation</a></li>
  <li><a href="https://streamlit.io/docs">Streamlit Documentation</a></li>
  <li><a href="https://plotly.com/python/">Plotly Python Documentation</a></li>
  <li><a href="https://neon.tech/docs">Neon PostgreSQL Documentation</a></li>
  <li><a href="https://github.com/iuricode/readme-template">Readme Template</a></li>
</ol>

<hr>

<p align="center">
  <b>🍋 Desenvolvido pela Equipe CALOGIC | FECAP 2025 - ADS 4 </b>
</p>

</body>
</html>
