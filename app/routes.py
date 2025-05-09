# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import LoginForm, RegistrationForm, RecipeForm, CommentForm, RatingForm
from app.models import User, Recipe, Comment, CommentRating
from app import db
from datetime import datetime
import zoneinfo

main = Blueprint("main", __name__)

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.recipes"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)

@main.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.recipes"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password", "danger")
            return redirect(url_for("main.login"))
        login_user(user)
        return redirect(url_for("main.recipes"))
    return render_template("login.html", form=form)

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/recipes")
@login_required
def recipes():
    recipes = Recipe.query.all()
    return render_template("recipes.html", recipes=recipes)

@main.route("/recipe/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe added successfully!", "success")
        return redirect(url_for("main.recipes"))
    return render_template("recipe_form.html", form=form, legend="New Recipe")

@main.route("/recipe/<int:recipe_id>/edit", methods=["GET", "POST"])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash("You are not authorized to edit this recipe.", "danger")
        return redirect(url_for("main.recipes"))
    form = RecipeForm(obj=recipe)
    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        db.session.commit()
        flash("Recipe updated successfully!", "success")
        return redirect(url_for("main.view_recipe", recipe_id=recipe.id))
    return render_template("recipe_form.html", form=form, legend="Edit Recipe")

@main.route("/recipe/<int:recipe_id>/delete", methods=["POST"])
@login_required
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash("You are not authorized to delete this recipe.", "danger")
        return redirect(url_for("main.recipes"))
    db.session.delete(recipe)
    db.session.commit()
    flash("Recipe deleted!", "success")
    return redirect(url_for("main.recipes"))

@main.route("/recipe/<int:recipe_id>/view")
@login_required
def view_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)

    # convert each comment.created_at to PST
    pst = zoneinfo.ZoneInfo("America/Los_Angeles")
    for c in recipe.comments:
        dt = c.created_at
        if dt.tzinfo is None:
            # assume UTC
            dt = dt.replace(tzinfo=zoneinfo.ZoneInfo("UTC"))
        c.pst_created = dt.astimezone(pst)

    comment_form = CommentForm()
    rating_forms = {c.id: RatingForm(prefix=f"rate-{c.id}") for c in recipe.comments}

    return render_template(
        "view_recipe.html",
        recipe=recipe,
        comment_form=comment_form,
        rating_forms=rating_forms
    )

@main.route("/profile/<int:user_id>")
@login_required
def view_profile(user_id):
    user = User.query.get_or_404(user_id)
    posted_recipes = Recipe.query.filter_by(user_id=user.id).all()

    is_self = (current_user.id == user.id)

    return render_template(
        "view_profile.html",
        user=user,
        recipes=posted_recipes,
        is_self=is_self
    )

@main.route('/recipe/<int:recipe_id>/comment', methods=['POST'])
@login_required
def post_comment(recipe_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data,
            user_id=current_user.id,
            recipe_id=recipe_id,
            parent_id=form.parent_id.data or None
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment posted.', 'success')
    return redirect(url_for('main.view_recipe', recipe_id=recipe_id))

@main.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        flash('Not authorized.', 'danger')
    else:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted.', 'success')
    return redirect(request.referrer)

@main.route('/comment/<int:comment_id>/rate', methods=['POST'])
@login_required
def rate_comment(comment_id):
    prefix = f"rate-{comment_id}"
    form = RatingForm(prefix=prefix)
    if form.validate_on_submit():
        rating = CommentRating.query.filter_by(
            user_id=current_user.id, comment_id=comment_id
        ).first()
        if rating:
            rating.value = form.value.data
        else:
            rating = CommentRating(
                user_id=current_user.id,
                comment_id=comment_id,
                value=form.value.data
            )
            db.session.add(rating)
        db.session.commit()
        flash('Rating saved.', 'success')
    return redirect(request.referrer)
