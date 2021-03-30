from os import name
from django.db.models import Q, Count
from django.contrib.auth.models import Group, User
from django.shortcuts import render,redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from notes.models import Comment, Note, Profile, StudyGroup, Category, Url, rates_comments, rates_notes
from notes.forms import CommentForm, NoteForm, UrlForm, UserForm, ProfileForm, GroupForm

# Create your views here.

class Search(View):
    def get(self, request):
        context_dict = {}
        context_dict['categories'] = None
        groups = {}
        
        # Apply filters 
        queryCategory = self.request.GET.get('queryCategory')
        queryGroup = self.request.GET.get('queryGroup')
        joined = self.request.GET.get('joined')
            
        if(queryCategory):
            category_list = Category.objects.filter(Q(categoryName__icontains=queryCategory.strip())).order_by('categoryName')
        else:   
            category_list = Category.objects.order_by('categoryName')

        # Check if the query returned the categories
        if(category_list.exists()):
            
            categories = []

            # Get groups for each category
            for category in category_list:

                print(joined)
                if(queryGroup):
                    group = StudyGroup.objects.filter(Q(groupName__icontains=queryGroup.strip()), category=category)
                else:  
                    group = StudyGroup.objects.filter(category=category)

                if(joined):
                    group = group.filter(members=request.user)
                
                if(group or (queryGroup==None and joined==None)):
                    categories.append(category)
                    groups[category.categoryName] = group

            context_dict['groups'] = groups
            context_dict['categories'] = categories

        return render(request, 'search.html', context=context_dict)

class Faq(View):
    def get(self, request):
        return render(request, 'faq.html', context={})

class Register(View):
    
    def get(self, request):
        context_dict = {}
        context_dict['registered'] = False
        context_dict['user_form'] = UserForm()
        context_dict['profile_form'] = ProfileForm()

        # Render the template 
        return render(request, 'register.html', context=context_dict)

    def post(self, request):
        context_dict = {}
        context_dict['error'] = None
        context_dict['registered'] = False
        user_form = UserForm()
        profile_form = ProfileForm()


        # REGISTRATION 
        if request.POST.get('submit') == 'Register':

            user_form = UserForm(request.POST)
            profile_form = ProfileForm(request.POST, request.FILES)

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
                if 'profilePic' in request.FILES:
                    profile.profileImg = request.FILES['profilePic']

                # Registration was successful.
                profile.save()
                
                context_dict['registered'] = True
                login(request, user)

        # LOGIN
        elif request.POST.get('submit') == 'Sign-in':
            # Get credentials
            username = request.POST.get('username')
            password = request.POST.get('password')

            # See if the username/password combination is valid
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('notes:search'))
                else:
                    # An inactive account was used - no logging in!
                    return HttpResponse("Your account is disabled.")
            else:
                # Invalid login details provided
                context_dict['Sign_in_errors'] = "Invalid username or password, or both"

        context_dict['user_form'] = user_form
        context_dict['profile_form'] = profile_form

        return render(request, 'register.html', context=context_dict)

class Logout(View):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        return redirect(reverse('notes:search'))
    
class Account(View):
    def get_user_details(self, username):
        user = User.objects.get(username=username)
        #user_form = UserForm({'username':user.username,'email':user.email})
        user_profile = Profile.objects.get_or_create(user=user)[0]
        form = ProfileForm({'profileImg': user_profile.profileImg})
        
        return (user, user_profile, form)

    @method_decorator(login_required)
    def get(self, request, username):
        context_dict = {}
        context_dict['user_account'] = None
        
        if(request.user.username == username):
                (user, user_profile, form) = self.get_user_details(username)
                context_dict['groups'] = StudyGroup.objects.filter(members = user)
                context_dict['user_account'] = user
                #context_dict['user_form'] = user_form
                context_dict['user_profile'] = user_profile
                context_dict['form'] = form

        return render(request, 'account.html', context=context_dict)

    @method_decorator(login_required)
    def post(self, request, username):
        context_dict = {}

        if(request.user.username == username):
            (user, user_profile, form) = self.get_user_details(username)

        form = ProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('notes:account', user.username)
        else:
            context_dict['user_profile'] = user_profile
            context_dict['user_account'] = user
            context_dict['form'] = form
        
        return render(request, 'rango/profile.html', context_dict)
    
class Show_group(View):
    def get(self, request, studyGroup_slug):
        context_dict = {}
        context_dict['comment_form'] = CommentForm()

        rating = self.request.GET.get('rating')
        queryNote = self.request.GET.get('queryNote')

        try:
            # Get studyGroup related to this slug, if any
            studyGroup = StudyGroup.objects.get(slug=studyGroup_slug)
            context_dict['group'] = studyGroup

            # Get urls
            context_dict['urls'] = Url.objects.filter(studyGroup=studyGroup)

            # Get notes
            if(queryNote):
                notes = Note.objects.filter(Q(noteName__icontains=queryNote.strip()), studyGroup=studyGroup)
            else:
                notes = Note.objects.filter(studyGroup=studyGroup)

            if(rating):
                notes = notes.annotate(upVotes=Count('rates', filter=Q(rates_notes__rating=1))).order_by("upVotes").reverse()

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
            # if there are no associated groups the template will display the "no category" message.
            context_dict['group'] = None

        return render(request, 'show_group/show_group.html', context=context_dict)

    @method_decorator(login_required)
    def post(self, request, studyGroup_slug):
        comment_form = CommentForm(request.POST)

        username = request.POST['username']
        note_id = request.POST['note_id']

        print("Username: "+username)

        if(comment_form.is_valid()):

            user = User.objects.get(username = username)
            note = Note.objects.get(id = note_id)

            comment = comment_form.save(commit=False)
            comment.user = user
            comment.note = note
            comment.save()
            
        return redirect(reverse('notes:show_group', kwargs={'studyGroup_slug':studyGroup_slug}))

class Create_group(View):
    @method_decorator(login_required)
    def get(self, request, username):
        group_form = GroupForm()
        return render(request, 'create_group.html', context={'form': group_form})
    
    @method_decorator(login_required)
    def post(self, request, username):
        # Get category
        cat_id = request.POST.get("category")
        category =  Category.objects.get(id = int(cat_id))

        post = request.POST.copy()
        post["category"] = category

        group_form = GroupForm(post, instance=category)

        if(group_form.is_valid()):

            # group = group_form.save(commit=False)
            # group.admin = User.objects.get(username=username)
            # group.save()  

            name = post["groupName"]
            
            # check if the group name has been already used
            try:
                StudyGroup.objects.get(groupName = name)
                error = "A group with the same name already exists."
                return render(request, 'create_group.html', context={'form': group_form, 'errors': error})
            
            # If the name is valid, create a new group
            except:
                user = User.objects.get(username=username)
                group = StudyGroup.objects.create(groupName = name, category = category, admin = user)
                group.description = post["description"]
                group.rules = post["rules"]
                group.save()
            
            return redirect(reverse('notes:show_group', kwargs={'studyGroup_slug':group.slug}))

class Remove_group(View):
    @method_decorator(login_required)
    def get(self, request):

        #if(request.user.username == )
        group_slug = request.GET['group_slug']
        group = StudyGroup.objects.get(slug=group_slug)

        if(request.user == group.admin):
            group.delete()
        else:
            group.members.remove(request.user)

        return HttpResponse()

class Join_group(View):
    @method_decorator(login_required)
    def get(self, request):

        group_slug = request.GET['group_slug']
        group = StudyGroup.objects.get(slug=group_slug)
        group.members.add(request.user)

        return HttpResponse()

class Upload_note(View):
    @method_decorator(login_required)
    def get(self, request, group_slug):
        note_form = NoteForm()
        return render(request, 'upload_note.html', context={'note_form': note_form, 'group_slug':group_slug})
    
    @method_decorator(login_required)
    def post(self, request, group_slug):
        try:
            user = request.user
            group = StudyGroup.objects.get(slug=group_slug)
            note_form = NoteForm(request.POST, request.FILES)

            
            if(note_form.is_valid()):

                note = note_form.save(commit=False)
                note.user = user
                note.studyGroup = group
                note.file = request.FILES['file']

                note.save()
                
                return redirect(reverse('notes:show_group', kwargs={'studyGroup_slug':group.slug}))

            return render(request, 'upload_note.html', context={'note_form': note_form, 'group_slug':group_slug})

        except Exception:
            return HttpResponse(-1)

class Download_note(View):
    def get(self,response, id):

        note = Note.objects.get(id = id)

        try:
            filename = note.file.name.split('/')[-1]
            response = HttpResponse(note.file, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
            return response
        except:
            group = StudyGroup.objects.get(id=note.studyGroup.id)
            return redirect(reverse('notes:show_group', kwargs={'studyGroup_slug':group.slug}))

class Remove_note(View):
    @method_decorator(login_required)
    def get(self, request):

        #if(request.user.username == )
        note_id = request.GET['note_id']
        note = Note.objects.get(id=note_id)

        if(request.user == note.user):
            note.delete()

        return HttpResponse()

class Add_link(View):
    @method_decorator(login_required)
    def get(self, request, group_slug):
        url_form = UrlForm()
        return render(request, 'add_link.html', context={'url_form': url_form, 'group_slug':group_slug})
    
    @method_decorator(login_required)
    def post(self, request, group_slug):

        group = StudyGroup.objects.get(slug=group_slug)
        url_form = UrlForm(request.POST)

        if(url_form.is_valid()):

            url = url_form.save(commit=False)
            url.studyGroup = group
            url.save()
            
            return redirect(reverse('notes:show_group', kwargs={'studyGroup_slug':group.slug}))

        return render(request, 'add_link.html', context={'url_form': url_form, 'group_slug':group_slug})

class Add_comment(View):
    
    @method_decorator(login_required)
    def post(self, request, group_slug):

        comment_form = CommentForm(request.POST)

        username = request.POST['username']
        note_id = request.POST['note_id']

        if(comment_form.is_valid()):

            user = User.objects.get(username = username)
            note = Note.objects.get(id = note_id)

            comment = comment_form.save(commit=False)
            comment.user = user
            comment.note = note
            comment.save()
            
        return redirect(reverse('notes:show_group', kwargs={'studyGroup_slug':group_slug}))

class Vote_comment(View):
    @method_decorator(login_required)
    def get(self, request):
        comment_id = request.GET['id']
        vote = request.GET['vote']
        user = request.user

        comment = Comment.objects.get(id=int(comment_id))
        
        try:
            try:
                rates_comments.objects.filter(comment=comment, user=user).delete()
            except Exception:
                pass

            rates_comments.objects.create(comment=comment, user=user, rating=vote)
            upVotes = rates_comments.objects.filter(comment=comment, rating=1).count()
            downVotes = rates_comments.objects.filter(comment=comment, rating=0).count()
            
            return JsonResponse({'upVotes':upVotes, 'downVotes':downVotes})

        except Exception:
            return HttpResponse(-1)

class Vote_note(View):
    @method_decorator(login_required)
    def get(self, request):
        note_id = request.GET['id']
        vote = request.GET['vote']
        user = request.user

        note = Note.objects.get(id=int(note_id))
        
        try:
            try:
                rates_notes.objects.filter(note=note, user=user).delete()
            except Exception:
                pass

            rates_notes.objects.create(note=note, user=user, rating=vote)
            upVotes = rates_notes.objects.filter(note=note, rating=1).count()
            downVotes = rates_notes.objects.filter(note=note, rating=0).count()
            
            return JsonResponse({'upVotes':upVotes, 'downVotes':downVotes})

        except Exception:
            return HttpResponse(-1)



