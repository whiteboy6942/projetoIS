import graphene

# Define os campos do esteroide
class Esteroide(graphene.ObjectType):
    nome = graphene.String()
    preco = graphene.Float()
    categoria = graphene.String()
    emStock = graphene.Boolean()

# Lista de esteroides simulada
esteroides_data = [
    {"nome": "Anavar", "preco": 55.0, "categoria": "Oral", "emStock": True},
    {"nome": "Winstrol", "preco": 50.0, "categoria": "Oral", "emStock": True},
]

# Query para listar esteroides
class Query(graphene.ObjectType):
    esteroides = graphene.List(Esteroide)

    def resolve_esteroides(self, info):
        return esteroides_data

# Mutation para adicionar esteroides
class AdicionarEsteroide(graphene.Mutation):
    class Arguments:
        nome = graphene.String()
        preco = graphene.Float()
        categoria = graphene.String()
        emStock = graphene.Boolean()

    esteroide = graphene.Field(lambda: Esteroide)

    def mutate(self, info, nome, preco, categoria, emStock):
        novo = {
            "nome": nome,
            "preco": preco,
            "categoria": categoria,
            "emStock": emStock
        }
        esteroides_data.append(novo)
        return AdicionarEsteroide(esteroide=novo)

# Mutation container
class Mutation(graphene.ObjectType):
    adicionarEsteroide = AdicionarEsteroide.Field()

# Exporta o schema
schema = graphene.Schema(query=Query, mutation=Mutation)

