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
        # Process the user's answers

        for i in range(5):
            user_answer = request.POST.get(f'answer_{i}')  # Fetch answer for each question
            print(user_answer)  # Print both user answer and question for debugging

        return redirect('show_results')
        # Get the questions from the session or wherever they are stored
    questions = [
    {
        "question_name": "Q1.(a).Find probabilities",
        "questions": ["union", "complement"],
        "answer": ["0.4", "0.6"]
    },
    {
        "question_name": "Q1.(c).Baye's Theorem",
        "questions": ["probability"],
        "answer": ["0.0588"]
    },
    {
        "question_name": "Q2.(b).Mean and SD",
        "questions": ["mean", "SD"],
        "answer": ["12.05", "1.635"]
    },
    {
        "question_name": "Q2.(c).Heights of female students",
        "questions": ["mean", "variance", "median"],
        "answer": ["65.78", "4.284", "66"]
    },
    {
        "question_name": "Q2.(c).OR Quartile Range",
        "questions": ["Q1", "Q3", "Q5", "IQR"],
        "answer": ["17.5", "23.93", "27.5", "6.43"]
    },
    {
        "question_name": "Q3.(b).Regression lines",
        "questions": ["regression line of y on x", "regression line of x on y"],
        "answer": ["y = 0.59x + 26.3", "x = 1.2y + 8.2"]
    },
    {
        "question_name": "Q3.(c).Defective bottles",
        "questions": ["boxes with no defects", "boxes with at least 2 defects"],
        "answer": ["90.44", "9.56"]
    },
    {
        "question_name": "Q3.(b).OR Best fitting line",
        "questions": ["a", "b"],
        "answer": ["0", "1.6"]
    },
    {
        "question_name": "Q3.(c).OR Number of bulbs",
        "questions": ["bulbs with >2400 hours", "bulbs between 1900-2300 hours"],
        "answer": ["228", "642"]
    },
    {
        "question_name": "Q5.(b).Tyre company claim",
        "questions": ["t-value"],
        "answer": ["5.03"]
    },
    {
        "question_name": "Q5.(c).Mistakes per page",
        "questions": ["chi-square value"],
        "answer": ["1.58"]
    }
]
    # questions_str = get_numerical_questions()  # Assuming it returns a JSON string with backticks

    # # Remove triple backticks and the word 'json' if present
    # questions_str = questions_str.replace('```json', '').replace('```', '').strip()
    # # Convert the string to a list/dictionary if it’s in JSON format
    # try:
    #     questions = json.loads(questions_str)
    #     print(questions)
    # except json.JSONDecodeError: 
    #     return render(request, 'error_page.html', {'error': 'Invalid question format'})
    
    return render(request, 'display_questions.html', {'questions': questions})




def show_results_view(request):
    
    return render(request, 'show_results.html', {'user_answers': []})
