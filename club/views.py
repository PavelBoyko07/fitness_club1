from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.shortcuts import render




from .forms import ApplicationForm, LoginForm, RegisterForm, ReviewForm
from .models import (Application,ApplicationMembership,FitnessDirection,Membership,Review,ScheduleType,Stock,Trainer,TrainingType,Visit,)

def index(request):
    directions = FitnessDirection.objects.filter(is_active=True)[:6]
    memberships = Membership.objects.select_related('direction', 'training_type').filter(is_active=True)[:6]
    trainers = Trainer.objects.all()[:4]
    stocks = Stock.objects.filter(is_active=True)[:3]
    reviews = Review.objects.filter(is_published=True)[:3]
    context = {
        'directions': directions,
        'memberships': memberships,
        'trainers': trainers,
        'stocks': stocks,
        'reviews': reviews,
    }
    return render(request, 'index.html', context)

def membership_list(request):
    memberships = Membership.objects.select_related('direction', 'training_type').filter(is_active=True)
    context = {'memberships': memberships}
    return render(request, 'memberships/membership_list.html', context)

def membership_detail(request, slug):
    membership = get_object_or_404(
        Membership.objects.select_related('direction', 'training_type'),
        slug=slug,
        is_active=True,
    )
    trainers = Trainer.objects.filter(membership_trainers__membership=membership)
    context = {'membership': membership, 'trainers': trainers}
    return render(request, 'memberships/membership_detail.html', context)

def direction_detail(request, slug):
    direction = get_object_or_404(FitnessDirection, slug=slug, is_active=True)
    memberships = Membership.objects.filter(direction=direction, is_active=True)
    context = {'direction': direction, 'memberships': memberships}
    return render(request, 'directions/direction_detail.html', context)

def training_type_list(request):
    training_types = TrainingType.objects.all()
    context = {'training_types': training_types}
    return render(request, 'training_types/training_type_list.html', context)

def trainer_list(request):
    trainers = Trainer.objects.all()
    context = {'trainers': trainers}
    return render(request, 'trainers/trainer_list.html', context)

def trainer_detail(request, pk):
    trainer = get_object_or_404(Trainer, pk=pk)
    memberships = Membership.objects.filter(membership_trainers__trainer=trainer, is_active=True)
    context = {'trainer': trainer, 'memberships': memberships}
    return render(request, 'trainers/trainer_detail.html', context)

@login_required
def application_list(request):
    if request.user.is_staff:
        applications = Application.objects.select_related('user').all()
    else:
        applications = Application.objects.select_related('user').filter(user=request.user)
    context = {'applications': applications}
    return render(request, 'applications/application_list.html', context)

@login_required
def application_detail(request, pk):
    if request.user.is_staff:
        application = get_object_or_404(Application, pk=pk)
    else:
        application = get_object_or_404(Application, pk=pk, user=request.user)
    memberships = ApplicationMembership.objects.filter(application=application).select_related('membership')
    context = {'application': application, 'memberships': memberships}
    return render(request, 'applications/application_detail.html', context)

@login_required
def create_application(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, is_active=True)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.total_price = membership.price
            application.save()
            ApplicationMembership.objects.create(
                application=application,
                membership=membership,
            )
            return redirect('application_detail', pk=application.pk)
    else:
        initial = {'client_name': request.user.get_full_name() or request.user.username}
        form = ApplicationForm(initial=initial)
    context = {'form': form, 'membership': membership}
    return render(request, 'applications/create_application.html', context)

def stock_list(request):
    stocks = Stock.objects.filter(is_active=True)
    context = {'stocks': stocks}
    return render(request, 'stocks/stock_list.html', context)

def review_list(request):
    reviews = Review.objects.filter(is_published=True)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            if request.user.is_authenticated:
                review.user = request.user
            review.save()
            return redirect('review_list')
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['author_name'] = request.user.get_full_name() or request.user.username
        form = ReviewForm(initial=initial)
    context = {'reviews': reviews, 'form': form}
    return render(request, 'reviews/review_list.html', context)

@login_required
def visit_list(request):
    visits = Visit.objects.select_related('direction', 'trainer').all()
    context = {'visits': visits}
    return render(request, 'visits/visit_list.html', context)

def schedule_type_list(request):
    schedule_items = ScheduleType.objects.select_related('trainer', 'direction').all()
    context = {'schedule_items': schedule_items}
    return render(request, 'schedule/schedule_type_list.html', context)

def about(request):
    return render(request, 'about.html')

def contacts(request):
    return render(request, 'components/contacts.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})

class UserLoginView(LoginView):
    authentication_form = LoginForm
    template_name = 'registration/login.html'
