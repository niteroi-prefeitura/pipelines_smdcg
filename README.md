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
    <li><a href="#usage--uso">Usage | Uso</a></li>
    <li><a href="#-contributing--contribuindo">Contributing | Contribuindo</a></li>
    <li><a href="#contact--contato">Contact | Contato</a></li>
    <li><a href="#contributors--contribuidores">Contributors | Contribuidores</a></li>
  </ol>
</details>

## About The Repository | Sobre O Repositório

<p>Welcome! This repository, created by the Data Office of the City of Niterói, organizes and shares the pipelines developed for Municipal Secretariat of Civil Defense and Geotechnics of Niterói.
<br></p>

<p>Bem vindo(a)! Este repositório, criado pelo Escritório de Dados da Prefeitura de Niterói, organiza e compartilha as pipelines desenvolvidas para a Secretaria Municipal De Defesa Civil E Geotecnia De Niterói.
<br></p>
<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With | Desenvolvido Com

[![Python]][Python-url] [![Prefect]][Prefect-url]![env] ![Arcgis]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h2 id="files--arquivos">Files | Arquivos</h2>

<details id="pipelines">
  <summary>📁 pipelines</summary>
    <details>
      <summary>📁 niteroi_contra_queimadas</summary>
      <p>In this folder we find two pipelines developed to generate updates on fires in the Niterói Contra Queimadas HUB <a href="https://niteroicontraqueimadas.niteroi.rj.gov.br/">🔗 niteroicontraqueimadas.niteroi.rj.gov.br</a></p>
      <ul>
        <li><strong>fire-occurrences:</strong></li>
        <li><strong>fire_risk:</strong></li>
      </ul>
      <p>Nesta pasta encontramos duas pipelines desenvolvidas para gerar as atualizações sobre incêndios no HUB de Niterói Contra Queimadas <a href="https://niteroicontraqueimadas.niteroi.rj.gov.br/">🔗 niteroicontraqueimadas.niteroi.rj.gov.br</a></p>
      <ul>
        <li><strong>fire-occurrences:</strong></li>
        <li><strong>fire_risk:</strong></li>
      </ul>
    </details>
    <details>
      <summary>📁 svida</summary>
      <p>In this folder we find two pipelines developed to generate updates on fires in the Niterói Contra Queimadas HUB</p>
      <ul>
        <li><strong>📄 fire-occurrences:</strong></li>
        <li><strong>📄 fire_risk:</strong></li>
      </ul>
      <p>Nesta pasta encontramos uma pipeline que faz a integração dos dados meteorológicos disponíbilizados pela defesa civil.</p>
      <ul>
        <li><strong>📄 svida_integration:</strong></li>
      </ul>
    </details>
</details>




<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

First, install the dependencies needed to run this project

<p>Primeiro, instale as dependências necessárias para rodar o projeto</p>

### Prerequisites | Pré-requisitos

- Python -> https://www.python.org/
- Arcpy -> https://pro.arcgis.com/en/pro-app/latest/arcpy/get-started/what-is-arcpy-.htm
- Arcgis.gis -> https://developers.arcgis.com/python/

### Installation | Instalação

1. Clone the repo | Clone o repositório
   ```sh
   git clone https://github.com/...
   ```

2. Install Libraries | Instale as bibliotecas

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


## Usage | Uso

Will be listed here the code's demo | Será inserido aqui uma demo do uso dos códigos

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 🤝 Contributing | Contribuindo
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

## Contact | Contato

Sistema de Gestão de Geoinformação - [Portal SIGeo](https://www.sigeo.niteroi.rj.gov.br/) - atendimento@sigeo.niteroi.rj.gov.br

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributors | Contribuidores

<a href="https://github.com/SIGeo-Niteroi/pipelines_smdcg/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=SIGeo-Niteroi/pipelines_smdcg" />
</a>

Made with [contrib.rocks](https://contrib.rocks).

<p align="right">(<a href="#readme-top">back to top</a>)</p>


[Python]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white
[Prefect]: https://img.shields.io/badge/Prefect-0c1b1f?style=for-the-badge&logo=prefect&logoColor=white
[Arcgis]: https://img.shields.io/badge/ArcGIS-2C7AC3.svg?style=for-the-badge&logo=ArcGIS&logoColor=white
[env]: https://img.shields.io/badge/.ENV-ECD53F.svg?style=for-the-badge&logo=dotenv&logoColor=black
[Python-url]: https://www.python.org/
[Prefect-url]: https://www.prefect.io/