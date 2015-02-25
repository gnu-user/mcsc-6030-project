TEX = pdflatex -interaction nonstopmode
BIB = bibtex
 
PROPOSAL = proposal
PRELIMINARY = preliminary_report
FINAL = final_report
BIBFILE = references.bib
BUNDLE = all_reports.pdf

all: $(PROPOSAL).pdf clean

view: $(BUNDLE)
	open $(BUNDLE)
 
spell::
	ispell *.tex

clean::
	rm -fv *.aux *.log *.bbl *.blg *.toc *.out *.lot *.lof

clean-all::
	rm -fv *.aux *.log *.bbl *.blg *.toc *.out *.lot *.lof *.pdf

$(PROPOSAL).pdf: $(PROPOSAL).tex $(PROPOSAL).bbl 
	$(TEX) $(PROPOSAL) 
	$(TEX) $(PROPOSAL)
 
$(PROPOSAL).bbl: $(PROPOSAL).tex $(BIBFILE)
	$(TEX) $(PROPOSAL)
	$(BIB) $(PROPOSAL)
