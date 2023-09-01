PU := plantuml
PU_FLAGS := 

diagrams := \
	manter_professor\
	manter_aluno	\
	manter_turma	\
	efetuar_login	\
	propor_projeto	\
	avaliar_proposta\
	manter_projeto	\
	consultar_projeto \
	escolher_projeto

all: $(diagrams)

manter_professor: manter_professor.puml
	$(PU) $(PU_FLAGS) $^

manter_aluno: manter_aluno.puml
	$(PU) $(PU_FLAGS) $^

manter_turma: manter_turma.puml
	$(PU) $(PU_FLAGS) $^

efetuar_login: efetuar_login.puml
	$(PU) $(PU_FLAGS) $^

propor_projeto: propor_projeto.puml
	$(PU) $(PU_FLAGS) $^

avaliar_proposta: avaliar_proposta.puml
	$(PU) $(PU_FLAGS) $^

manter_projeto: manter_projeto.puml
	$(PU) $(PU_FLAGS) $^

consultar_projeto: consultar_projeto.puml
	$(PU) $(PU_FLAGS) $^

escolher_projeto: escolher_projeto.puml
	$(PU) $(PU_FLAGS) $^

clean:
	rm -rf *.png
