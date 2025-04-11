<a id="readme-top">En | Pt-br</a>

<br />
<div align="center">
  <a href="">
      <img src="https://www.ortofotos.niteroi.rj.gov.br/arquivos/Imagens/github_ED/logos/logo_smdcg%20_%20ED.png" alt="Logo" height="80">
  </a>
  <h3 align="center">Pipelines repository - SMDCG | Repositório de pipelines - SMDCG</h3>
  <p align="center">
    This repository aims to organize and share the pipelines developed for SMDCG - Secretaria Municipal De Defesa Civil E Geotecnia De Niterói
  </p>
  <p>
    Esse repositório tem como objetivo organizar e compartilhar as pipelines desenvolvidas para a SMDCG - Secretaria Municipal De Defesa Civil E Geotecnia De Niterói
  </p>
  <p><a href="https://github.com/SIGeo-Niteroi/scripts/issues">Report Bug</a></p>
</div>

<details>
  <summary>Table of contents | Súmario</summary>
  <ol>
    <li>
      <a href="#about-the-repository--sobre-o-repositório">About The Repository | Sobre O Repositório</a>
      <ul>
        <li><a href="#built-with--desenvolvido-com">Built With | Desenvolvido Com</a></li>
      </ul>
    </li>
    <li>
      <a href="#files--arquivos">Files | Arquivos</a>
      <ul>
        <li><a href="#pipelines">pipelines</a>
          <ul>
            <li><a href="#ncq">niterói_contra_queimadas</a></li>
            <li><a href="#svida">svida</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started | Inicializando</a>
      <ul>
        <li><a href="#prerequisites--pré-requisitos">Prerequisites | Pré-requisitos</a></li>
        <li><a href="#installation--instalação">Installation | Instalação</a></li>
      </ul>
    </li>
    <li><a href="#how-prefect-works">What is Prefect and how it works | O que é o Prefect e como ele funciona</a></li>
    <li><a href="#-contributing--contribuindo">Contributing | Contribuindo</a></li>
    <li><a href="#contact--contato">Contact | Contato</a></li>
    <li><a href="#contributors--contribuidores">Contributors | Contribuidores</a></li>
  </ol>
</details>

<h2 id="about-the-repository--sobre-o-repositório">About The Repository | Sobre O Repositório</h2>

<p>Welcome! This repository, created by the Data Office of the City of Niterói, organizes and shares the pipelines developed for Municipal Secretariat of Civil Defense and Geotechnics of Niterói.
<br></p>

<p>Bem vindo(a)! Este repositório, criado pelo Escritório de Dados da Prefeitura de Niterói, organiza e compartilha as pipelines desenvolvidas para a Secretaria Municipal De Defesa Civil E Geotecnia De Niterói.
<br></p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="built-with--desenvolvido-com">Built With | Desenvolvido Com</h2>

[![Python]][Python-url] [![Prefect]][Prefect-url]![env] ![Arcgis]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="files--arquivos">Files | Arquivos</h2>

<details id="pipelines">
  <summary>📁 pipelines</summary>
    <details>
      <summary>📁 niteroi_contra_queimadas</summary>
      <p>In this folder, you’ll find two pipelines developed to update fire-related data on the Niterói Contra Queimadas HUB <a href="https://niteroicontraqueimadas.niteroi.rj.gov.br/">🔗 niteroicontraqueimadas.niteroi.rj.gov.br</a></p>
      <ul>
        <li>
          <strong>fire-occurrences: </strong>TAutomatically updates a fire incident layer on ArcGIS Online (AGOL) using data from Niterói's Civil Defense API, ensuring data synchronization and supporting operational decision-making.
        </li>
        <li>
          <strong>fire_risk: </strong>Consolidates fire risk and meteorological data from Niterói's Civil Defense APIs into a record on ArcGIS Online to power a real-time alert system.
        </li>
      </ul>
      <p>Nesta pasta estão duas pipelines desenvolvidas para atualizar dados sobre incêndios no HUB Niterói Contra Queimadas <a href="https://niteroicontraqueimadas.niteroi.rj.gov.br/">🔗 niteroicontraqueimadas.niteroi.rj.gov.br</a></p>
      <ul>
        <li>
          <strong>fire-occurrences: </strong> Atualiza automaticamente uma camada de ocorrências de incêndio no ArcGIS Online (AGOL) com dados da API da Defesa Civil de Niterói, garantindo sincronização e apoiando a tomada de decisões operacionais.
        </li>
        <li>
          <strong>fire_risk:</strong> Consolida dados de risco de incêndio e meteorologia, recebidos das APIs da Defesa Civil de Niterói, em um registro no ArcGIS Online para alimentar um sistema de alertas em tempo real.
        </li>
      </ul>
    </details>
    <details>
      <summary>📁 svida</summary>
      <p>In this folder, you’ll find a pipeline that integrates Niterói's Civil Defense climate monitoring APIs with ArcGIS layers.</p>
      <ul>
        <li>
          <strong>📄 svida_integration: </strong>Integrates and updates geospatial and meteorological data — such as rain gauge locations, alert stages, emergency sirens, weather forecasts, localized climate data, public support points, and air quality alerts — from Niterói's Civil Defense APIs into ArcGIS platforms (Enterprise and AGOL), keeping layers and tables up to date in real time.
        </li>
      </ul>
      <p>Nesta pasta está uma pipeline que integra as APIs de monitoramento climático da Defesa Civil de Niterói com camadas do ArcGIS.</p>
      <ul>
        <li>
          <strong>📄 svida_integration: </strong>Integra e atualiza dados geoespaciais e meteorológicos — como localização de pluviômetros, estágios de atenção, sirenes de emergência, previsões do tempo, dados climáticos regionais, pontos de apoio à população e alertas de qualidade do ar — a partir das APIs da Defesa Civil de Niterói nas plataformas ArcGIS (Enterprise e AGOL), mantendo camadas e tabelas atualizadas em tempo real. 
        </li>
      </ul>
    </details>
</details>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
<h2 id="getting-started">Getting Started</h2>

<h3 id="prerequisites--pré-requisitos">Prerequisites | Pré-requisitos</h3>

- Python -> https://www.python.org/ (3.11 version | versão 3.11)

<h2 id="installation--instalação">Installation | Instalação</h2>

1. Clone the repo | Clone o repositório
   ```sh
   git clone https://github.com/...
   ```
2. Crie um âmbiente virtual na versão necessária para instalar as depenências e rodar o projeto
   ```sh
   py -3.11 -venv nome_do_ambiente
   ```
   - comando força a criação de um ambiente na versão indicada na flag. É necessário já ter o versão instalada na máquina
   
3. Install the dependencies needed to run this project | Instale as dependências necessárias para rodar o projeto:

<ul>
  <li></li>
</ul>

3. Create a .env local file based on the .env.example file | Crie um arquivo local .env baseado no arquivo .env.example
   *When necessary | quando necessário* 

4. Start the application | Rode o script
    ```sh
    ptyhon script.py
   ```
<p>
  ❗ NOTE: These pipelines are being executed by the Prefect Workflows manager, which saves the environment variables used. To use them locally, you will need to replace the variable values ​​as needed.

  ❗ OBS.: Essas pipelines estão sendo executadas pelo gerenciador de Workflows Prefect, que guarda as variáveis de âmbiente usadas. Para usar localmente será necessário que você substitua os valores das variáveis de acordo com a necessidade.
</p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>


<h2 id="how-prefect-works">What is Prefect and how it works | O que é o Prefect e como ele funciona</h2>

<p>
  O Prefect é uma ferramenta de orquestração de workflows que facilita a execução, o gerenciamento e o monitoramento de pipelines de dados e automações. Ele permite definir fluxos de trabalho como código Python e oferece recursos como agendamento, controle de dependências, logging e monitoramento.
</p>
<h3>Como ele executa pipelines do Github?</h3>
<ol>
  <li><strong>Código salvo no Github:</strong>
  <br>
  • O código do fluxo (flow) está no repositório do GitHub.
  </li>

  <li><strong>Definição de um Deployment do Prefect</strong>
  <br>
  • Define quando e como o fluxo será executado, indicamos no proprio código através do "@flow":
  <br>
  <code>
  @flow(name="waze-live-hist",log_prints=True)<br>
  def waze_live():
  try:
  </code>
  <br>
  • Ele pode ser configurado para rodar periodicamente (agendado) ou ser acionado manualmente.
  </li>

  <li><strong>Conexão do Prefect com o Repositório</strong>
  <br>
  • O Prefect pode buscar o código no GitHub automaticamente. Para isso, configura-se um Storage Block (GitHub block) no Prefect Cloud ou Prefect Server.
  </li>
  <li><strong>Execução do Pipeline</strong>
  <br>
  • Quando o fluxo é acionado (manualmente ou via agendamento), o Prefect baixa o código do GitHub e o executa na infraestrutura configurada.
  </li>
</ol>

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<h2 id="#-contributing--contribuindo">🤝 Contributing | Contribuindo</h2> 
Contributions are **greatly appreciated**! | Contribuições são **sempre bem vindas**!

If you have a suggestion that would make this project better, please fork the repo and create a pull request. You can also open an issue with the tag "enhancement".
<p>Se você possuir alguma sugestão que possa tornar esse projeto melhor, por favor fork esse repositório e crie um pull request. Você pode também abrir um issue com a tag "enhancement".</p>

1. Fork the Project | Fork o Projeto
2. Create your Feature Branch | Crie sua  Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes | Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch | Push para sua Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request | Abra um Pull Request

Thanks! Obrigado! 😄

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="contact--contato">Contact | Contato</h2>

Sistema de Gestão de Geoinformação - [Portal SIGeo](https://www.sigeo.niteroi.rj.gov.br/) - atendimento@sigeo.niteroi.rj.gov.br

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="contributors--contribuidores">Contributors | Contribuidores</h2>

<a href="https://github.com/niteroi-prefeitura/pipelines_smdcg/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=niteroi-prefeitura/pipelines_smdcg" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[Python]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
[Prefect]: https://img.shields.io/badge/Prefect-0c1b1f?style=for-the-badge&logo=prefect&logoColor=white
[Arcgis]: https://img.shields.io/badge/ArcGIS-2C7AC3.svg?style=for-the-badge&logo=ArcGIS&logoColor=white
[env]: https://img.shields.io/badge/.ENV-ECD53F.svg?style=for-the-badge&logo=dotenv&logoColor=black
[Python-url]: https://www.python.org/
[Prefect-url]: https://www.prefect.io/