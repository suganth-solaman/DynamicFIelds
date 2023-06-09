# inbuilt module
from django.shortcuts import render
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response

# user defined module
from .models import Details, DynamicField, Forms


def create_employee(request):
    context = {}
    if request.method == "POST":
        post_data = dict(request.POST)

        if 'form' in post_data:
            form_name = post_data['form'][0]
            Forms.objects.create(form=form_name)
        elif 'id' in post_data:
            id_form = int(post_data['id'][0])
            form_data = Forms.objects.filter(id=id_form)
            form_model = DynamicField.objects.filter(details__id=id_form)
            context["form_data"] = form_data
            if form_model.exists():
                field_detail = []
                for key, value in form_model[0].fields.items():
                    lable = f"<lable>{value[0]}</lable>"
                    if value[1] == "Check":
                        box = f"<input type='checkbox' style='width:25%' id={value[0]} name={value[0]} >"
                    elif value[1] == "input":
                        box = f'<input type="text" id={value[0]} name={value[0]} placeholder="enter">'
                    else:
                        box = f'<textarea  id={value[0]} name={value[0]} ></textarea>'
                    field_detail.append(lable)
                    field_detail.append(box)
                context["field"] = field_detail
        elif 'available' in post_data:
            post_data.pop("csrfmiddlewaretoken")
            post_data.pop("available")
            name = post_data['name']
            code = post_data['code']
            form = post_data['forms']
            post_data.pop('name')
            post_data.pop('code')
            dynamic_data = {}
            for key, value in post_data.items():
                dynamic_data[key] = value[0]
            get_form = Forms.objects.get(id=int(form[0]))
            modify, built = Details.objects.get_or_create(details=get_form)
            modify.name = name[0]
            modify.worker_id = code[0]
            modify.additional = dynamic_data
            modify.save()
    data = Forms.objects.all()
    context["data"] = data
    return render(request, 'create_emp.html', context)


def dynamic(request):
    context = {}
    if request.method == "POST":
        field = dict(request.POST)
        get_form = Forms.objects.get(id=int(field['form'][0]))
        field.pop("csrfmiddlewaretoken")
        field.pop("form")
        DynamicField.objects.get_or_create(details=get_form, fields=field)
    data = Forms.objects.all()
    context['data'] = data
    return render(request, 'dynamic.html', context)


def view(request, pk):
    context = {}
    data = Details.objects.filter(details__id=pk)
    if data.exists():
        context['data'] = data
    return render(request, 'view.html', context)


def update(request, pk):
    context = {}
    data = Details.objects.filter(id=pk)
    return_id = data[0].details.id
    form_model = DynamicField.objects.filter(details__id=data[0].details.id)
    additional = data[0].additional
    field = form_model[0].fields
    if form_model.exists():
        field_detail = []
        for key in field:
            lable = f"<lable>{field[key][0]}</lable>"
            if field[key][1] == "Check":
                box = f"<input type='checkbox' style='width:25%' id={field[key][0]} name={field[key][0]} value={additional[field[key][0]]} >"
            elif field[key][1] == "input":
                box = f'<input type="text" id={field[key][0]} name={field[key][0]} placeholder="enter" value={additional[field[key][0]]}>'
            else:
                box = f'<textarea  id={field[key][0]} name={field[key][0]} value={additional[field[key][0]]} ></textarea>'
            field_detail.append(lable)
            field_detail.append(box)
        context["field"] = field_detail
        context["name"] = data[0].name
        context["worker_id"] = data[0].worker_id
    if request.method == "POST":
        data = dict(request.POST)
        name = data.pop('name')
        work_id = data.pop('code')
        data.pop('csrfmiddlewaretoken')
        data.pop('available')
        data['forms'] = [additional['forms']]
        data = {x: y[0] for x, y in data.items()}
        if "vaccinated" not in data:
            data['vaccinated'] = "True"
        uptodate = Details.objects.get(id=pk)
        uptodate.name = name[0]
        uptodate.worker_id = work_id[0]
        uptodate.additional = data
        uptodate.save()
        return redirect('view', return_id)
    return render(request, 'update.html', context)
