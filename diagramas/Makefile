PU := plantuml
PU_FLAGS := 

diagrams := \
	usecase	\
	classe_dominio	\
	classe_projeto


all: $(diagrams)

usecase: usecase.puml
	$(PU) $(PU_FLAGS) $^

classe_dominio: classe_dominio.puml
	$(PU) $(PU_FLAGS) $^

classe_projeto: classe_projeto.puml
	$(PU) $(PU_FLAGS) $^

clean:
	rm -rf *.png
