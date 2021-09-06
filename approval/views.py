from django.shortcuts import render, redirect

from django.views.generic import CreateView, ListView, UpdateView, DetailView, TemplateView, FormView, DeleteView, View

from approval.models import ApprovalRequest, ApprovalOne, ApprovalTwo, Rejected, Identity, Department, Report
from django.http import JsonResponse

from django.urls import reverse

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

# Create your views here.
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = "dashboard.html"


# Create your views here.
@method_decorator(login_required, name='dispatch')
class RequestCreateView(CreateView):
    model = ApprovalRequest
    template_name = "request.html"
    fields = [
        'sgid',
        'name',
        'department',
        'department_which',
        'imporove',
        'before_image',
        'after_image',
    ]
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current"] = 'request'
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Please check for input errors.')
        return super().form_invalid(form)

    def form_valid(self, form):
        item = form.save()
        item.user= self.request.user
        item.save()
        ApprovalOne.objects.create(
            app_request = item,
        )
        res = reverse('request_create')
        messages.success(self.request, 'Request submitted, Please wait for approval.')
        return HttpResponseRedirect(res)
    
@method_decorator(login_required, name='dispatch')
class ApprovalOneListView(ListView):
    model = ApprovalOne
    template_name = "approval1_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current"] = 'app1'
        return context

    def get_queryset(self):
        return ApprovalOne.objects.filter(status=False)

    
@method_decorator(login_required, name='dispatch')
class RequestDetailView(DetailView):
    model = ApprovalRequest
    template_name = "request-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
    

@method_decorator(login_required, name='dispatch')
class ApprovalTwoListView(ListView):
    model = ApprovalTwo
    template_name = "approval1_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current"] = 'app2'
        return context
    
    def get_queryset(self):
        return ApprovalTwo.objects.filter(status=False)
    


class RequestListView(ListView):
    model = ApprovalRequest
    template_name = "request-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["current"] = 'requests'
        return context
    
class PopulateSGID(View):
    def get(self, request, *args, **kwargs ):
        Identity.objects.all().delete()
        for i in range(5):
            Identity.objects.create(
                name="SG ID"+str(i)
            )

        return JsonResponse({
            'status': True
        })

class PopulateIDW(View):
    def get(self, request, *args, **kwargs ):
        Department.objects.all().delete()
        for i in range(5):
            Department.objects.create(
                name="W Choice "+str(i)
            )

        return JsonResponse({
            'status': True
        })

def approval_one(request, *args, **kwargs ):
    pk = kwargs.get('pk')

    if pk:
        try:
            approval = ApprovalOne.objects.get(app_request__pk=pk)
            approval.status = True
            approval.user=request.user

            approval.save()

            ApprovalTwo.objects.create(
                app_request=approval.app_request,
            )
            messages.success(request, "Successfully approved !")
        except:
            return redirect('request_list_a1')
    else:
        messages.error("Request Does Not Exist !")
    return redirect('request_list')


def approval_two(request, *args, **kwargs ):
    pk = kwargs.get('pk')

    if pk:
        try:
            approval = ApprovalTwo.objects.get(app_request__pk=pk)
            approval.status = True
            approval.user=request.user
            
            approval.save()
            
            messages.success(request, "Successfully approved !")
        except:
            return redirect('request_list_a1')
    else:
        messages.error("Request Does Not Exist !")
    return redirect('request_list')

from reportlab.rl_config import defaultPageSize

PAGE_WIDTH  = defaultPageSize[0]
PAGE_HEIGHT = defaultPageSize[1]

def respond_pdf_from_object(app_request):
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    f_approval_time =  app_request.first_approval.udpated.strftime('%Y-%m-%d %H:%M')
    s_approval_time =  app_request.second_approval.udpated.strftime('%Y-%m-%d %H:%M')


    p.drawString(50, PAGE_HEIGHT-50, f'SGID: {app_request.sgid.name}')
    p.drawString(50, PAGE_HEIGHT-65, f'Name: {app_request.name}')
    p.drawString(50, PAGE_HEIGHT-80, f'Department: {app_request.department}')
    p.drawString(50, PAGE_HEIGHT-95, f'Dept in which: {app_request.department_which.name}')
    p.drawString(50, PAGE_HEIGHT-110, f'Improve Constant: {app_request.imporove}')
    p.drawString(50, PAGE_HEIGHT-125, f'First Approval: {f_approval_time}')
    p.drawString(50, PAGE_HEIGHT-140, f'Second Approval: {s_approval_time}')
    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')

def generate_pdf(request, *args, **kwargs ):
    pk = kwargs.get('pk')

    if pk:
        try:
            approval = ApprovalTwo.objects.get(app_request__pk=pk)
            if approval.status == True:
                return respond_pdf_from_object(approval.app_request)
            else:
                messages.error(request, "Approval Pending !")
                return redirect('request_detail', pk=pk)  
            
            messages.success(request, "Successfully approved !")
        except Exception as e:
            print(e)
            return redirect('request_detail', pk=pk)  
    else:
        messages.error("Request Does Not Exist !")
    return redirect('request_detail', pk=pk)  