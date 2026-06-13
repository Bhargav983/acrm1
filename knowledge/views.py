from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, FloatField, Q
from django.db.models.functions import Cast
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    AstrologyKnowledgeForm,
    CategoryForm,
    CustomerKnowledgeTrackingForm,
    HypothesisQuestionFormSet,
    HypothesisQuestionForm,
    ResearchInterviewForm,
    ResearchInterviewSelectForm,
    TrackingQuestionAnswerForm,
)
from .models import (
    AstrologyKnowledge,
    Category,
    CustomerKnowledgeTracking,
    CustomerResearchAnswer,
    HypothesisQuestion,
)


SYSTEM_SECTION_MAP = {
    'classical_astrology': [
        'lagna',
        'planet_in_house',
        'planet_in_sign',
        'planet_in_nakshatra',
        'planet_in_nakshatra_pada',
        'house_lord_in_house',
        'house_lord_in_sign',
        'house_lord_in_nakshatra',
        'house_lord_in_nakshatra_pada',
        'dasha',
        'transit',
        'dosha',
        'yoga',
        'divisional_chart',
    ],
    'bnn': [
        'planet_activation_age',
        'planet_combination',
        'planet_chain',
        'signification_transfer',
        'house_activation',
        'event_timing',
        'marriage_pattern',
        'career_pattern',
        'spiritual_pattern',
        'karmic_pattern',
    ],
    'kp': [
        'house_signification',
        'planet_significator',
        'cuspal_sub_lord',
        'marriage_rule',
        'career_rule',
        'child_birth_rule',
        'property_rule',
        'foreign_travel_rule',
        'health_rule',
        'event_timing',
    ],
    'numerology': [
        'life_path_number',
        'destiny_number',
        'soul_urge_number',
        'personality_number',
        'name_number',
        'personal_year_number',
        'compatibility',
        'career_pattern',
        'financial_pattern',
        'relationship_pattern',
        'health_pattern',
    ],
    'jaimini': [
        'atmakaraka',
        'amatyakaraka',
        'darakaraka',
        'karakamsha_lagna',
        'swamsha',
        'arudha_lagna',
        'pada_analysis',
        'chara_dasha',
        'upapada_lagna',
        'career_indicators',
        'marriage_indicators',
        'spiritual_indicators',
    ],
}


def build_research_library_tabs(records):
    section_labels = dict(AstrologyKnowledge.SECTION_CHOICES)
    records_by_system_section = {}
    for record in records:
        records_by_system_section.setdefault(record.system, {}).setdefault(
            record.section,
            [],
        ).append(record)

    tab_groups = []
    for system_value, system_label in AstrologyKnowledge.SYSTEM_CHOICES:
        section_tabs = []
        total_count = 0
        for section_value in SYSTEM_SECTION_MAP.get(system_value, []):
            section_records = records_by_system_section.get(system_value, {}).get(
                section_value,
                [],
            )
            total_count += len(section_records)
            section_tabs.append(
                {
                    'value': section_value,
                    'label': section_labels.get(section_value, section_value),
                    'records': section_records,
                    'count': len(section_records),
                }
            )

        tab_groups.append(
            {
                'value': system_value,
                'label': system_label,
                'sections': section_tabs,
                'count': total_count,
            }
        )
    return tab_groups


@login_required
def category_list(request):
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', 'active')
    categories = Category.objects.all()

    if status_filter == 'active':
        categories = categories.filter(is_active=True)
    elif status_filter == 'inactive':
        categories = categories.filter(is_active=False)

    if search_query:
        categories = categories.filter(
            Q(category_name__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    return render(
        request,
        'knowledge/category_list.html',
        {
            'page_title': 'Categories',
            'categories': categories,
            'search_query': search_query,
            'status_filter': status_filter,
        },
    )


@login_required
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    knowledge_count = category.knowledge_records.count()
    return render(
        request,
        'knowledge/category_detail.html',
        {
            'page_title': category.category_name,
            'category': category,
            'knowledge_count': knowledge_count,
        },
    )


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('knowledge:category_detail', pk=category.pk)
    else:
        form = CategoryForm()

    return render(
        request,
        'knowledge/category_form.html',
        {
            'page_title': 'Add Category',
            'form': form,
            'submit_label': 'Create Category',
        },
    )


@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('knowledge:category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        'knowledge/category_form.html',
        {
            'page_title': 'Edit Category',
            'form': form,
            'category': category,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def category_deactivate(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.is_active = False
        category.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'Category deactivated successfully.')
        return redirect('knowledge:category_list')

    return render(
        request,
        'knowledge/category_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Category',
            'category': category,
        },
    )


@login_required
def knowledge_list(request):
    search_query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('category', '')
    section_filter = request.GET.get('section', '')
    type_filter = request.GET.get('type', '')
    system_filter = request.GET.get('system', '')
    hypothesis_status_filter = request.GET.get('hypothesis_status', '')
    status_filter = request.GET.get('status', 'active')
    view_mode = request.GET.get('view', 'list')
    if view_mode not in ['list', 'tabs']:
        view_mode = 'list'
    knowledge_records = AstrologyKnowledge.objects.select_related(
        'category',
        'created_by',
        'updated_by',
    ).annotate(questions_count=Count('questions', filter=Q(questions__is_active=True)))

    if status_filter == 'active':
        knowledge_records = knowledge_records.filter(is_active=True)
    elif status_filter == 'inactive':
        knowledge_records = knowledge_records.filter(is_active=False)

    if category_filter:
        knowledge_records = knowledge_records.filter(category_id=category_filter)
    if system_filter:
        knowledge_records = knowledge_records.filter(system=system_filter)
    if section_filter:
        knowledge_records = knowledge_records.filter(section=section_filter)
    if type_filter:
        knowledge_records = knowledge_records.filter(knowledge_type=type_filter)
    if hypothesis_status_filter:
        knowledge_records = knowledge_records.filter(status=hypothesis_status_filter)

    if search_query:
        knowledge_records = knowledge_records.filter(
            Q(title__icontains=search_query)
            | Q(short_meaning__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(category__category_name__icontains=search_query)
            | Q(life_areas__icontains=search_query)
            | Q(applies_to_name__icontains=search_query)
            | Q(applies_to_subtype__icontains=search_query)
            | Q(related_factor__icontains=search_query)
            | Q(verification_question__icontains=search_query)
            | Q(expected_result__icontains=search_query)
        )

    knowledge_records = list(knowledge_records.order_by('system', 'section', 'title'))
    list_query_params = request.GET.copy()
    list_query_params['view'] = 'list'
    tabs_query_params = request.GET.copy()
    tabs_query_params['view'] = 'tabs'

    return render(
        request,
        'knowledge/knowledge_list.html',
        {
            'page_title': 'Research Library',
            'knowledge_records': knowledge_records,
            'tab_groups': build_research_library_tabs(knowledge_records),
            'categories': Category.objects.filter(is_active=True),
            'system_choices': AstrologyKnowledge.SYSTEM_CHOICES,
            'section_choices': AstrologyKnowledge.SECTION_CHOICES,
            'knowledge_type_choices': AstrologyKnowledge.KNOWLEDGE_TYPE_CHOICES,
            'hypothesis_status_choices': AstrologyKnowledge.STATUS_CHOICES,
            'search_query': search_query,
            'category_filter': category_filter,
            'system_filter': system_filter,
            'section_filter': section_filter,
            'type_filter': type_filter,
            'hypothesis_status_filter': hypothesis_status_filter,
            'status_filter': status_filter,
            'view_mode': view_mode,
            'list_view_query': list_query_params.urlencode(),
            'tabs_view_query': tabs_query_params.urlencode(),
        },
    )


@login_required
def knowledge_detail(request, pk):
    knowledge = get_object_or_404(
        AstrologyKnowledge.objects.select_related('category', 'created_by', 'updated_by')
        .prefetch_related('questions'),
        pk=pk,
    )
    answers = CustomerResearchAnswer.objects.select_related(
        'customer',
        'question',
        'answered_by',
    ).filter(hypothesis=knowledge)
    tracking_records = CustomerKnowledgeTracking.objects.select_related(
        'customer',
        'verified_by',
    ).filter(knowledge=knowledge)
    rating_average = answers.filter(question__question_type='rating').exclude(
        answer_value='',
    ).annotate(
        numeric_answer=Cast('answer_value', FloatField()),
    ).aggregate(average=Avg('numeric_answer'))['average']
    return render(
        request,
        'knowledge/knowledge_detail.html',
        {
            'page_title': knowledge.title,
            'knowledge': knowledge,
            'questions': knowledge.questions.all(),
            'answers': answers.order_by('-answered_date', '-created_at')[:25],
            'total_customers_answered': answers.values('customer').distinct().count(),
            'yes_count': answers.filter(answer_value='yes').count(),
            'no_count': answers.filter(answer_value='no').count(),
            'average_rating': rating_average,
            'final_applies_count': tracking_records.filter(status='applies').count(),
            'final_partial_count': tracking_records.filter(status='partially_applies').count(),
            'final_does_not_apply_count': tracking_records.filter(status='does_not_apply').count(),
        },
    )


@login_required
def knowledge_create(request):
    if request.method == 'POST':
        form = AstrologyKnowledgeForm(request.POST)
        question_formset = HypothesisQuestionFormSet(
            request.POST,
            queryset=HypothesisQuestion.objects.none(),
            prefix='questions',
        )
        if form.is_valid() and question_formset.is_valid():
            knowledge = form.save(commit=False)
            knowledge.created_by = request.user
            knowledge.updated_by = request.user
            knowledge.save()
            for question_form in question_formset:
                if not question_form.cleaned_data or not question_form.cleaned_data.get('question_text'):
                    continue
                question = question_form.save(commit=False)
                question.hypothesis = knowledge
                question.save()
            messages.success(request, 'Research hypothesis created successfully.')
            return redirect('knowledge:knowledge_detail', pk=knowledge.pk)
    else:
        form = AstrologyKnowledgeForm()
        question_formset = HypothesisQuestionFormSet(
            queryset=HypothesisQuestion.objects.none(),
            prefix='questions',
        )

    return render(
        request,
        'knowledge/knowledge_form.html',
        {
            'page_title': 'Add Research Hypothesis',
            'form': form,
            'question_formset': question_formset,
            'submit_label': 'Create Research Hypothesis',
        },
    )


@login_required
def knowledge_update(request, pk):
    knowledge = get_object_or_404(AstrologyKnowledge, pk=pk)
    if request.method == 'POST':
        form = AstrologyKnowledgeForm(request.POST, instance=knowledge)
        question_formset = HypothesisQuestionFormSet(
            request.POST,
            queryset=knowledge.questions.all(),
            prefix='questions',
        )
        if form.is_valid() and question_formset.is_valid():
            knowledge = form.save(commit=False)
            knowledge.updated_by = request.user
            knowledge.save()
            for question_form in question_formset:
                if not question_form.cleaned_data:
                    continue
                question_text = question_form.cleaned_data.get('question_text')
                if not question_form.instance.pk and not question_text:
                    continue
                question = question_form.save(commit=False)
                question.hypothesis = knowledge
                question.save()
            messages.success(request, 'Research hypothesis updated successfully.')
            return redirect('knowledge:knowledge_detail', pk=knowledge.pk)
    else:
        form = AstrologyKnowledgeForm(instance=knowledge)
        question_formset = HypothesisQuestionFormSet(
            queryset=knowledge.questions.all(),
            prefix='questions',
        )

    return render(
        request,
        'knowledge/knowledge_form.html',
        {
            'page_title': 'Edit Research Hypothesis',
            'form': form,
            'question_formset': question_formset,
            'knowledge': knowledge,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def knowledge_deactivate(request, pk):
    knowledge = get_object_or_404(AstrologyKnowledge, pk=pk)
    if request.method == 'POST':
        knowledge.is_active = False
        knowledge.updated_by = request.user
        knowledge.save(update_fields=['is_active', 'updated_by', 'updated_at'])
        messages.success(request, 'Research hypothesis deactivated successfully.')
        return redirect('knowledge:knowledge_list')

    return render(
        request,
        'knowledge/knowledge_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Research Hypothesis',
            'knowledge': knowledge,
        },
    )


@login_required
def hypothesis_question_create(request, hypothesis_pk):
    hypothesis = get_object_or_404(AstrologyKnowledge, pk=hypothesis_pk)
    if request.method == 'POST':
        form = HypothesisQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.hypothesis = hypothesis
            question.save()
            messages.success(request, 'Research question added successfully.')
            return redirect('knowledge:knowledge_detail', pk=hypothesis.pk)
    else:
        form = HypothesisQuestionForm()

    return render(
        request,
        'knowledge/hypothesis_question_form.html',
        {
            'page_title': 'Add Research Question',
            'hypothesis': hypothesis,
            'form': form,
            'submit_label': 'Add Question',
        },
    )


@login_required
def hypothesis_question_update(request, pk):
    question = get_object_or_404(
        HypothesisQuestion.objects.select_related('hypothesis'),
        pk=pk,
    )
    if request.method == 'POST':
        form = HypothesisQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, 'Research question updated successfully.')
            return redirect('knowledge:knowledge_detail', pk=question.hypothesis_id)
    else:
        form = HypothesisQuestionForm(instance=question)

    return render(
        request,
        'knowledge/hypothesis_question_form.html',
        {
            'page_title': 'Edit Research Question',
            'hypothesis': question.hypothesis,
            'question': question,
            'form': form,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def hypothesis_question_deactivate(request, pk):
    question = get_object_or_404(
        HypothesisQuestion.objects.select_related('hypothesis'),
        pk=pk,
    )
    if request.method == 'POST':
        question.is_active = False
        question.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'Research question deactivated successfully.')
        return redirect('knowledge:knowledge_detail', pk=question.hypothesis_id)

    return render(
        request,
        'knowledge/hypothesis_question_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Research Question',
            'question': question,
            'hypothesis': question.hypothesis,
        },
    )


@login_required
def research_interview_select(request, customer_pk):
    from customers.models import Customer

    customer = get_object_or_404(Customer, pk=customer_pk)
    if request.method == 'POST':
        form = ResearchInterviewSelectForm(request.POST)
        if form.is_valid():
            hypothesis = form.cleaned_data['hypothesis']
            return redirect(
                'knowledge:research_interview',
                customer_pk=customer.pk,
                hypothesis_pk=hypothesis.pk,
            )
    else:
        form = ResearchInterviewSelectForm()

    return render(
        request,
        'knowledge/research_interview_select.html',
        {
            'page_title': 'Start Research Interview',
            'customer': customer,
            'form': form,
        },
    )


@login_required
def research_interview(request, customer_pk, hypothesis_pk):
    from customers.models import Customer

    customer = get_object_or_404(Customer, pk=customer_pk)
    hypothesis = get_object_or_404(AstrologyKnowledge, pk=hypothesis_pk, is_active=True)
    questions = list(hypothesis.questions.filter(is_active=True))
    existing_answers = {
        answer.question_id: answer
        for answer in CustomerResearchAnswer.objects.filter(
            customer=customer,
            hypothesis=hypothesis,
            question__in=questions,
        )
    }
    initial = {}
    for question in questions:
        answer = existing_answers.get(question.pk)
        if answer:
            initial[ResearchInterviewForm.answer_field_name(question)] = (
                answer.answer_value or answer.answer_text
            )
            initial[ResearchInterviewForm.notes_field_name(question)] = answer.notes

    tracking = CustomerKnowledgeTracking.objects.filter(
        customer=customer,
        knowledge=hypothesis,
        tracking_type='research_answer',
    ).first()
    if tracking:
        initial['final_status'] = tracking.status
        initial['researcher_notes'] = tracking.researcher_notes
        initial['verified_date'] = tracking.verified_date

    if request.method == 'POST':
        form = ResearchInterviewForm(request.POST, questions=questions)
        if form.is_valid():
            today = timezone.localdate()
            for question in questions:
                answer_value = form.cleaned_data.get(
                    ResearchInterviewForm.answer_field_name(question),
                )
                notes = form.cleaned_data.get(
                    ResearchInterviewForm.notes_field_name(question),
                    '',
                )
                answer_value = '' if answer_value is None else str(answer_value)
                answer_text = answer_value
                if not answer_value and not notes:
                    continue
                CustomerResearchAnswer.objects.update_or_create(
                    customer=customer,
                    hypothesis=hypothesis,
                    question=question,
                    defaults={
                        'answer_text': answer_text,
                        'answer_value': answer_value,
                        'notes': notes,
                        'answered_by': request.user,
                        'answered_date': today,
                    },
                )

            CustomerKnowledgeTracking.objects.update_or_create(
                customer=customer,
                knowledge=hypothesis,
                tracking_type='research_answer',
                defaults={
                    'status': form.cleaned_data['final_status'],
                    'researcher_notes': form.cleaned_data.get('researcher_notes', ''),
                    'verified_by': request.user,
                    'verified_date': form.cleaned_data.get('verified_date') or today,
                    'is_active': True,
                },
            )
            messages.success(request, 'Research interview saved successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = ResearchInterviewForm(questions=questions, initial=initial)

    return render(
        request,
        'knowledge/research_interview_form.html',
        {
            'page_title': 'Research Interview',
            'customer': customer,
            'hypothesis': hypothesis,
            'questions': questions,
            'question_fields': [
                (
                    question,
                    form[ResearchInterviewForm.answer_field_name(question)],
                    form[ResearchInterviewForm.notes_field_name(question)],
                )
                for question in questions
            ],
            'form': form,
        },
    )


def get_tracking_question_context(customer_id, hypothesis_id, post_data=None):
    questions = []
    initial = {}
    if customer_id and hypothesis_id:
        questions = list(
            HypothesisQuestion.objects.filter(
                hypothesis_id=hypothesis_id,
                is_active=True,
            ).order_by('sort_order', 'id')
        )
        existing_answers = {
            answer.question_id: answer
            for answer in CustomerResearchAnswer.objects.filter(
                customer_id=customer_id,
                hypothesis_id=hypothesis_id,
                question__in=questions,
            )
        }
        for question in questions:
            answer = existing_answers.get(question.pk)
            if answer:
                initial[TrackingQuestionAnswerForm.answer_field_name(question)] = (
                    answer.answer_value or answer.answer_text
                )
                initial[TrackingQuestionAnswerForm.notes_field_name(question)] = answer.notes

    answer_form = TrackingQuestionAnswerForm(
        post_data,
        questions=questions,
        initial=initial if post_data is None else None,
    )
    return questions, answer_form


def save_tracking_question_answers(answer_form, customer, hypothesis, user):
    today = timezone.localdate()
    for question in answer_form.questions:
        answer_value = answer_form.cleaned_data.get(
            TrackingQuestionAnswerForm.answer_field_name(question),
        )
        notes = answer_form.cleaned_data.get(
            TrackingQuestionAnswerForm.notes_field_name(question),
            '',
        )
        answer_value = '' if answer_value is None else str(answer_value)
        answer_text = answer_value
        if not answer_value and not notes:
            continue
        CustomerResearchAnswer.objects.update_or_create(
            customer=customer,
            hypothesis=hypothesis,
            question=question,
            defaults={
                'answer_text': answer_text,
                'answer_value': answer_value,
                'notes': notes,
                'answered_by': user,
                'answered_date': today,
            },
        )


@login_required
def tracking_list(request):
    search_query = request.GET.get('q', '').strip()
    tracking_type_filter = request.GET.get('tracking_type', '')
    status_filter = request.GET.get('status', '')
    outcome_filter = request.GET.get('outcome', '')
    active_filter = request.GET.get('active', 'active')
    tracking_records = CustomerKnowledgeTracking.objects.select_related(
        'customer',
        'knowledge',
        'verified_by',
    )

    if active_filter == 'active':
        tracking_records = tracking_records.filter(is_active=True)
    elif active_filter == 'inactive':
        tracking_records = tracking_records.filter(is_active=False)

    if tracking_type_filter:
        tracking_records = tracking_records.filter(tracking_type=tracking_type_filter)
    if status_filter:
        tracking_records = tracking_records.filter(status=status_filter)
    if outcome_filter:
        tracking_records = tracking_records.filter(outcome=outcome_filter)

    if search_query:
        tracking_records = tracking_records.filter(
            Q(customer__customer_name__icontains=search_query)
            | Q(knowledge__title__icontains=search_query)
        )

    return render(
        request,
        'knowledge/tracking_list.html',
        {
            'page_title': 'Research Tracking',
            'tracking_records': tracking_records,
            'search_query': search_query,
            'tracking_type_filter': tracking_type_filter,
            'status_filter': status_filter,
            'outcome_filter': outcome_filter,
            'active_filter': active_filter,
            'tracking_type_choices': CustomerKnowledgeTracking.TRACKING_TYPE_CHOICES,
            'status_choices': CustomerKnowledgeTracking.STATUS_CHOICES,
            'outcome_choices': CustomerKnowledgeTracking.OUTCOME_CHOICES,
        },
    )


@login_required
def tracking_detail(request, pk):
    tracking = get_object_or_404(
        CustomerKnowledgeTracking.objects.select_related(
            'customer',
            'knowledge',
            'knowledge__category',
            'verified_by',
        ),
        pk=pk,
    )
    return render(
        request,
        'knowledge/tracking_detail.html',
        {
            'page_title': 'Research Summary Detail',
            'tracking': tracking,
        },
    )


@login_required
def tracking_create(request):
    if request.method == 'POST':
        form = CustomerKnowledgeTrackingForm(request.POST)
        customer_id = request.POST.get('customer')
        knowledge_id = request.POST.get('knowledge')
        questions, answer_form = get_tracking_question_context(
            customer_id,
            knowledge_id,
            request.POST,
        )
        if form.is_valid() and answer_form.is_valid():
            tracking = form.save(commit=False)
            if not tracking.verified_by_id:
                tracking.verified_by = request.user
            tracking.save()
            save_tracking_question_answers(
                answer_form,
                tracking.customer,
                tracking.knowledge,
                request.user,
            )
            messages.success(request, 'Research summary created successfully.')
            return redirect('knowledge:tracking_detail', pk=tracking.pk)
    else:
        initial = {}
        customer_id = request.GET.get('customer')
        knowledge_id = request.GET.get('knowledge')
        if customer_id:
            initial['customer'] = customer_id
        if knowledge_id:
            initial['knowledge'] = knowledge_id
        initial['verified_by'] = request.user
        form = CustomerKnowledgeTrackingForm(initial=initial)
        questions, answer_form = get_tracking_question_context(customer_id, knowledge_id)

    return render(
        request,
        'knowledge/tracking_form.html',
        {
            'page_title': 'Add Research Summary',
            'form': form,
            'answer_form': answer_form,
            'questions': questions,
            'question_fields': [
                (
                    question,
                    answer_form[TrackingQuestionAnswerForm.answer_field_name(question)],
                    answer_form[TrackingQuestionAnswerForm.notes_field_name(question)],
                )
                for question in questions
            ],
            'submit_label': 'Create Research Summary',
        },
    )


@login_required
def tracking_update(request, pk):
    tracking = get_object_or_404(CustomerKnowledgeTracking, pk=pk)
    if request.method == 'POST':
        form = CustomerKnowledgeTrackingForm(request.POST, instance=tracking)
        customer_id = request.POST.get('customer')
        knowledge_id = request.POST.get('knowledge')
        questions, answer_form = get_tracking_question_context(
            customer_id,
            knowledge_id,
            request.POST,
        )
        if form.is_valid() and answer_form.is_valid():
            tracking = form.save(commit=False)
            if not tracking.verified_by_id:
                tracking.verified_by = request.user
            tracking.save()
            save_tracking_question_answers(
                answer_form,
                tracking.customer,
                tracking.knowledge,
                request.user,
            )
            messages.success(request, 'Research summary updated successfully.')
            return redirect('knowledge:tracking_detail', pk=tracking.pk)
    else:
        form = CustomerKnowledgeTrackingForm(instance=tracking)
        questions, answer_form = get_tracking_question_context(
            tracking.customer_id,
            tracking.knowledge_id,
        )

    return render(
        request,
        'knowledge/tracking_form.html',
        {
            'page_title': 'Edit Research Summary',
            'form': form,
            'answer_form': answer_form,
            'questions': questions,
            'question_fields': [
                (
                    question,
                    answer_form[TrackingQuestionAnswerForm.answer_field_name(question)],
                    answer_form[TrackingQuestionAnswerForm.notes_field_name(question)],
                )
                for question in questions
            ],
            'tracking': tracking,
            'submit_label': 'Save Changes',
        },
    )


@login_required
def tracking_deactivate(request, pk):
    tracking = get_object_or_404(CustomerKnowledgeTracking, pk=pk)
    if request.method == 'POST':
        tracking.is_active = False
        tracking.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'Research summary deactivated successfully.')
        return redirect('knowledge:tracking_list')

    return render(
        request,
        'knowledge/tracking_confirm_deactivate.html',
        {
            'page_title': 'Deactivate Research Summary',
            'tracking': tracking,
        },
    )
