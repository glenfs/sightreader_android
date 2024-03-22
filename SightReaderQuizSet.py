class SightReaderQuizSet:
    questions = []
    clef = None
    notes = []

    def __init__(self):
        self.questions = []
        self.clef = ""
        self.notes = []

    def __init__(self, questions, clef, notes):
        self.questions = questions
        self.clef = clef
        self.notes = notes

    def add_question(self, question, user_response, is_correct, stem_points, label_pos, label_size, label_text, num_of_ledger,note_pos,note_size,ledger_point):
        self.questions.append(
            {'question': question, 'response': user_response, 'is_correct': is_correct, 'label_pos': label_pos,
             'label_size': label_size, 'label_text': label_text, 'num_of_ledger': num_of_ledger,'stem_points':stem_points,'note_pos':note_pos,'note_size':note_size,'ledger_point':ledger_point})

    def print_data(self):
        pass
        #print("$$$$$$ in print_data $$$$$")
        #for note in self.questions:
            #print(note['ledger_point'])
        #print("$$$$$$ end print_data $$$$$")

    def add_clef(self, clef):
        self.clef = clef

    def add_notes(self, note):
        self.notes.append(note)

    def get_notes(self):
        return self.notes

    def get_clef(self):
        return self.clef

    def copy(self):
        new_instance = SightReaderQuizSet(questions=self.questions, clef=self.clef, notes=self.notes)
        return new_instance
