from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from TestsGUI.models import Test, UserProgress, Question, Answer


@method_decorator(login_required, name='dispatch')
class Home(TemplateView):
    template_name = 'TestsGUI/main-page.html'

    # noinspection PyUnresolvedReferences
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the current user
        user = self.request.user

        # Filter active tests for the current user
        active_tests = Test.objects.filter(is_active=True)

        # Get the UserProgress records for the current user
        user_progress = UserProgress.objects.filter(user=user)

        test_data = []  # Initialize a list to store test data

        # Loop through active tests to prepare data for the template
        for test in active_tests:
            test_dict = {'test': test, 'question_url': None}  # Dictionary to store test data

            # Check if the user has progress for this test
            user_test_progress = user_progress.filter(test=test)

            if user_test_progress:
                # Get the first uncompleted question for the test
                sngt = user_test_progress.order_by('question__sequence_number').first().question.sequence_number

                first_uncompleted_question = Question.objects.filter(
                    test=test,
                    is_active=True,
                    sequence_number=sngt
                ).order_by('sequence_number').first()

                if first_uncompleted_question:
                    # Set the URL to the first uncompleted question
                    test_dict['question_url'] = f"tests/{test.slug}/{first_uncompleted_question.sequence_number}"

            else:
                # Get the lowest sequence number question for the test
                lowest_sequence_question = Question.objects.filter(
                    test=test,
                    is_active=True
                ).order_by('sequence_number').first()

                if lowest_sequence_question:
                    # Set the URL to the lowest sequence number question
                    test_dict['question_url'] = f"tests/{test.slug}/{lowest_sequence_question.sequence_number}"

            if test_dict.get('question_url'):
                test_data.append(test_dict)  # Add the test data to the list

        context['tests'] = test_data  # Add test data to the context

        return context


@method_decorator(login_required, name='dispatch')
class TestGenerator(TemplateView):
    template_name = 'TestsGUI/tests-page.html'

    # noinspection PyUnresolvedReferences
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Access captured URL parameters
        test_slug = self.kwargs.get('test_slug')
        sequence_number = self.kwargs.get('sequence_number')

        test = Test.objects.filter(slug=test_slug).first()
        question = Question.objects.filter(test=test, sequence_number=sequence_number).first()
        user = self.request.user
        user_test_progress = UserProgress.objects.filter(test=test, user=user, question=question)

        if not user_test_progress.exists():
            user_test_progress = UserProgress.objects.create(
                user=user,
                test=test,
                question=question,
                is_completed=False
            )
            user_test_progress.save()

        answers = Answer.objects.filter(question=question)

        context['question_text'] = question.question_text
        context['answers'] = answers

        return context


def logout_user(request):
    logout(request)

    return redirect('home')
