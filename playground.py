import comparer
i = comparer.PMD()
f = i.get_compare_fun()
#print(f['Street']("1858 Sullivan Parkway", "1858 Sullivan Parkway", .65))

#print(f['Street']("1858 Sullivan Parkway", "	142 Summer Ridge Place", .65))
#print(f["Date of Birth"]("6/28/198/", "6/25/1988", .65))
#print(f["Sex"]("F", "Female", .65))
#print(f["State"]("New York", "NY", .65))

print(f["First Name"]("", "", .65))
