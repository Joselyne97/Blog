from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SubmitField,TextAreaField
from wtforms.validators import Required,Email
from wtforms import ValidationError

class BlogForm(FlaskForm):
    title = StringField('Title',validators=[Required()])
    description = TextAreaField("What do you have for us today?",validators=[Required()])
    # category = RadioField('Label', choices=[ ('pickup','pickup'), ('interview','interview'),('promotion','promotion'),('product','product')],validators=[Required()])
    submit = SubmitField('Post your blog')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField('Comment')

class UpdateBlogForm(FlaskForm):
    title=StringField('Title', validators=[Required()])
    description = TextAreaField('edit your blog',validators = [Required()])
    submit = SubmitField('Update')


# class UpvoteForm(FlaskForm):
# 	submit = SubmitField()


# class Downvote(FlaskForm):
# 	submit = SubmitField()

