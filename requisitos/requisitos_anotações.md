# Sistema Web pra Portfólio de Projetos de Engenharia de Software - Anotações

Este sistema possui o intuito de ser uma plataforma para gerenciar projetos de Engenharia de Software, nele os alunos propoem temas e a professora os analisa e gerencia. 

Projetos podem ser públicos ou privados.

Projetos grandes poderão ter subprojetos filhos.

NÃO é permitido excluir projetos.

Um projeto poderá ter várias versões (versão 1, versão 2 etc.) com alunos diferentes, onde os unicos atributos que serão mantidos são o nome e o código do projeto.

Um projeto PRECISA ter início e fim ou estimativa de fim.

## 1 - Atores

Os atores do sistema são: 

Aluno: 
-possui acesso a projetos públicos e projetos que participa;
-pode fazer propostas. 

professor: 
-possui acesso aos projetos das disciplinas que ensina;
-pode fazer propostas.

chefe de departamento: 
-possui acesso aos projetos do departamento que chefia.

gestor de sistema: 
-possui acesso a todo o sistema.
-analisa e aprova propostas.

administrador: 
-gerencia as partes mais técnicas.

Como pode ser visto existe uma hierarquia de acesso para os atores.

## 2 - Atributos de um projeto

Para que um projeto seja proposto é preciso que quem o propôs preencha certos atributos, estes atributos são:

- Área (Saúde, educação etc.).
- Ano.
- Nome (sigla).
- Descrição (objetivo).
- Fase do projeto (status).
- Entrega prevista.
- Origem (aluno ou professor).
- Departamento.
- Anexos (documentos).

Um código será atribuído ao projeto em sua criação. 

## 3 - Status de proposta e projeto

Antes de um projeto ser iniciado, é preciso que seja feito o cadastro de uma proposta onde serão preenchidos os atributos do projeto, nesse momento o estado da proposta é proposta em elaboração, nesse estado o usuário não precisa preencher tudo de uma vez, ele poderá sair e deixar os atributos salvos como rascunho e retomar o cadastro da proposta em um outro momento. Tanto o professor como o aluno podem fazer propostas.

Após os atributos serem preenchidos nossa proposta terá o estado de proposta em análise até que o gestor do sistema aprove e a proposta seja aceita. A partir desse momento, a proposta vira um projeto que pode ter os seguintes estados: Projeto a iniciar, fase inicial do projeto onde não foi feito progresso ainda; Projeto em execução, fase intermediária do projeto; Projeto concluído; Projeto inativo, não está sendo feito nenhum progresso no projeto; Projeto suspenso; Projeto cancelado.

## 4 - Consultas

No sistema é possível fazer consultas de acordo com o nível de acesso do usuário através de filtros de busca como status, periodo de início, período de fim, departamento, professor, aluno, ano etc.





