# Sistema de Informacao Nutricional - Etapa 3
Terceira e ultima etapa do trabalho da cadeira de desenvolvimento de software para persistência, com o uso de MongoDB Trabalho em conjunto LeviLeal

## Como rodar

```
git clone https://github.com/LeviLeal/informacao_nutricional_etapa_3.git
cd informacao_nutricional_etapa_3
uv run fastapi dev
```

## Diagrama 

classDiagram
    class Usuario {
        +String nome
        +int idade
        +float peso
    }

    class Alimento {
        +String nome
        +float calorias
        +float proteinas
        +float carboidratos
        +float gorduras
        +float sodio
        +float acucar
    }

    class Refeicao {
        +String tipo
        +date data
        +Usuario usuario
        +List~Alimento~ alimentos
    }

    Usuario --> "0..*" Refeicao : tem
    Refeicao --> "1" Usuario : pertence
    Refeicao --> "0..*" Alimento : inclui
    Alimento --> "0..*" Refeicao : está em
