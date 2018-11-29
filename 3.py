file1=open("op.txt").read()
file2=open("outputs.txt","w+")
lines=file1.split("\n")
opline=""
for i in range(0,len(lines)):
	opline=","
	n_entries=lines[i].split(",")
	print len(n_entries)/8
	opline+=lines[i]
	n_extra=max(0,280-len(n_entries))
	for j in range(0,n_extra):
		opline+=",0"
	file2.write(opline)
	file2.write("\n")
print "Done"
		