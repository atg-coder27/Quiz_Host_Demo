


from BaseApp.models import Quiz,Question
from datetime import datetime
def schedule():
    quizes = Quiz.objects.all()
    current_time = datetime.now()
    prev = None
    for quiz in quizes:
        if current_time < quiz.start_time:
            quiz.status = "Future"
        elif quiz.start_time <= current_time <= quiz.end_time:
            quiz.status = "Ongoing"
        else:
            quiz.status = "Completed"
        quiz.save()
        
        pt = 1
        questions = Question.objects.filter(quiz = quiz)
        for question in questions:
            question.current_no = pt
            pt += 1
            question.save()
        


    

    

    