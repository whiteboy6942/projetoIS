Projeto de Serviços Web Multitecnologia

Este repositório contém a implementação de um sistema de catálogo de esteroides anabolizantes utilizando diferentes tecnologias de serviços web: REST, SOAP, gRPC e GraphQL.

---

 Estrutura do Projeto

```
projeto/
├── cliente_graphql.py
├── cliente_rest.py
├── cliente_soap.py
├── produtos.json
├── produtos.xml
├── schema.py
├── schema.json
├── server_graphql.py
├── server_rest.py
├── server_soap.py
├── app.py
├── grpc/
│   └── ...
├── soap/
│   └── ...
├── rest/
│   └── app.py
└── graphql/
    └── server_graphql.py
```

---

Tecnologias Utilizadas

- REST com Flask
- SOAP com Spyne
- GraphQL com Flask + Graphene
- gRPC com `grpcio` e `protobuf`

---

 Funcionalidades

 REST

- Listar esteroides
- Adicionar esteroide
- Atualizar esteroide
- Remover esteroide
- Importação/exportação em JSON e XML

SOAP

- Listagem e adição de esteroides com validação via XSD

GraphQL

- Query de esteroides
- Mutation para adicionar

 gRPC

- Listagem e adição de esteroides

---
Como Executar

 1. Ativar ambiente virtual

bash
source venv-rest/bin/activate  # ou venv-graphql, etc.


2. Executar o servidor REST

bash
python rest/app.py


 3. Testar com curl

bash
curl http://localhost:5000/esteroides


 4. Executar servidor GraphQL

bash
python graphql/server_graphql.py


A interface interativa GraphiQL estará acessível em:


http://localhost:5002/graphql


5. Executar servidor SOAP

bash
python server_soap.py


6. Executar servidor gRPC

bash
python grpc/server_grpc.py




 Importação de Dados

 JSON

bash
curl -X POST http://localhost:5000/importar/json

 XML

bash
curl -X POST http://localhost:5000/importar/xml
```

---

Observações

- Todos os servidores escutam localmente nas suas respetivas portas:
  - REST: `5000`
  - GraphQL: `5002`
  - SOAP: `8000`
  - gRPC: `50051`

---

Autor

Bernardo Cebola — Projeto para a UC de Integração de Sistemas 

