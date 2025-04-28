q1:
	python3 questions/Question1.py
	
q2:
	python3 questions/Question2.py

q3:
	python3 questions/Question3.py

q4:
	python3 questions/Question4.py

q5: #la question 5 lance la question 6 car ce sont les mêmes questions
	python3 questions/Question6.py

q6:
	python3 questions/Question6.py

q7:
	python3 questions/Question7.py

q8:
	python3 questions/Question8.py

q9:
	python3 questions/Question9.py

q10:
	python3 questions/Question10.py

q11:
	python3 questions/Question11.py

q12:
	python3 questions/Question12.py

mt:
	@make q8 && make q9 && make q10 && make q11 && make q12

ac:
	@make q1 && make q2 && make q3 && make q4 && make q6 && make q7

#Exemple d'utilisation:
# make q13 MACHINE=Machines/machine_0egal1.txt MOT=0101
q13:
	python3 main.py $(MACHINE) $(MOT)