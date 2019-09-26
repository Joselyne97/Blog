import markdown2
from flask import render_template,request,redirect,url_for,abort, flash
from . import main
from .forms import BlogForm, CommentForm, UpdateProfile
from .. import db, photos
from ..models import Blog, User,Comment
from flask_login import login_required, current_user



# Views
@main.route('/', methods = ['GET','POST'])
def index():

    '''
    View root page function that returns the index page and its data
    '''

    blog= Blog.query.filter_by().first()

    title = 'Home - Welcome to our Blogging-app Website Online'

    life = Blog.query.filter_by(category = "life")
    music = Blog.query.filter_by(category = "music")
    emotion = Blog.query.filter_by(category = "emotion")
    inspiration = Blog.query.filter_by(category = "inspiration")
    
    # upvotes = Upvote.get_all_upvotes(blog_id=Blog.id)


    return render_template('category.html', title = title, blog = blog, life = life, music = music, emotion = emotion, inspiration = inspiration)

@main.route('/blogs/new/', methods = ['GET', 'POST'])
@login_required
def new_blog():
    form = BlogForm()

    if form.validate_on_submit():
       description = form.description.data
       title = form.title.data
       user_id = current_user
       category = form.category.data
       print(current_user._get_current_object().id)
       new_blog = Blog(user_id = current_user._get_current_object().id, title = title, description=description, category=category)
       db.session.add(new_blog)
       db.session.commit()
       return redirect(url_for('main.index'))
    return render_template('blog.html',form=form)

@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    blog=Blog.query.get(blog_id)
    if form.validate_on_submit():
        description = form.description.data

        new_comment = Comment(description = description, user_id = current_user._get_current_object().id, pitch_id = pitch_id)
        db.session.add(new_comment)
        db.session.commit()


        return redirect(url_for('.new_comment', blog_id= blog_id))

    all_comments = Comment.query.filter_by(blog_id = blog_id).all()
    return render_template('comment.html', form = form, comment = all_comments, blog = blog )


@main.route('/user/<uname>')
@login_required
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    get_blogs = Blog.query.filter_by(user_id = current_user.id).all()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user, description = get_blogs)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)



# @main.route('/blog/upvote/<int:blog_id>/upvote', methods = ['GET', 'POST'])
# @login_required
# def upvote(blog_id):
#     blog = Blog.query.get(blog_id)
#     user = current_user
#     blog_upvotes = Upvote.query.filter_by(blog_id= blog_id)
    
#     if Upvote.query.filter(Upvote.user_id==user.id,Upvote.blog_id==blog_id).first():
#         return  redirect(url_for('main.index'))


#     new_upvote = Upvote(blog_id=blog_id, user = current_user)
#     new_upvote.save_upvotes()
#     return redirect(url_for('main.index'))



# @main.route('/blog/downvote/<int:blog_id>/downvote', methods = ['GET', 'POST'])
# @login_required
# def downvote(blog_id):
#     blog = Blog.query.get(blog_id)
#     user = current_user
#     blog_downvotes = Downvote.query.filter_by(blog_id= blog_id)
    
#     if Downvote.query.filter(Downvote.user_id==user.id,Downvote.blog_id==blog_id).first():
#         return  redirect(url_for('main.index'))


#     new_downvote = Downvote(blog_id=blog_id, user = current_user)
#     new_downvote.save_downvotes()
#     return redirect(url_for('main.index'))




    
