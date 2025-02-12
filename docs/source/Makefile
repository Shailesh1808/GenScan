outdir := html

doc:
	python -m sphinx -T -E -b html -d _build/doctrees -D language=en ./ $(outdir)

clean:
	rm -rf $(outdir) generated _build

cliref:
	echo "CLI reference for genscan" > cliref.rst
	echo "=======================" >> cliref.rst
	echo >> cliref.rst
	echo "::" >> cliref.rst
	echo >> cliref.rst
	cd ../.. ; python3 -m genscan --help | sed 's/^/  /' >> docs/source/cliref.rst

all: clean cliref doc