CXX ?= g++
CXXFLAGS ?= -O3 -std=c++17 -Wall
INC = include/gauss.hpp include/tracker.hpp include/loop_word.hpp
JOBS ?= 8

all: bin/e5_stacking bin/o6_heptagon bin/test_gauss bin/z8solve

bin/e5_stacking: src/e5_stacking.cpp $(INC) include/stacking_states.hpp
	@mkdir -p bin; $(CXX) $(CXXFLAGS) -Iinclude $< -o $@
bin/o6_heptagon: src/o6_heptagon.cpp $(INC) include/heptagon_states.hpp
	@mkdir -p bin; $(CXX) $(CXXFLAGS) -Iinclude $< -o $@
bin/test_gauss: src/test_gauss.cpp include/gauss.hpp
	@mkdir -p bin; $(CXX) $(CXXFLAGS) -Iinclude $< -o $@
bin/z8solve: src/z8solve.cpp
	@mkdir -p bin; $(CXX) $(CXXFLAGS) $< -o $@

# quick self-test (about a minute)
check: all
	bash tests/quick_check.sh $(JOBS)

# full tables in out/ (E5: 2^23 rows, O6: 2^25 rows), compared with data/SHA256.json
tables: all
	bash scripts/run_tables.sh $(JOBS) out

clean:
	rm -rf bin out

.PHONY: all check tables clean
