from catalog.models import Component, Service
from .forms import ApplicationForm
from .models import (Application, ApplicationComponentItem,
                     ApplicationServiceItem)
import weasyprint
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, ListView, UpdateView, DeleteView)


@method_decorator(login_required, name='dispatch')
class ApplicationListView(ListView):
    """Class representing a list of all applications."""

    model = Application
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        for application in context['object_list']:
            application.can_edit = application.master == self.request.user
        return context


def create_resources(request, application):
    """Function for creating details and services in the application."""
    components_ids = request.POST.getlist('components')
    for component_id in components_ids:
        quantity = int(request.POST.get(
            f'component_quantity_{component_id}', 0)
        )
        if quantity:
            component = Component.objects.get(id=component_id)
            ApplicationComponentItem.objects.create(
                application=application,
                component=component,
                quantity=quantity
            )

    services_ids = request.POST.getlist('services')
    for service_id in services_ids:
        quantity = int(request.POST.get(
            f'service_quantity_{service_id}', 0)
        )
        service = Service.objects.get(id=service_id)
        ApplicationServiceItem.objects.create(
            application=application,
            service=service,
            quantity=quantity
        )


@method_decorator(login_required, name='dispatch')
class ApplicationCreateView(CreateView):
    """Class providing a page for creating an application."""

    model = Application
    form_class = ApplicationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['components'] = Component.objects.all()
        context['services'] = Service.objects.all()
        return context

    def form_valid(self, form):
        application = form.save()
        create_resources(self.request, application)
        return HttpResponseRedirect(reverse('applications:applications_list'))


@method_decorator(login_required, name='dispatch')
class ApplicationEditView(UpdateView):
    """Class providing the application editing page."""

    model = Application
    form_class = ApplicationForm

    def dispatch(self, request, *args, **kwargs):
        application = self.get_object()
        if application.master != request.user:
            return render(request, '404.html', status=404)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['components'] = Component.objects.all()
        context['services'] = Service.objects.all()
        context['selected_components'] = {
            item.component.id: item.quantity
            for item in self.object.component_items.all()
        }
        context['selected_services'] = {
            item.service.id: item.quantity
            for item in self.object.service_items.all()
        }
        return context

    def form_valid(self, form):
        application = form.save()

        ApplicationComponentItem.objects.filter(
            application=application).delete()

        ApplicationServiceItem.objects.filter(
            application=application).delete()

        create_resources(self.request, application)
        return HttpResponseRedirect(reverse('applications:applications_list'))


@method_decorator(login_required, name='dispatch')
class ApplicationDeleteView(DeleteView):
    """Class representing the application deletion page."""

    model = Application


@login_required
def create_application_pdf(request, application_id):
    """Function converting application into PDF page."""
    application = get_object_or_404(Application, pk=application_id)
    context = {
        'application': application,
        'selected_components': ApplicationComponentItem.objects.filter(
            application=application),
        'selected_services': ApplicationServiceItem.objects.filter(
            application=application),
    }
    html = render_to_string('applications/application_pdf.html',
                            context=context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{application.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response
