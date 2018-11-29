from pprint import pprint
import ast
import json

pos_json_data=open("pos.json").read()
pos_data = json.loads(pos_json_data)

dep_json_data=open("dep.json").read()
dep_data = json.loads(dep_json_data)

pos_json_data=ast.literal_eval(json.dumps(pos_json_data))
dep_json_data=ast.literal_eval(json.dumps(dep_json_data))

FVfile=open("fv.txt","w+")

agreement_text=open("1.txt").read()
agreement_lines=agreement_text.split("\n")

from pycorenlp.corenlp import StanfordCoreNLP
host = "http://localhost"
port = "9000"
nlp = StanfordCoreNLP(host + ":" + port)

for iter in range(0,len(agreement_lines)):
	text = agreement_lines[iter]
	output = nlp.annotate(
		text,
		properties={
			"outputFormat": "json",
			"annotators": "depparse,lemma"
		}
	)


	output=ast.literal_eval(json.dumps(output))
	FV=""
	pprint(output)
	length_tokens=len(output["sentences"][0]["tokens"])
	print length_tokens
	print output["sentences"][0]["tokens"][1]["lemma"]
	tokens=output["sentences"][0]["tokens"]
	deps=output["sentences"][0]["basicDependencies"]
	for i in range(0,min(50,length_tokens)):
		maxsim=0
		FV+=","+str(sum(bytearray(tokens[i]["lemma"].lower()))-96*len(tokens[i]["lemma"]))
		print "lemma done!";
		pos=tokens[i]["pos"]
		if(pos in pos_data):
			pos_id=pos_data[pos]
			FV+=","+str(pos_id)
		else:
			FV+=",0"
		print "POS done!"
		print FV
		counter1=0
		counter2=0
		for l in range(0,len(deps)):
			if(deps[l]["governorGloss"].lower()==tokens[i]["lemma"].lower() and counter1<10):
				counter1+=1
				print "counter1="+str(counter1)
				depword=deps[l]["dependentGloss"]
			
				maxsim=0
				FV+=","+str(sum(bytearray(deps[l]["governorGloss"].lower()))-96*len(deps[l]["governorGloss"]))
				depstring=deps[l]["dep"]
				if(depstring in dep_data):
					dep_id=dep_data[depstring]
					FV+=","+str(dep_id)
				else:
					FV+=",0"
				dep_pos=""	
				for j in range(0,length_tokens):
					if(tokens[j]["word"].lower()==depword.lower()):
						dep_pos=tokens[j]["pos"]
						break
				if(dep_pos in dep_data):
					dep_pos_id=dep_data[dep_pos]
					FV+=""+str(dep_pos_id)
				else:
					FV+=",0"
				print "Done"
		for l in range(0,max(0,10-counter1)):
			FV+=",0,0,0"
		
		for l in range(0,len(deps)):
			if(deps[l]["dependentGloss"].lower()==tokens[i]["lemma"].lower() and counter2<10):
				counter2+=1
				print "counter2="+str(counter2)
				depword=deps[l]["governorGloss"]
			
				maxsim=0
				FV+=","+str(sum(bytearray(deps[l]["dependentGloss"].lower()))-96*len(deps[l]["dependentGloss"]))
				depstring=deps[l]["dep"]
				if(depstring in dep_data):
					dep_id=dep_data[depstring]
					FV+=","+str(dep_id)
				else:
					FV+=",0"
				dep_pos=""	
				for j in range(0,length_tokens):
					if(tokens[j]["word"].lower()==depword.lower()):
						dep_pos=tokens[j]["pos"]
						break
				if(dep_pos in dep_data):
					dep_pos_id=dep_data[dep_pos]
					FV+=","+str(dep_pos_id)
				else:
					FV+=",0"
				print "Done"
		for l in range(0,max(0,10-counter2)):
			FV+=",0,0,0"
	
	for i in range(0,max(0,50-length_tokens)):
		for j in range(0,62):
			FV+=",0"
	FV+="\n"
	FVfile.write(FV)
	print iter
	print len(FV.split(","))