import PyPDF2
from django.shortcuts import render, redirect
from .models import PDFUpload, Question, UserAnswer
from .forms import PDFUploadForm

def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_upload = form.save()
            # After saving the PDF, parse it
            parse_pdf(pdf_upload.pdf_file)
            return redirect('display_questions', pdf_id=pdf_upload.id)
    else:
        form = PDFUploadForm()

    return render(request, 'upload_pdf.html', {'form': form})

def parse_pdf(pdf_file):
    # Use PyPDF2 to extract text from PDF
    with open(pdf_file.path, 'rb') as f:
        reader = PyPDF2.PdfFileReader(f)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extractText()

            # Here, you'd have to write logic to detect numerical questions from the text
            # For now, let's assume it splits by newline
            questions = [line for line in text.split('\n') if is_numerical_question(line)]
            for question_text in questions:
                Question.objects.create(pdf_upload=pdf_file, question_text=question_text)

def is_numerical_question(text):
    # Basic check for a numerical question
    return any(char.isdigit() for char in text)


def display_questions_view(request, pdf_id):
    pdf_upload = PDFUpload.objects.get(id=pdf_id)
    questions = Question.objects.filter(pdf_upload=pdf_upload)

    if request.method == 'POST':
        for question in questions:
            user_answer = request.POST.get(f'answer_{question.id}')
            if user_answer:
                # In production, you will call your model (Gemini or any other) to get the correct answer
                correct_answer = call_gemini_model(question.question_text)
                is_correct = user_answer == correct_answer
                UserAnswer.objects.create(
                    question=question,
                    user_answer=user_answer,
                    correct_answer=correct_answer,
                    is_correct=is_correct
                )
        return redirect('show_results', pdf_id=pdf_upload.id)

    return render(request, 'display_questions.html', {'questions': questions})

def call_gemini_model(question_text):
    # This function interacts with the model to get the correct answer
    # For now, it’s a placeholder that always returns '42'
    return '42'

def show_results_view(request, pdf_id):
    pdf_upload = PDFUpload.objects.get(id=pdf_id)
    user_answers = UserAnswer.objects.filter(question__pdf_upload=pdf_upload)

    return render(request, 'question_checker/show_results.html', {'user_answers': user_answers})
