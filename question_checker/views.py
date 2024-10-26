import io
from django.shortcuts import render, redirect
from .models import PDFUpload
from .forms import PDFUploadForm
from .geminiapi.app import parse_pdf ,get_numerical_questions , get_correct_answers
import json


def upload_pdf(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')  # Get the uploaded file directly

        if pdf_file:
            # Call your parse_pdf function with the file-like object
            parse_pdf(pdf_file)
            
            # Store the questions in the session

            # Redirect to display the questions
            return redirect('display_questions')

    return render(request, 'upload_pdf.html')


def display_questions_view(request):
    if request.method == 'POST':
        # Retrieve the questions from the session
        questions = request.session.get('questions', [])
        
        # Loop through each question and collect answers
        for question_index, question in enumerate(questions, start=1):
            user_answers = []
            for sub_index in range(1, len(question["questions"]) + 1):
                answer_key = f'answer_{question_index}_{sub_index}'
                if answer_key in request.POST:
                    user_answer = request.POST[answer_key]
                    user_answers.append(user_answer)
            
            # Add the collected user answers to the question dictionary
            question['user_answers'] = user_answers
        
        # Update session with questions now containing user answers
        request.session['questions'] = questions

        return redirect('show_results_view')

    #Get questions from function and clean up format
    questions_str = get_numerical_questions()  
    questions_str = questions_str.replace('```json', '').replace('```', '').strip()
    
    # Convert JSON string to list of questions
    try:
        questions_anwers = json.loads(questions_str)
    except json.JSONDecodeError: 
        return render(request, 'error_page.html', {'error': 'Invalid question format'})
#     questions_anwers = [
# {
#     "question_name": "Q1.(a).Find probabilities",
#     "questions": ["union", "complement"],
#     "answer": ["0.4", "0.6"]
# },
# {
#     "question_name": "Q1.(c).Baye's Theorem",
#     "questions": ["probability"],
#     "answer": ["0.0588"]
# },
# {
#     "question_name": "Q2.(b).Mean and SD",
#     "questions": ["mean", "SD"],
#     "answer": ["12.05", "1.635"]
# },
# {
#     "question_name": "Q2.(c).Heights of female students",
#     "questions": ["mean", "variance", "median"],
#     "answer": ["65.78", "4.284", "66"]
# },
# {
#     "question_name": "Q2.(c).OR Quartile Range",
#     "questions": ["Q1", "Q3", "Q5", "IQR"],
#     "answer": ["17.5", "23.93", "27.5", "6.43"]
# },
# {
#     "question_name": "Q3.(b).Regression lines",
#     "questions": ["regression line of y on x", "regression line of x on y"],
#     "answer": ["y = 0.59x + 26.3", "x = 1.2y + 8.2"]
# },
# {
#     "question_name": "Q3.(c).Defective bottles",
#     "questions": ["boxes with no defects", "boxes with at least 2 defects"],
#     "answer": ["90.44", "9.56"]
# },
# {
#     "question_name": "Q3.(b).OR Best fitting line",
#     "questions": ["a", "b"],
#     "answer": ["0", "1.6"]
# },
# {
#     "question_name": "Q3.(c).OR Number of bulbs",
#     "questions": ["bulbs with >2400 hours", "bulbs between 1900-2300 hours"],
#     "answer": ["228", "642"]
# },
# {
#     "question_name": "Q5.(b).Tyre company claim",
#     "questions": ["t-value"],
#     "answer": ["5.03"]
# },
# {
#     "question_name": "Q5.(c).Mistakes per page",
#     "questions": ["chi-square value"],
#     "answer": ["1.58"]
# }
# ]
    # Store questions in session
    request.session['questions'] = questions_anwers
    
    return render(request, 'display_questions.html', {'questions': questions_anwers})


def show_results_view(request):
    # Retrieve the updated questions with user answers from the session
    questions = request.session.get('questions', [])
    print(questions)
    # Pass questions with user answers to the template
    return render(request, 'show_results.html', {'questions': questions})
