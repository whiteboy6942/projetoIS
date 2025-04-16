import graphene

class Esteroide(graphene.ObjectType):
    nome = graphene.String()
    preco = graphene.Float()
    categoria = graphene.String()
    em_stock = graphene.Boolean()

class Query(graphene.ObjectType):
    esteroides = graphene.List(Esteroide)

    def resolve_esteroides(parent, info):
        return [
            Esteroide(nome="Anavar", preco=55.00, categoria="Oral", em_stock=True),
            Esteroide(nome="Winstrol", preco=50.00, categoria="Oral", em_stock=True),
            Esteroide(nome="Trembolona", preco=70.00, categoria="Injetável", em_stock=False),
            Esteroide(nome="Sustanon 250", preco=65.00, categoria="Injetável", em_stock=True),
            Esteroide(nome="Deca-Durabolin", preco=60.00, categoria="Injetável", em_stock=False),
            Esteroide(nome="Dianabol", preco=45.00, categoria="Oral", em_stock=True),
        ]

schema = graphene.Schema(query=Query)

