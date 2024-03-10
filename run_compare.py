
from ModuleTest import Compare


test_file = "EGFR_sequential_fit_2.ant"
comparison_file = 'test_1.ant'
# species = ['time', '[Lig]', '[Egfr]']

# comp = Compare(test_file, comparison_file, species)
comp = Compare(test_file, comparison_file)
comp.compare_trace()

print(comp.sim1)
print(comp.sim2)
print(comp.diff)
print()
print(comp.abs_diff)
