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