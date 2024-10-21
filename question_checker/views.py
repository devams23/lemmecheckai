import io
from django.shortcuts import render, redirect
from .models import PDFUpload
from .forms import PDFUploadForm
from .geminiapi.app import parse_pdf ,get_numerical_questions , get_correct_answers

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
    # Get the questions from the session or wherever they are stored
    questions = get_numerical_questions()

    if request.method == 'POST':
        # Process the user's answers
        correct_answers = get_correct_answers(questions)
        for index, question in enumerate(questions, start=1):
            user_answer = request.POST.get(f'answer_{index}')  # Fetch answer for each question
                # In production, call your model to get the correct answer
            print(user_answer , question)
        print(correct_answers)
        return redirect('show_results')
    print(questions)
    return render(request, 'display_questions.html', {'questions': questions})




def show_results_view(request):
    
    return render(request, 'show_results.html', {'user_answers': []})
