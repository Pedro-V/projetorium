PU := plantuml
PU_FLAGS := 

diagrams := $(wildcard *.puml)
images := $(patsubst %.puml,%.png,$(diagrams))

all: $(images)

%.png: %.puml
	$(PU) $(PU_FLAGS) $^

clean:
	rm -rf *.png
