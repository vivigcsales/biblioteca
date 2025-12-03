# 📚 Backend Frameworks - Sistema de Biblioteca ✨

Este projeto implementa uma aplicação backend completa para um sistema de cadastro de livros, utilizando **Python** com os frameworks **Flask** (para a interface web) e **FastAPI** (para a API REST). 
O projeto simula um ambiente de desenvolvimento moderno onde a camada de frontend/web consome dados de uma API separada.

---

## ⚙️ Tecnologias Utilizadas

* **Linguagem:** Python
* **Banco de Dados:** SQLite (`biblioteca.db`)
* **Web Framework (UI):** Flask
    * **Requisições Externas:** `requests` (para integração com o FastAPI)
* **API Framework (REST):** FastAPI
    * **Validação de Dados:** Pydantic
    * **Servidor ASGI:** Uvicorn

# 💡 Estrutura do Projeto
O projeto é dividido em dois serviços distintos que demonstram a arquitetura de microserviços/APIs.

# (FastAPI - Camada de Dados) 📊
Implementa a lógica de negócio e as operações CRUD (Create, Read, Update, Delete) acessando diretamente o biblioteca.db.

# 🔑 Requisitos Técnicos Cumpridos
* Database: Criação do biblioteca.db (SQLite) com a tabela livros.

* Flask: Rota / com listagem e formulário HTML.

* FastAPI: Implementação completa de todos os endpoints CRUD (GET, POST, PUT, DELETE).

* Validação: Uso de Pydantic para validação de dados nos endpoints da API.

* Integração: O Flask consome a API FastAPI, demonstrando a separação de responsabilidades.
