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
    # questions_str = get_numerical_questions()  
    # questions_str = questions_str.replace('```json', '').replace('```', '').strip()
    
    # # Convert JSON string to list of questions
    # try:
    #     questions_anwers = json.loads(questions_str)
    #     print(questions_anwers)
    # except json.JSONDecodeError: 
    #     return render(request, 'error_page.html', {'error': 'Invalid question format'})
    
    questions_anwers = [{'question_name': 'Q.1 (a) (i)  Probability Calculation', 'questions': ['Find the probability of A union B'], 'answer': [0.4]}, {'question_name': 'Q.1 (a) (ii) Probability Calculation', 'questions': ['Find the probability of complement of A union B'], 'answer': [0.6]}, {'question_name': 'Q.1 (c) Bayes Theorem', 'questions': ['Find the probability of a scooter driver given that the driver had an accident'], 'answer': [0.0588]}, {'question_name': 'Q.2 (b) Mean and Standard Deviation', 'questions': ['Calculate the mean of the distribution', 'Calculate the standard deviation of the distribution'], 'answer': [12.11, 1.1391]}, {'question_name': 'Q.2 (c) (i) Sample Mean and Variance', 'questions': ['Calculate the sample mean of the heights', 'Calculate the sample variance of the heights'], 'answer': [65.81, 4.29]}, {'question_name': 'Q.2 (c) (iii) Median', 'questions': ['Find the median height'], 'answer': [66]}, {'question_name': 'Q.2 (c)  Quartiles and Interquartile Range', 'questions': ['Determine Q1', 'Determine Q3', 'Determine Q5', 'Calculate the interquartile range'], 'answer': [17.5, 25, 32.5, 7.5]}, {'question_name': 'Q.3 (b) Regression Lines', 'questions': ['Find the regression line of y on x', 'Find the regression line of x on y'], 'answer': ['y = 57.14 + 0.39x', 'x = 28.24 + 0.89y']}, {'question_name': 'Q.3 (c) Poisson Distribution', 'questions': ['Find the number of boxes with no defective bottles', 'Find the number of boxes with at least 2 defective bottles'], 'answer': [90, 2.6]}, {'question_name': 'Q.3 (b) Best Fitting Straight Line', 'questions': ['Find the equation of the best fitting straight line'], 'answer': ['y = 0.2 + 1.8x']}, {'question_name': 'Q.3 (c) Normal Distribution', 'questions': ['Find the number of bulbs expected to burn more than 2400 hours', 'Find the number of bulbs expected to burn between 1900 and 2300 hours'], 'answer': [228, 642]}, {'question_name': 'Q.5 (b) Hypothesis Testing', 'questions': ['Calculate the test statistic', 'Determine if the new product is significantly better'], 'answer': [2.86, 'Yes, the new product is significantly better']}, {'question_name': 'Q.5 (c) Poisson Distribution and Goodness of Fit', 'questions': ['Calculate the expected frequencies for each category', 'Calculate the chi-square test statistic', 'Determine the degrees of freedom', 'Determine the critical value at a significance level (e.g., 0.05)', 'Conclude whether to accept or reject the fit'], 'answer': [[209.18, 94.13, 21.19, 3.18, 0.32], [1.39], [2], [5.99], ['Accept the fit']]}]
    # Store questions in session
    request.session['questions'] = questions_anwers
    
    return render(request, 'display_questions.html', {'questions': questions_anwers})


def show_results_view(request):
    # Retrieve the updated questions with user answers from the session
    questions = request.session.get('questions', [])

    print("show results view" ,questions[0])
    for question in questions:
        question['paired_data'] = list(zip(question['questions'], question['answer'], question['user_answers']))
    print(questions[0])
    # Pass questions with user answers to the template
    return render(request, 'show_results.html', {'questions': questions})
