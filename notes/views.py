from os import name
from django.contrib.auth.models import Group, User
from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from notes.models import Comment, Note, StudyGroup, Category, Url
from notes.forms import UserForm, ProfileForm, GroupForm

# Create your views here.
def search(request):
    context_dict = {}

    category_list = Category.objects.order_by('categoryName')

    groups = {}
    for category in category_list:
        group = StudyGroup.objects.filter(category = category)
        groups[category.categoryName] = group

    context_dict['groups'] = groups
    context_dict['categories'] = category_list

    return render(request, 'search.html', context=context_dict)

def faq(request):
    context_dict = {}
    return render(request, 'faq.html', context=context_dict)

def show_group(request, studyGroup_slug):
    context_dict = {}

    try:
        # Get studyGroup related to this slug, if any
        studyGroup = StudyGroup.objects.get(slug=studyGroup_slug)
        context_dict['group'] = studyGroup

        # Get urls
        context_dict['urls'] = Url.objects.filter(studyGroup=studyGroup)

        # Get notes
        notes = Note.objects.filter(studyGroup=studyGroup)
        context_dict['notes'] = notes

        # Get comments
        comments = {}
        for note in notes:
            comment = Comment.objects.filter(note = note)
            comments[note.noteName] = comment

        context_dict['comments'] = comments

        #Get members        
        context_dict['members'] = studyGroup.members.all().order_by("username")

    except StudyGroup.DoesNotExist:
        # if there are no associated groups
        # the template will display the "no category" message for us.
        context_dict['group'] = None
        context_dict['notes'] = None

    return render(request, 'show_group.html', context=context_dict)

def register(request):
    # True if the registration is successfull
    registered = False

    user_form = UserForm()
    profile_form = ProfileForm()

    if request.method == 'POST':

        # REGISTRATION 
        if request.POST.get('submit') == 'Register':
            user_form = UserForm(request.POST)
            profile_form = ProfileForm(request.POST)

            # Check if the form is valid
            if user_form.is_valid() and profile_form.is_valid():
                # Save the user's form data to the database.
                user = user_form.save()
                
                # Hash the password
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user

                # Check for a profile picture
                if 'picture' in request.FILES:
                    profile.profileImg = request.FILES['picture']

                # Registration was successful.
                profile.save()
                registered = True

                login(request, user)

        # LOGIN
        elif request.POST.get('submit') == 'Sign-in':
            # Get credentials
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.
            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('notes:search'))
                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Your account is disabled.")
            else:
                # Bad login details were provided. So we can't log the user in.
                error = "Invalid username or password, or both"
                return render(request, 'forms/register.html', context={'form': user_form, 'form_profile': profile_form, 'registered': registered, 'Sign_in_errors': error})

    # Render the template depending on the context.
    return render(request, 'forms/register.html', context={'form': user_form, 'form_profile': profile_form,'registered': registered})

@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse('notes:search'))

@login_required
def account(request, username):
    context_dict = {}
    context_dict['user_account'] = None
    
    if(request.user.username == username):
        try:
            user = User.objects.get(username=username)
            context_dict['groups'] = StudyGroup.objects.filter(members = user)
            context_dict['user_account'] = user
                
        except User.DoesNotExist:
            context_dict['groups'] = None

    return render(request, 'account.html', context=context_dict)

@login_required
def create_group(request, username):
    group_form = GroupForm()

    if request.method == 'POST':

        cat_id = request.POST.get("category")
        category =  Category.objects.get(id = cat_id)

        post = request.POST.copy()
        post["category"] = category
        
        group_form = GroupForm(post, instance=category)

        if(group_form.is_valid()):

            # group = group_form.save(commit=False)
            # group.admin = User.objects.get(username=username)
            # group.save()  

            name = post["groupName"]
            
            try:
                StudyGroup.objects.get(groupName = name)
                error = "A group with the same name already exists."
                return render(request, 'forms/create_group.html', context={'form': group_form, 'errors': error})

            except:
                user = User.objects.get(username=username)
                group = StudyGroup.objects.create(groupName = name, category = category, admin = user)
                group.description = post["description"]
                group.rules = post["rules"]
                group.save()
            
            return redirect(reverse('notes:account', kwargs={'username':username}))
        
    return render(request, 'forms/create_group.html', context={'form': group_form})
    



