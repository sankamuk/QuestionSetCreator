import sys
import pandas as pd
from random import randint

# Class denoting a question instance
class Question:
    def __init__(self, question, answer_01, answer_02, answer):
        self.question = question
        self.answer_option_01 = answer_01
        self.answer_option_02 = answer_02
        self.answer = answer

    def isQuestion(self, question):
        if self.question == question:
            return 0
        else:
            return 1

    def print_no_answer(self):
        return "Question: " + str(self.question) + "\nOptions: \n(A) " + str(self.answer_option_01) + "\n(B) " + str(self.answer_option_02) + "\n"

    def print_with_answer(self):
        return "Question: " + str(self.question) + "\nOptions: \n(A) " + str(self.answer_option_01) + "\n(B) " + str(self.answer_option_02) + "\nAnswer: \n" + str(self.answer) + "\n"


# Class denoting a library of questions for a specific subject
class Subject_Questions:
    def __init__(self, subject):
        self.subject = subject
        self.simple_question = 0
        self.difficult_question = 0
        self.simple_question_set = dict()
        self.difficult_question_set = dict()

    def add_question(self, difficulty, question, answer01, answer02, answer):
        if difficulty == "SIMPLE" :
            self.simple_question += 1
            questn = Question(question, answer01, answer02, answer)
            self.simple_question_set["question_"+str(self.simple_question)] = questn
        else:
            self.difficult_question += 1
            questn = Question(question, answer01, answer02, answer)
            self.difficult_question_set["question_"+str(self.difficult_question)] = questn

    def get_simple_question(self, number):
        return_list = []
        return_list_marker = []
        count = 0
        while count < number:
            random_number = randint(1, self.simple_question)
            if random_number not in return_list_marker:
                return_list_marker.append(random_number)
                return_list.append(self.simple_question_set["question_"+str(random_number)])
                count += 1
        return return_list

    def get_difficult_question(self, number):
        return_list = []
        return_list_marker = []
        count = 0
        while count < number:
            random_number = randint(1, self.difficult_question)
            if random_number not in return_list_marker:
                return_list_marker.append(random_number)
                return_list.append(self.difficult_question_set["question_"+str(random_number)])
                count += 1
        return return_list

    def get_total_question(self):
        return self.simple_question + self.difficult_question

# Class representing the complete question database
class Questions_DB:
    def __init__(self):
        self.total_question = 0
        self.question_set = dict()

    def add_question(self, subject, difficulty, question, answer01, answer02, answer):
        self.total_question += 1
        if subject in self.question_set.keys():
            subject_set = self.question_set[subject]
            subject_set.add_question(difficulty, question, answer01, answer02, answer)
        else:
            self.question_set[subject] = Subject_Questions(subject)
            subject_set = self.question_set[subject]
            subject_set.add_question(difficulty, question, answer01, answer02, answer)

    def return_subject_question(self, subject):
        return self.question_set[subject]

    def print_DB(self):
        for subject in self.question_set.keys():
            subject_set = self.return_subject_question(subject)
            print("Subject: " + subject + ", Difficulty: Hard.")
            for question_id in subject_set.difficult_question_set.keys():
                print(subject_set.difficult_question_set[question_id].print_with_answer())
            print("Subject: " + subject + ", Difficulty: Simple.")
            for question_id in subject_set.simple_question_set.keys():
                print(subject_set.simple_question_set[question_id].print_with_answer())

    def load_DB(self, db_file, sheet_name):
        df = pd.read_excel(db_file, sheet_name)
        for i in df.index:
            self.add_question(df['SUBJECT'][i], df['DIFFICULTY'][i], df['QUESTION'][i], df['POSSIBLE ANSWER 1'][i], df['POSSIBLE ANSWER 2'][i], df['CORRECT ANSWER'][i])


# MAIN SECTION
print("\n")
print("=======================================================================")
print("=                     QUESTION CREATOR TOOL                           =")
print("=======================================================================")
print("\n")
print("Loading database, please wait...")
db = Questions_DB()
db.load_DB('DB.xlsx', 'Feuil1')
print("Successfully loaded database.")
print("\n")
print("Below is the inputs to be provided by you before we generate the question paper for you.")
print("\n")
print("* The subjects identified from database to be available are provided below:\n")
print("|---------------------------|-----------------|-----------------|")
print("| %25s | %15s | %15s |" % ("Subject", "Difficult Qns", "Simple Qns"))
print("|---------------------------|-----------------|-----------------|")
for subject in db.question_set.keys():
    subject_set = db.return_subject_question(subject)
    print("| %25s | %15d | %15d |" % (subject, subject_set.difficult_question, subject_set.simple_question))
print("|---------------------------|-----------------|-----------------|")
print("\nNOTE:")
print("* For below question please provide 1. Total questions, 2. Questions per subject, 3. Total questions per difficulty level for each subject.")
print("* At any given point you cannot give value more than available in perticular catagory or overall question, thus plan your numbers accordingly.")
print("\n")
print("=======================================================================")
final_question_set = []
total_question = int(input("\nTotal number of question you want in the question(Maximum "+ str(db.total_question) +"): "))
if total_question > db.total_question:
    print("\nERROR: You cannot create question set more than available question. Exiting!!!\n")
    sys.exit(1)

for subject in db.question_set.keys():
    subject_set = db.return_subject_question(subject)
    diff_questn = int(input("\nTotal number of difficult question for "+ subject +"(Catagory Maximum "\
        + str(subject_set.difficult_question) +", Overall Maximum "+ str(total_question) +"): "))
    if ( diff_questn > subject_set.difficult_question ) or ( diff_questn > total_question ) :
        print("\nERROR: You cannot create question set with more questions available difficult question for subject "+ subject +". Exiting!!!\n")
        sys.exit(1)
    final_question_set.extend(subject_set.get_difficult_question(diff_questn))
    total_question = total_question - diff_questn
    if total_question == 0 :
        print("\nTotal questions requested has reached no more questions left to select. Thus stopping.")
        break
    simpl_questn = int(input("\nTotal number of simple question for "+ subject +"(Catagory Maximum "\
        + str(subject_set.simple_question) +", Overall Maximum "+ str(total_question) +"): "))
    if ( simpl_questn > subject_set.simple_question ) or ( simpl_questn > total_question ) :
        print("\nERROR: You cannot create question set with more questions available simple question for subject "+ subject +". Exiting!!!\n")
        sys.exit(1)
    final_question_set.extend(subject_set.get_simple_question(simpl_questn))
    total_question = total_question - simpl_questn
    if total_question == 0 :
        print("\nTotal questions requested has reached no more questions left to select. Thus stopping.")
        break

print("\n")
print("=======================================================================")
print("\n")
print("Thanks for your inputs, we are preparing your question set.")

print("\n")
with open("Question_Set_WithoutAnswer.txt", "w") as f1:
    count = 0
    for i in final_question_set:
        count += 1
        f1.write("- "+ str(count) +"_"+ i.print_no_answer() +"\n")
with open("Question_Set_WithAnswer.txt", "w") as f2:
    count = 0
    for i in final_question_set:
        count += 1
        f2.write("- "+ str(count) +"_"+ i.print_with_answer() +"\n")
print("Question set prepared. Question set with answer is in file Question_Set_WithAnswer.txt. Question set without answer is in file Question_Set_WithoutAnswer.txt.")
print("\n")
print("Thank you.")

