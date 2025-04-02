from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import LandDocument,Staff
from .forms import LandDocumentForm
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
def staff_dashboard(request):
    documents = LandDocument.objects.all()
    return render(request, 'views/staff_dashboard.html', {'documents': documents})

@login_required
def document_list(request):
    documents = LandDocument.objects.all()
    return render(request, 'views/document_list.html', {'documents' : documents} )

# @login_required
# def approve_document(request, document_id):
#     document = get_object_or_404(LandDocument, id=document_id)
#     if request.method == 'POST':
#         document.is_approved = True
#         document.approved_by = request.user.staff
#         document.save()
#         return redirect('staff_dashboard')
#     return render(request, 'staff/approve_document.html', {'document': document})



@login_required
@require_POST
def approve_document(request, document_id):
    document = get_object_or_404(LandDocument, id=document_id)
    
    try:
        staff = request.user.staff
    except Staff.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': "Staff profile not found. Please contact an administrator."
        })
    
    if staff.is_approving_officer:
        document.is_approved = True
        document.approved_by = staff
        document.save()
        return JsonResponse({
            'success': True,
            'message': f"Document '{document.title}' has been approved.",
            'approved_by': str(staff)
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "You don't have permission to approve documents."
        })

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = LandDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.submitted_by = request.user
            document.save()
            return redirect('staff_dashboard')
    else:
        form = LandDocumentForm()
    return render(request, 'views/upload_document.html', {'upload_form': form})

# In staff/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm

def staff_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('staff_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/staff_login.html', {'staff_form': form})