import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'our_notes.settings')

import django
django.setup()
from notes.models import Comment, Note, Url, User, Category, StudyGroup, rates_comments, rates_notes

import random as r
import csv
from faker import Faker

from django.contrib.auth.hashers import make_password, check_password

DATA_FOLDER = os.path.join('theme', 'static')
fake = Faker()

def getPath(file):
    return os.path.join(DATA_FOLDER, file)

def readFile(file):
    try:
        data = []
        with open(getPath(file), 'r') as f:
            line = f.readline()
            while line != '':
                data.append(line.strip())
                line = f.readline()

        return data
    except:
        print("\nERROR: Impossible retrieve "+file+"!\n")

def getRandomElement(list):
    index = r.randint(0,len(list)-1)
    return list[index], index

def getParagraph(min, max):
    paragraphs = fake.paragraphs(nb=r.randint(min,max))

    text = ""
    for p in paragraphs:
        text = text+p+"\n"

    return text

def add_user( username, email):
    user = User.objects.get_or_create(username=username)[0]
    user.email = email
    user.set_password(fake.password(length=12))
    user.save()
    return user

def add_category(name):
    category = Category.objects.get_or_create(categoryName=name)[0]
    category.save()
    return category

def add_studyGroup(cat, name, admin, members):
    group = StudyGroup.objects.get_or_create(category=cat, groupName=name, admin=admin)[0]
    group.description = getParagraph(0,6)
    group.rules = getParagraph(0,3)
    
    for member in members:
        group.members.add(member)

    group.save()
    return group

def add_url(group, urls):
    link, index = getRandomElement(urls)

    url = Url.objects.get_or_create(studyGroup=group)[0]
    url.label = link[0]
    url.link = link[1]
    url.save()
    return url

def add_note(group, creator, name):
    note = Note.objects.get_or_create(studyGroup=group, user=creator, noteName=name)[0]
    note.description = getParagraph(0,6)
    note.save()
    return note

def add_rateNotes(note, user):
    rateNote = rates_notes.objects.get_or_create(note=note, user=user, rating = r.randint(0,1))[0]
    rateNote.save()
    return rateNote

def add_comment(note, user, replyTo=None):
    comment = Comment.objects.get_or_create(note=note, user=user)[0]
    
    comment.text = getParagraph(1,3)

    if(replyTo!=None):
        comment.replyTo = replyTo

    comment.save()
    return comment

def reply(note, user, replyTo, maxReplies):
    for i in range(r.randint(0, maxReplies)):
        if(r.randint(0,1)==1):
            replyTo = add_comment(note, user, replyTo)
            reply(note, user, replyTo, int(maxReplies/2))
    
    return replyTo

def add_rateComment(comment, user):
    rateComment = rates_comments.objects.get_or_create(comment=comment, user=user, rating = r.randint(0,1))[0]
    rateComment.save()
    return rateComment

def populate(nUsers, maxGroups, maxNotes):

    categories = readFile('categories.txt')
    
    urls=[('Discord','https://discord.com/'), ('Zoom','https://www.teamspeak.com/en/'), ('TeamSpeak','https://zoom.us/'), ('GoogleMeet','https://meet.google.com/')]

    usernames = [fake.unique.first_name() for i in range(nUsers)]
    emails = [fake.unique.email() for i in range(nUsers)]
    
    groupNames = [fake.unique.company() for i in range(maxGroups*len(categories))]

    noteNames = [fake.unique.file_name() for i in range(maxNotes*len(groupNames))]

    maxUsers = int(nUsers/3)

    users = []
    groups = []

    print("\nAdding users...")
    # Add users
    for i in range(nUsers):
        users.append(add_user(usernames[i], emails[i]))

    print("Adding categories...")
    # Add categories, study groups and urls
    count = 0 
    for category in categories:
        
        print("\tAdding groups to category: "+ category +" ...")
        # Add category
        category_key = add_category(category)
        
        for x in range(r.randint(0,maxGroups)):

            # Generate admin and members
            admin, index = getRandomElement(users)

            members = []
            for y in range(r.randint(1, maxUsers)):
                member, i = getRandomElement(users)
                if(i!=index):
                    members.append(member)

            # Add study group
            group = add_studyGroup(category_key, groupNames[count], admin, members)
            groups.append(group)
            count += 1

            # Add url
            add_url(group, urls)

    #Add notes 
    count = 0
    for group in groups:

        print("Adding notes to group: "+ group.groupName +" ...")
        for x in range(r.randint(0,maxNotes)):
            
            creator, index = getRandomElement(users)

            # Add note
            note = add_note(group, creator, noteNames[count])
            count += 1

            # Rate, comment note
            for i in range(maxUsers):
                # Rating note
                user, index = getRandomElement(users)
                add_rateNotes(note, user)
                
                # Adding a comment
                comment = add_comment(note, user)
                
                # Rating the comment
                add_rateComment(comment, user)
                #reply(note, user, comment, 10)
            

if __name__ == '__main__':
    print('Populating database...')
    populate(20,3,4)