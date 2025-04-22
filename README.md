

Este é um projeto realizado na UC de IS que implementa um sistema de gestão de produtos (esteroides) utilizando várias tecnologias de comunicação: REST, SOAP, gRPC e GraphQL.

## Tecnologias Usadas
- Python 3.12
- Flask
- Spyne (SOAP)
- gRPC
- Graphene (GraphQL)
- XML / JSON para importação e exportação de dados

## Estrutura
```
projeto/
├── rest/
│   ├── server_rest.py
│   └── produtos.json / produtos.xml
├── soap/
│   ├── server_soap.py
│   ├── produtos.xml / schema.xsd
├── grpc/
│   ├── server_grpc.py
│   └── esteroides.proto
├── graphql/
│   ├── server_graphql.py
│   └── schema.py
├── cliente/
    ├── cliente_rest.py
    ├── cliente_soap.py
    ├── cliente_grpc.py
    ├── cliente_graphql.py
    └── cliente_import_export.py
```

---

## Funções REST

### Importação JSON
- **Rota**: `/importar/json`
- **Método**: `POST`
- **Função**: Recebe um ficheiro JSON e guarda os dados no servidor.

### Exportação JSON
- **Rota**: `/exportar/json`
- **Método**: `GET`
- **Função**: Devolve os dados do servidor num ficheiro JSON para backup.

### Importação XML
- **Rota**: `/importar/xml`
- **Método**: `POST`
- **Função**: Recebe um ficheiro XML e guarda os dados no servidor.

### Exportação XML
- **Rota**: `/exportar/xml`
- **Método**: `GET`
- **Função**: Devolve os dados atuais do servidor num ficheiro XML para backup.

O cliente `cliente_import_export.py` permite interagir com estas funções, escolhendo entre importar e exportar dados.

---

## SOAP
- A função `adicionar_produto` permite validar dados com `schema.xsd` antes de guardar no `produtos.xml`.
- O cliente usa a biblioteca `suds` para fazer chamadas ao servidor.

## gRPC
- Define serviços no ficheiro `.proto`
- Suporta adicionar e listar produtos

## GraphQL
- Permite queries e mutations para gerir esteroides
- Usa o cliente `requests` para enviar queries ao endpoint `/graphql`

---

## Como executar
1. Ativar o ambiente virtual correspondente (ex: `source venv-rest/bin/activate`)
2. Executar o servidor (ex: `python3 server_rest.py`)
3. Abrir o cliente correspondente
4. Interagir com o sistema (listar, adicionar, importar/exportar)


