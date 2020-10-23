from django.shortcuts import render
from django.views.generic import FormView
from processing.forms import TransferMoneyForm


class MoneyTransferView(FormView):
    template_name = 'index.html'
    form_class = TransferMoneyForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
