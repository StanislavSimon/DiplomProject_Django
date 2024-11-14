from django.shortcuts import render, redirect, get_object_or_404
from photogramm.forms import PhotoForm, CommentForm, PhotoUploadForm, RegistrationForm, LoginForm
from photos.models import Photo
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def photo_list(request):
    photos = Photo.objects.all()
    comment_form = CommentForm()

    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        photo = get_object_or_404(Photo, id=photo_id)

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.photo = photo
            comment.save()
            return redirect('photo_list')

    return render(request, 'photo_list.html', {
        'photos': photos,
        'comment_form': comment_form,
    })


def upload_photo(request):
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('photo_list')
    else:
        form = PhotoUploadForm()
    return render(request, 'upload_photo.html', {'form': form})


def delete_photo(request, photo_id):
    photo = get_object_or_404(Photo, id=photo_id)

    if request.method == 'POST':

        if photo.image:
            image_path = os.path.join(settings.MEDIA_ROOT, photo.image.name)
            if os.path.isfile(image_path):
                os.remove(image_path)

        photo.delete()
        return redirect('photo_list')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('photo_list')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('photo_list')
            else:
                if form.errors.get('age'):
                    return redirect('underage')
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
