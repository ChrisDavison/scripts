INPUT=
INPSUFF=$(subst raw-collar,, $(INPUT))

inp: $(INPUT)
	@echo $(INPUT)
	@echo $(INPSUFF)

.PHONY: features classified raw
nool: $(INPUT)
	@echo "Removing outliers..." $^

features: $(INPUT)
	@echo "Features for: " $^
	@echo $(subst ' ',,features$(INPSUFF))

classified: features
	@echo "Classified: " $^

budgets: classified
	@echo "Time budgets: " $^

plots: budgets classified features nool $(INPUT)
	@echo "PLOTTING"
