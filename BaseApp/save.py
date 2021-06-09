
from .models import CompletedChoiceMCQ, Quiz,Question,CompletedQuestion,ChoiceMCQ,ChoiceSubjective,CompletedChoiceSubjective,CompletedQuiz

def SaveToModel(id):
    print("Hit")
    instance = Quiz.objects.get(id = id)
    instance.status = "Completed"
    instance.save()
    quiz_instance = CompletedQuiz(
        category = instance.category,
        start_time = instance.start_time,
        end_time = instance.end_time
        )
    quiz_instance.save()
    questions_completed = Question.objects.filter(quiz = instance)
    for question in questions_completed:
        question_instance = CompletedQuestion(
            quiz = quiz_instance,
            title = question.title,
            type = question.type,
            total = question.total,
            current_no = question.current_no
        )
        question_instance.save()
        choice_completed = ChoiceMCQ.objects.filter(question = question)
        for choice in choice_completed:
            choice_instance = CompletedChoiceMCQ(
                question = question_instance,
                title = choice.title,
                select = choice.select,
                correct = choice.correct,
            )
            choice_instance.save()
