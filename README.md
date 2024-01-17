# Projetorium

* Universidade Federal de Sergipe - Departamento de Computação
* COMP0438 - ENGENHARIA DE SOFTWARE I (2023.1 - T01)

* [Protótipos de telas](https://www.figma.com/team_invite/redeem/41WAUZlTE9xhkFDD1W9q3R)
* [Documento completo](https://docs.google.com/document/d/1_U4rpsdHIMNtEIF37tJauM6HSGS_AoE69NjjJnROhYg/edit?usp=sharing)

## Estrutura

* `diagramas/`: Código-fonte dos arquivos PUML e os binários gerados por eles.
* `documentos/`: Documentação, que reúne modelagem, requisitos e todos os
  artefatos do processo de engenharia de software.
* `reunioes/`: Anotações das reuniões com os professores, para futura
  referência.
* `dev/`: Desenvolvimento da aplicação: frontend, backend, SQL, entre outros.

## TODO

Tarefas com ??? é pq precisam de alguém para fazer.

### Urgente

- Revisar diagramas de sequência (DS).
  - Já revisados (5/9): AvaliarProposta, ConsultarProjeto, EscolherProjeto,OfertarProjeto, AdicionarAluno, AlterarAluno
  - Não permitir comunicação  `Entidade->Controle`, e `Ator->Ator`
  - Numerar mensagens 
  - Quem sabe informações (incluido existência) sobre uma determinada entidade
    são os próprios objetos daquela entidade.
    Ex: É um objeto da classe Registro que sabe dizer se um registro existe no
    sistema.
  - Manter apenas aspectos de lógica de negocios, retirar noções de interface gráfica.
  - A existência de um mêtodo no DS implica na existência desse método na
    respectiva classe no diagrama de classes.
  - A resposta final do diagrama pode ir direta à Tela.
  - OBS: Criar um diagrama de sequencia para o caso de uso "AlterarProfessor"

### Necessário

- Requisitos de manutenção de modelos
  - Turma: Rayan, Jonas
  - Aluno: Pedro V, Pedro A
  - Professor: Max, Carlos
- Remover classes irrelevantes do ER (Endereço, etc), atualizar cardinalidade de Turma-Aluno: Matheus

### Seria legal

- Dar uma estudada no sistema de templates do Django para fazer telas,
  [aqui](https://docs.djangoproject.com/en/5.0/topics/templates/) e 
  [aqui](https://docs.djangoproject.com/en/5.0/ref/templates/): Todos

## Membros

* [Carlos Eduardo](https://github.com/Eduardocesn) - 
* [Rayan Tavares](https://github.com/Rayan01261) - [rayantavaresjjba@academico.ufs.br](mailto:rayantavaresjjba@acadeimoc.ufs.br)
* [Pedro Vinícius](https://github.com/Pedro-V) - [pedrov2003@academico.ufs.br](mailto:pedrov2003@acadeimoc.ufs.br)
* [Max Antônio](https://github.com/Max-Antonio) - [antoniomax@academico.ufs.br](mailto:antoniomax@academico.ufs.br)
* [Jonas Gabriel](https://github.com/jonasgabrieel) - [jonasgab@academico.ufs.br](mailto:jonasgab@academico.ufs.br)
* [Matheus Fontes](https://github.com/Ultedad) - [matheusx123@academico.ufs.br](mailto:matheusx123@academico.ufs.br)
* [Pedro Augusto](https://github.com/PedroAgsto) - 
