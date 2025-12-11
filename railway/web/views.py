from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Імпортуємо моделі з іншого додатку
from tickets.models import Ticket, Trip, Passenger, Cashier

# --- 1. АВТОРИЗАЦІЯ (Вимога: сторінка реєстрації/логіну) ---
class CustomLoginView(LoginView):
    template_name = 'web/login.html'

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'web/register.html', {'form': form})

# --- 2. ГОЛОВНА ---
def home(request):
    return render(request, 'web/home.html')

# --- 3. СПИСКИ З КАРТИНКАМИ (Вимога: відображення зображення) ---
class PassengerListView(ListView):
    model = Passenger
    template_name = 'web/passenger_list.html'
    context_object_name = 'passengers'

class TripListView(ListView):
    model = Trip
    template_name = 'web/trip_list.html'
    context_object_name = 'trips'

class CashierListView(ListView):
    model = Cashier
    template_name = 'web/cashier_list.html'
    context_object_name = 'cashiers'

# --- 4. CRUD ДЛЯ КВИТКІВ (Вимога: список, деталі, форма додавання, видалення) ---

class TicketsListView(ListView):
    model = Ticket
    template_name = 'web/ticket_list.html'
    context_object_name = 'tickets'

class TicketsDetailView(DetailView):
    model = Ticket
    template_name = 'web/ticket_detail.html'
    context_object_name = 'ticket'

class TicketsCreateView(CreateView):
    model = Ticket
    template_name = 'web/ticket_form.html'
    # Вказуємо поля для форми (поле-зв'язок є: trip, passenger)
    fields = ['trip', 'passenger', 'cashier', 'base_price', 'payment_method']
    success_url = reverse_lazy('tickets_list')

class TicketsUpdateView(UpdateView):
    model = Ticket
    template_name = 'web/ticket_form.html'
    fields = ['trip', 'passenger', 'cashier', 'base_price', 'payment_method']
    success_url = reverse_lazy('tickets_list')

class TicketsDeleteView(DeleteView):
    model = Ticket
    template_name = 'web/ticket_confirm_delete.html'
    success_url = reverse_lazy('tickets_list')