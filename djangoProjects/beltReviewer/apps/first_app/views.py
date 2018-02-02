# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import Users
from .models import Books
from .models import Authors
from .models import Reviews
from django.core.urlresolvers import reverse
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
	if request.session.get('user_id')== None:
		request.session['user_id']=""
	if request.session.get('first_name')== None:
		request.session['first_name']=""
	if request.session.get('last_name')== None:
		request.session['last_name']=""
	if request.session.get('email_address')== None:
		request.session['email_address']=""
	if request.session.get('status')== None:
		request.session['status']=""
	return render(request, 'first_app/index.html')

def goback(request):
	request.session['first_name']=""
	request.session['last_name']=""
	request.session['email_address']=""
	request.session['status']=""
	request.session['user_id']=""
	request.session.clear()
	return redirect('/')



def login(request):
	errors = {}
	user = Users.objects.filter(email_address=request.POST['email_address']).first()

	if user:
		pw= str(request.POST['password'])
		request.session['status']="NotNew"
		if not bcrypt.checkpw(pw.encode(), user.password.encode()):
			errors['password'] = "Password does not match!"
	else:
		errors['email_address'] = "Email not registered!"
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		request.session['user_id']=user.id
		request.session['first_name']=user.first_name
		request.session['last_name']=user.last_name
		return redirect('/books')


def register(request):
	request.session['first_name']=request.POST['first_name']
	request.session['last_name']=request.POST['last_name']
	request.session['email_address']=request.POST['email_address']
	request.session['status']=""

	errors = Users.objects.basic_validator(request.POST)
	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('/')
	else:
		pw= str(request.POST['password'])
		hashed_pw = bcrypt.hashpw(pw, bcrypt.gensalt())
		Users.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email_address=request.POST['email_address'], password=hashed_pw)
		request.session['user_id']=Users.objects.last().id
		request.session['status']="New"
		return redirect('/books')


###################################33

def result(request):
	books = Books.objects.filter()
	book_reviews_top = []
	book_reviews_rest=[]
	count = 1
	for x in books:
		if count<=3:
			book_reviews_top.append({
				"book":x,
				"reviews": Reviews.objects.filter(book_reviewed=x)
			})
		else:
			book_reviews_rest.append({
				"book":x,
				"reviews": Reviews.objects.filter(book_reviewed=x)
			})
		count=count+1

	context = {
		"topReviews":book_reviews_top,
		"rest":book_reviews_rest
	}

	return render(request, 'first_app/result.html', context)

def add(request):
	return render(request, 'first_app/add.html', {"authors":Authors.objects.all()})

def addBook(request):
	errors = {}

	if (str(request.POST['newAuthor']) == "") and (str(request.POST['author']) == "" or len(str(request.POST['author'])) < 5 ):
		errors['newAuthor'] = "You must either select an Author or Create a New one 5 char long!"
	if request.POST['rating'] =="":
		errors['rating'] = "Rating must be selected!"
	if len(str(request.POST['book'])) < 5:
		errors['book'] = "Must insert title 5 char long at least!"
	if len(str(request.POST['review'])) < 15:
		errors['review'] = "Must insert review 15 char long at least!"

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
		return redirect('books/add')
	else:
		Books.objects.create(title=str(request.POST['book']), uploaded_by=Users.objects.get(id=str(request.session['user_id'])))
		book_id = int(Books.objects.last().id)

		if request.POST['newAuthor']!="":
			Authors.objects.create(name=request.POST['newAuthor'])
			author_id = Authors.objects.last().id
			Authors.objects.get(id=author_id).books_published.add(Books.objects.last())
		else:
			author_id = Authors.objects.filter(name=request.POST['author']).first().id
			Authors.objects.get(id=author_id).books_published.add(Books.objects.get(id=book_id))

		Reviews.objects.create(review=request.POST['review'], rating=request.POST['rating'], reviewed_by=Users.objects.get(id=int(request.session['user_id'])), book_reviewed=Books.objects.get(id=book_id))

		return redirect('books/'+str(book_id))

def bookReviews(request, number):

	book = Books.objects.get(id=number)
	book.book_authors.first()
	temp = []
	count=0
	reviews = book.book_reviews.all()
	reviewers = []
	for i in reviews:
		reviewers.append(reviewers.append(Reviews.objects.get(id=i.id).reviewed_by))
		#count=count+1
	 	#if count <=3:
	 		#temp.append(reviews[i])
	#print reviewers
	#print Books.objects.Books.objects.get(id=number).Reviews.objects.all().Users.objects.all()
	#book.book_reviews.all().order_by("-")
	test=Reviews.objects.filter(book_reviewed=book).all()

	context = {
		"book_id":book.id, 
		'book_title': book.title,
		"book_author": book.book_authors.first().name,
		"reviews": Reviews.objects.filter(book_reviewed=book)
		}
	return render(request, 'first_app/review.html', context)

def destroyComment(request):
	Reviews.objects.get(id=str(request.POST['review_id'])).delete()
	return redirect('/books/'+str(request.POST['book_id']))

def addReview(request):
	#validations
	errors = {}
	if len(str(request.POST['review'])) < 15:
		errors['password'] = "Review must be at least 15 char long!"
	if request.POST['rating'] =="":
		errors['password'] = "Rating must be selected!"

	if len(errors):
		for tag, error in errors.iteritems():
			messages.error(request, error, extra_tags=tag)
	else:
		Reviews.objects.create(review=request.POST['review'], rating=request.POST['rating'], reviewed_by=Users.objects.get(id=int(request.session['user_id'])), book_reviewed=Books.objects.get(id=request.POST['book_id']))
		
	return redirect('/books/'+str(request.POST['book_id'])) 


def user(request, number):
	user = Users.objects.get(id=number)
	unique_ids = user.reviews_by.all().values("book_reviewed").distinct()
	unique_books = []
	for book in unique_ids:
		unique_books.append(Books.objects.get(id=book['book_reviewed']))

	context = {
		"user":Users.objects.get(id=str(number)), 
		"reviews_count":str(len(Reviews.objects.filter(reviewed_by=Users.objects.get(id=str(number))))),
		"books":unique_books
		}

	return render(request, 'first_app/user.html', context)