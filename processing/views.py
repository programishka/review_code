from django.urls import reverse_lazy
from django.views.generic import FormView
from processing.forms import TransferMoneyForm


class MoneyTransferView(FormView):
    template_name = 'index.html'
    form_class = TransferMoneyForm
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
