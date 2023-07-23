from flask import render_template, url_for, request, Blueprint,  redirect, current_app, flash
from .models import Show, Movie, Ticket, Theaters, RegisteredUser
import secrets
import os
from datetime import datetime
from . import db
from flask_login import current_user, login_required
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.sqlite3"
# app.config['JWT_SECRET_KEY'] = 'super-secret' 
# db = SQLAlchemy(app)
# jwt = JWTManager(app)

view = Blueprint('views', __name__)


@view.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = RegisteredUser.query.filter_by(username=username).first()

    if user is None or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


@view.route('/sign_up', methods=['POST'])
def sign_up():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    name = request.json.get('name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not name:
        return jsonify({"msg": "Missing name parameter"}), 400
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = RegisteredUser.query.filter_by(email=email).first()

    if user is not None:
        return jsonify({"msg": "User with this email already exists"}), 400

    new_user = RegisteredUser(name=name, email=email, password=generate_password_hash(password))

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True}), 200


@view.route('/')
def home():
    # movie = Movie.query.all()
    # show = Show.query.all()
    # return jsonify({'message': 'This is a protected route'}), 200
    return render_template('base1.html')   #, movie=movie , user=


# @view.route("/search", methods=['POST'])
# def search():
#     try:
#         movie = Movie.query.all()
#         print("done", movie[0].title)
#         searched = request.form.get("searching")
#         print(searched)
#         query = request.form.get("options")
#         print(query)
#         if query == 'Movie Name':
#             movie_t = []
#             for i in range(len(movie)):
#                 movie_t.append(movie[i].title)
#             print(movie_t)
#             moviess = []
#             index = []
#             for j in range(len(movie_t)):
#                 if searched.lower() in movie_t[j].lower():
#                     moviess.append(movie[j])
#                     index.append(j)
#             print(moviess)
#             print(movie)
#             return render_template('home.html', user=current_user, movie=moviess)
#         elif query == 'rating greater than':
#             movie_t = []
#             for i in range(len(movie)):
#                 movie_t.append(movie[i].rating)
#             print(movie_t[0])
#             print(3<4.0)
#             moviess = []
#             index = []
#             for j in range(len(movie_t)):
#                 if float(searched) < float(movie_t[j]):
#                     moviess.append(movie[j])
#                     index.append(j)
#             print(moviess)
#             print(movie)
#             return render_template('home.html', user=current_user, movie=moviess)
#         elif query == 'rating less or equal to':
#             movie_t = []
#             for i in range(len(movie)):
#                 movie_t.append(movie[i].rating)
#             print(movie_t[0])
#             print(3<4.0)
#             moviess = []
#             index = []
#             for j in range(len(movie_t)):
#                 if float(searched) >= float(movie_t[j]):
#                     moviess.append(movie[j])
#                     index.append(j)
#             print(moviess)
#             print(movie)
#             return render_template('home.html', user=current_user, movie=moviess)
#         elif query == 'Genre':
#             movie_t = []
#             for i in range(len(movie)):
#                 movie_t.append(movie[i].Genre)
#             print(movie_t[0])
#             moviess = []
#             index = []
#             for j in range(len(movie_t)):
#                 if searched in (movie_t[j]):
#                     moviess.append(movie[j])
#                     index.append(j)
#             print(moviess)
#             print(movie)
#             return render_template('home.html', user=current_user, movie=moviess)
#         else:
#             print(55)
#             moviee = []
#             return render_template('home.html', user=current_user, movie=moviee)

#     except Exception as e:
#         print("No")
#         movie = Movie.query.all()
#         print(movie)
#         return render_template('home.html', user=current_user, movie=movie)


@view.route('/api/search', methods=['POST'])
@jwt_required()
def search():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from the database

    try:
        movie = Movie.query.all()
        searched = request.get_json().get("searching")
        query = request.get_json().get("options")

        if query == 'Movie Name':
            movie_t = []
            for i in range(len(movie)):
                movie_t.append(movie[i].title)

            moviess = []
            for j in range(len(movie_t)):
                if searched.lower() in movie_t[j].lower():
                    moviess.append(movie[j])

            return jsonify({
                'user': current_user.username,
                'movies': [movie.to_dict() for movie in moviess]
            }), 200

        elif query == 'rating greater than':
            movie_t = []
            for i in range(len(movie)):
                movie_t.append(movie[i].rating)

            moviess = []
            for j in range(len(movie_t)):
                if float(searched) < float(movie_t[j]):
                    moviess.append(movie[j])

            return jsonify({
                'user': current_user.username,
                'movies': [movie.to_dict() for movie in moviess]
            }), 200

        elif query == 'rating less or equal to':
            movie_t = []
            for i in range(len(movie)):
                movie_t.append(movie[i].rating)

            moviess = []
            for j in range(len(movie_t)):
                if float(searched) >= float(movie_t[j]):
                    moviess.append(movie[j])

            return jsonify({
                'user': current_user.username,
                'movies': [movie.to_dict() for movie in moviess]
            }), 200

        elif query == 'Genre':
            movie_t = []
            for i in range(len(movie)):
                movie_t.append(movie[i].Genre)

            moviess = []
            for j in range(len(movie_t)):
                if searched in (movie_t[j]):
                    moviess.append(movie[j])

            return jsonify({
                'user': current_user.username,
                'movies': [movie.to_dict() for movie in moviess]
            }), 200

        else:
            return jsonify({
                'user': current_user.username,
                'movies': []
            }), 200

    except Exception as e:
        movie = Movie.query.all()

        return jsonify({
            'user': current_user.username,
            'movies': [movie.to_dict() for movie in movie]
        }), 200



# @view.route('/search1/<int:id>', methods=['GET', 'POST'])
# def search1(id):
#     try:
#         movie = Movie.query.get(int(id))
#         print("done", movie.title)
#         searched_theater = request.form.get("searching_theater")
#         print(searched_theater)
#         show = Show.query.filter_by(screened_m=int(id)).all()
#         print(show)
#         show_t = []
#         theater = []
#         for i in range(len(show)):
#             print(i)
#             show_t.append(show[i].t_in)
#             theater.append(show[i].t)
#             print(show_t)
#         showss = []
#         for j in range(len(show)):
#             print(j)
#             if searched_theater.lower() in theater[j].lower():
#                 print(theater[j].lower())
#                 showss.append(show[j])
#         print(showss)
#         print(show)
#         return render_template('select_theaters.html',movie=movie, user=current_user, shows=showss)
#     except Exception as e:
#         print("No")
#         movie = Movie.query.get(int(id))
#         show = Show.query.filter_by(screened_m=int(id)).all()
#         print(show)
#         return render_template('select_theaters.html',movie = movie, user=current_user, shows=show)


@view.route('/api/search1/<int:id>', methods=['POST'])
@jwt_required()
def search1(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from the database

    try:
        movie = Movie.query.get(int(id))
        searched_theater = request.get_json().get("searching_theater")

        show = Show.query.filter_by(screened_m=int(id)).all()

        show_t = []
        theater = []
        for i in range(len(show)):
            show_t.append(show[i].t_in)
            theater.append(show[i].t)

        showss = []
        for j in range(len(show)):
            if searched_theater.lower() in theater[j].lower():
                showss.append(show[j])

        return jsonify({
            'movie': movie.title,
            'user': current_user.username,
            'shows': [show.to_dict() for show in showss]
        }), 200

    except Exception as e:
        movie = Movie.query.get(int(id))
        show = Show.query.filter_by(screened_m=int(id)).all()

        return jsonify({
            'movie': movie.title,
            'user': current_user.username,
            'shows': [show.to_dict() for show in show]
        }), 200


# @view.route('/movies')
# @login_required
# def movies():
#     if current_user.is_admin:
#         return render_template('movies.html', user=current_user)
#     return redirect(url_for('views.home'))


@view.route('/api/movies', methods=['GET'])
@jwt_required()
def movies():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from the database

    if current_user.is_admin:
        return jsonify({'message': 'Admin access'}), 200
    else:
        return jsonify({'message': 'Unauthorized access'}), 403



# @view.route('/add_movies', methods=['GET', 'POST'])
# @login_required
# def add_movies():
#     if current_user.is_admin:
#         if request.method == 'POST':
#             title_m = request.form.get('title')
#             no_watched_movie = 0
#             poster_m = save_images(request.files['poster'])
#             rating = request.get_json('rating')
#             genre = request.form.get('Genre')
#             if len(title_m) >= 1:
#                 print("movie in process")
#                 new_movie = Movie(title=title_m, poster=poster_m, times_watched=no_watched_movie, movie_admin_id=current_user.id, rating = rating, Genre = genre)

#                 db.session.add(new_movie)
#                 db.session.commit()
#                 return redirect(url_for('views.movies'))
#             else:
#                 flash('fill all fields', category='error')
#                 return render_template('add_movies.html', user=current_user)
#         else:
#             return render_template('add_movies.html', user=current_user)
#     return redirect(url_for('views.home'))


@view.route('/api/add_movies', methods=['POST'])
@jwt_required()
def add_movies():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        data = request.get_json()

        title_m = data.get('title')
        no_watched_movie = 0
        poster_m = data.get('poster')  # assuming the image is already saved and you are passing the path
        rating = data.get('rating')
        genre = data.get('Genre')

        if title_m and len(title_m) >= 1:
            new_movie = Movie(title=title_m, poster=poster_m, times_watched=no_watched_movie, movie_admin_id=current_user.id, rating=rating, Genre=genre)

            db.session.add(new_movie)
            db.session.commit()
            return jsonify({'message': f'Movie {new_movie.title} is added'}), 200
        else:
            return jsonify({'message': 'Fill all fields'}), 400
    else:
        return jsonify({'message': 'Unauthorized access'}), 403


# @view.route('/update_movies/<int:id>', methods=['POST', 'GET'])
# @login_required
# def update_movies(id):
#     if current_user.is_admin:
#         update_m = Movie.query.get(int(id))
#         if request.method == 'POST':
#             update_m.poster = save_images(request.files['poster'])
#             update_m.title = request.form.get('title')
#             update_m.rating = request.form.get('rating')
#             update_m.Genre = request.form.get('Genre')
#             db.session.commit()
#             return redirect(url_for('views.movies'))
#         else:
#             if update_m:
#                 return render_template('update_movies.html', user=current_user, movie=update_m)
#     else:
#         return redirect(url_for('movies.home'))


@view.route('/api/update_movies/<int:id>', methods=['PUT'])
@jwt_required()
def update_movies(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        update_m = Movie.query.get(int(id))

        if update_m:
            data = request.get_json()

            update_m.poster = data.get('poster')  # assuming the image is already saved and you are passing the path
            update_m.title = data.get('title')
            update_m.rating = data.get('rating')
            update_m.Genre = data.get('Genre')

            db.session.commit()

            return jsonify({'message': f'Movie {update_m.title} is updated'}), 200
        else:
            return jsonify({'message': 'Movie not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized access'}), 403



# @view.route('/delete_movies/<int:id>', methods=['POST', 'GET'])
# @login_required
# def delete_movies(id):
#     if current_user.is_admin:
#         show = Show.query.filter_by(screened_m=int(id)).all()
#         print(show)
#         delete_m = Movie.query.get(int(id))
#         print(delete_m)
#         print(delete_m, " is deleted")
#         db.session.delete(delete_m)
#         for i in range(len(show)):
#             db.session.delete(show[i])
#         print(id)
#         db.session.commit()

#         return redirect(url_for('views.movies'))

#     else:
#         print(2)
#         return redirect(url_for('movies.home'))


@view.route('/api/delete_movies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_movies(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        show = Show.query.filter_by(screened_m=int(id)).all()
        delete_m = Movie.query.get(int(id))

        if delete_m:
            db.session.delete(delete_m)
            for s in show:
                db.session.delete(s)
            db.session.commit()

            return jsonify({'message': f'Movie {delete_m.name} is deleted'}), 200
        else:
            return jsonify({'message': 'Movie not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized access'}), 403



# @view.route('/my_theaters')
# @login_required
# def my_theaters():
#     if current_user.is_admin:
#         movie = Movie.query.all()
#         return render_template('my_theaters.html', user=current_user, movies=movie)
#     return redirect(url_for('views.home'))


@view.route('/api/my_theaters', methods=['GET'])
@jwt_required()
def my_theaters():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        movies = Movie.query.all()
        return jsonify({
            'user': current_user.to_dict(),
            'movies': [movie.to_dict() for movie in movies]
        }), 200
    else:
        return jsonify({'message': 'Unauthorized access'}), 403



# @view.route('/select_theaters/<int:id>')
# def select_theaters(id):

#     show = Show.query.filter_by(screened_m=int(id)).all()
#     print(show)
#     movie = Movie.query.get(int(id))
#     print(movie)
#     print("line 90")
#     if show:
#         return render_template('select_theaters.html', user=current_user, shows=show, movie= movie)
#     else:
#         flash('There is no show for this movie', category='note')
#         return redirect(url_for('views.home'))


@view.route('/api/select_theaters/<int:id>', methods=['GET'])
def select_theaters(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id) if current_user_id else None  # get user from database

    show = Show.query.filter_by(screened_m=int(id)).all()
    movie = Movie.query.get(int(id))

    if show:
        return jsonify({
            'user': current_user.to_dict() if current_user else None,
            'shows': [s.to_dict() for s in show],
            'movie': movie.to_dict() if movie else None
        }), 200
    else:
        return jsonify({'message': 'There is no show for this movie'}), 404



# @view.route('/add_theaters', methods=['GET', 'POST'])
# @login_required
# def add_theaters():
#     if current_user.is_admin:
#         if request.method == 'POST':
#             name_t = request.form.get('name')
#             address_t = request.form.get('address')
#             if len(name_t) >= 1 and len(address_t) >= 1:
#                 new_t = Theaters(name=name_t, address=address_t, theater_admin_id=current_user.id)
#                 db.session.add(new_t)
#                 db.session.commit()
#                 print('theatre added')
#                 flash('Your Theater is being added', category='success')
#                 return redirect(url_for('views.my_theaters'))
#             else:
#                 flash('Fill all the fields', category='error')
#                 return render_template('add_theaters.html', user=current_user)
#         else:
#             return render_template('add_theaters.html', user=current_user)
#     return redirect(url_for('views.home'))


@view.route('/api/add_theaters', methods=['POST'])
@jwt_required()
def add_theaters():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        name_t = request.json.get('name')
        address_t = request.json.get('address')

        if len(name_t) >= 1 and len(address_t) >= 1:
            new_t = Theaters(name=name_t, address=address_t, theater_admin_id=current_user.id)
            db.session.add(new_t)
            db.session.commit()

            return jsonify({'message': 'Your Theater is being added', 'theater': new_t.to_dict()}), 201
        else:
            return jsonify({'message': 'Fill all the fields'}), 400
    else:
        return jsonify({'message': 'Unauthorized access'}), 403



# @view.route('/update_theatre/<int:id>', methods=['POST', 'GET'])
# @login_required
# def update_theatre(id):
#     if current_user.is_admin:
#         update_t = Theaters.query.get(int(id))
#         if request.method == 'POST':
#             update_t.name = request.form.get('name')
#             update_t.address = request.form.get('address')
#             db.session.commit()
#             return redirect(url_for('views.my_theaters'))
#         else:
#             if update_t:
#                 return render_template('update_theatre.html', user=current_user, theater=update_t)
#     else:
#         return redirect(url_for('movies.home'))


@view.route('/api/update_theatre/<int:id>', methods=['PUT'])
@jwt_required()
def update_theatre(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        update_t = Theaters.query.get(int(id))
        
        if update_t is None:
            return jsonify({'message': 'Theater not found'}), 404

        if request.method == 'PUT':
            update_t.name = request.json.get('name')
            update_t.address = request.json.get('address')
            db.session.commit()
            return jsonify({'message': 'Theater updated successfully', 'theater': update_t.to_dict()}), 200
    else:
        return jsonify({'message': 'Unauthorized access'}), 403


# @view.route('/delete_theaters/<int:id>', methods=['POST', 'GET'])
# @login_required
# def delete_theater(id):
#     print('started')
#     if current_user.is_admin:
#         show = Show.query.filter_by(t_in=int(id)).all()
#         print(show)
#         theater = Theaters.query.get(int(id))
#         print(theater)
#         db.session.delete(theater)
#         for i in range(len(show)):
#             db.session.delete(show[i])
#         db.session.commit()

#         return redirect(url_for('views.my_theaters'))

#     else:
#         print(2)
#         return redirect(url_for('movies.home'))


@view.route('/api/delete_theaters/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_theater(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        show = Show.query.filter_by(t_in=int(id)).all()
        theater = Theaters.query.get(int(id))
        
        if theater is None:
            return jsonify({'message': 'Theater not found'}), 404

        db.session.delete(theater)
        for i in range(len(show)):
            db.session.delete(show[i])
        db.session.commit()

        return jsonify({'message': 'Theater deleted successfully'}), 200
    else:
        return jsonify({'message': 'Unauthorized access'}), 403


# @view.route('/my_tickets')
# @login_required
# def my_tickets():
#     return render_template('my_tickets.html', user=current_user)


@view.route('/api/my_tickets', methods=['GET'])
@jwt_required()
def my_tickets():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    tickets = Ticket.query.filter_by(user=current_user.id).all()
    tickets = [ticket.to_dict() for ticket in tickets]  # assuming you have a to_dict method in your Ticket model

    return jsonify({'user': current_user.to_dict(), 'tickets': tickets}), 200


# @view.route('/book_ticket/<int:id>', methods=['GET', 'POST'])
# @login_required
# def book_ticket(id):
#     if current_user.is_admin == False:
#         show = Show.query.get(int(id))
        
#         if request.method == 'POST':
#             t = Theaters.query.filter_by(name=str(show.t)).first()
#             total_seats = request.form.get('no_of_seats')
#             show.available_seats = int(show.available_seats) - int(total_seats)
#             new_ticket = Ticket(booked_show=show.id, booked_m=show.screened_m, booked_t=show.t_in, user=current_user.id, movie=show.movie, t=show.t, address_t=show.address_t, total_seats=total_seats, cost=int(show.cost) * int(total_seats), timinig_s=show.datetime)
            
#             db.session.add(new_ticket)
#             db.session.commit()


#             return redirect(url_for('views.my_tickets'))
#         else:
#             return render_template('book_ticket.html', user=current_user, show=show)
#     else:
#         return redirect(url_for('views.select_theaters'))


@view.route('/api/book_ticket/<int:id>', methods=['POST'])
@jwt_required()
def book_ticket(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database
    show = Show.query.get(int(id))

    if current_user.is_admin == False:
        if request.method == 'POST':
            t = Theaters.query.filter_by(name=str(show.t)).first()
            total_seats = request.json.get('no_of_seats')
            show.available_seats = int(show.available_seats) - int(total_seats)
            new_ticket = Ticket(booked_show=show.id, booked_m=show.screened_m, booked_t=show.t_in, user=current_user.id, movie=show.movie, t=show.t, address_t=show.address_t, total_seats=total_seats, cost=int(show.cost) * int(total_seats), timinig_s=show.datetime)
            
            db.session.add(new_ticket)
            db.session.commit()

            return jsonify({'message': 'Ticket booked successfully', 'ticket': new_ticket}), 201
        else:
            return jsonify({'message': 'GET method not allowed'}), 405
    else:
        return jsonify({'message': 'Unauthorized access'}), 403


# @view.route('/update_show/<int:id>', methods=['GET', 'POST'])
# @login_required
# def update_shows(id):
#     print('reached 116')
#     movie = Movie.query.all()
#     t = Theaters.query.filter_by(theater_admin_id=int(current_user.id)).all()
#     show = Show.query.get(int(id))
#     print(t)
#     if current_user.is_admin:
#         print('reached 120')
#         if request.method == 'POST':
#             print('reached 122')
#             screened_m = Movie.query.filter_by(title=request.form.get('movie')).first().id

#             if screened_m:
#                 t_in = int(request.form.get('t_in'))
#                 print(t_in)
#                 movie = request.form.get('movie')
#                 print(movie)
#                 t = Theaters.query.filter_by(id=request.form.get('t_in')).first()
#                 date_time = datetime.strptime(request.form.get('date_time'), '%Y-%m-%dT%H:%M')
#                 available_seats = int(request.form.get('available_seats'))
#                 print(available_seats)
#                 cost = request.form.get('cost')
#             else:
#                 flash('No movie', category='warning')
#                 return render_template('add_shows.html', user=current_user, movies=movie, theaters=t)
#             print(movie)

#             if t_in >= 1 and available_seats >= 1:
#                 show.screened_m = screened_m
#                 show.t_in = t_in
#                 show.movie = movie
#                 show.t = t.name
#                 show.address_t = t.address
#                 show.datetime = date_time
#                 show.t_admin_id = current_user.id
#                 show.available_seats = available_seats
#                 show.cost = cost
#                 db.session.commit()
#                 flash('Your Show is being updated', category='success')
#                 return redirect(url_for('views.my_theaters'))
#             else:
#                 flash('Fill all the fields', category='error')
#                 return render_template('update_show.html', user=current_user, movies=movie, theaters=t, show=show)
#         else:
#             return render_template('update_show.html', user=current_user, movies=movie, show=show)
#     else:
#         return render_template('home.html', user=current_user, movies=movie, show=show)


@view.route('/api/update_show/<int:id>', methods=['POST'])
@jwt_required()
def update_shows(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database
    show = Show.query.get(int(id))

    if current_user.is_admin:
        if request.method == 'POST':
            screened_m = Movie.query.filter_by(title=request.json.get('movie')).first().id

            if screened_m:
                t_in = int(request.json.get('t_in'))
                movie = request.json.get('movie')
                t = Theaters.query.filter_by(id=request.json.get('t_in')).first()
                date_time = datetime.strptime(request.json.get('date_time'), '%Y-%m-%dT%H:%M')
                available_seats = int(request.json.get('available_seats'))
                cost = request.json.get('cost')
            else:
                return jsonify({'message': 'No movie selected', 'movies': movie, 'theaters': t}), 400

            if t_in >= 1 and available_seats >= 1:
                show.screened_m = screened_m
                show.t_in = t_in
                show.movie = movie
                show.t = t.name
                show.address_t = t.address
                show.datetime = date_time
                show.t_admin_id = current_user.id
                show.available_seats = available_seats
                show.cost = cost
                db.session.commit()
                return jsonify({'message': 'Your Show is being updated', 'show': show}), 200
            else:
                return jsonify({'message': 'Fill all the fields', 'movies': movie, 'theaters': t, 'show': show}), 400
    else:
        return jsonify({'message': 'Unauthorized access'}), 403


# @view.route('/add_shows', methods=['GET', 'POST'])
# @login_required
# def add_shows():
#     print('reached 116')
#     movie = Movie.query.all()
#     t = Theaters.query.filter_by(theater_admin_id=int(current_user.id)).all()
#     print(t)
#     if current_user.is_admin:
#         print('reached 120')
#         if request.method == 'POST':
#             print('reached 122')
#             screened_m = Movie.query.filter_by(title=request.form.get('movie')).first().id

#             if screened_m:
#                 t_in = int(request.form.get('t_in'))
#                 print(t_in)
#                 movie = request.form.get('movie')
#                 print(movie)
#                 t = Theaters.query.filter_by(id=request.form.get('t_in')).first()
#                 date_time = datetime.strptime(request.form.get('date_time'), '%Y-%m-%dT%H:%M')
#                 available_seats = int(request.form.get('available_seats'))
#                 print(available_seats)
#                 cost = request.form.get('cost')
#             else:
#                 flash('No movie', category='warning')
#                 return render_template('add_shows.html', user=current_user, movies=movie, theaters=t)
#             print(movie)

#             if t_in >= 1 and available_seats >= 1:
#                 new_s = Show(screened_m=screened_m, t_in=t_in, movie=movie, t=t.name,address_t=t.address, datetime=date_time, t_admin_id=current_user.id, available_seats=available_seats, cost=cost)
#                 print(new_s)
#                 db.session.add(new_s)
#                 db.session.commit()
#                 flash('Your Show is being added', category='success')
#                 return redirect(url_for('views.my_theaters'))
#             else:
#                 flash('Fill all the fields', category='error')
#                 return render_template('add_shows.html', user=current_user, movies=movie, theaters=t)
#         else:
#             return render_template('add_shows.html', user=current_user, movies=movie)
#     else:
#         return render_template('home.html', user=current_user, movies=movie)


@view.route('/api/add_shows', methods=['POST'])
@jwt_required()
def add_shows():
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        if request.method == 'POST':
            screened_m = Movie.query.filter_by(title=request.json.get('movie')).first().id

            if screened_m:
                t_in = int(request.json.get('t_in'))
                movie = request.json.get('movie')
                t = Theaters.query.filter_by(id=request.json.get('t_in')).first()
                date_time = datetime.strptime(request.json.get('date_time'), '%Y-%m-%dT%H:%M')
                available_seats = int(request.json.get('available_seats'))
                cost = request.json.get('cost')
            else:
                return jsonify({'message': 'No movie', 'movies': movie, 'theaters': t}), 400

            if t_in >= 1 and available_seats >= 1:
                new_s = Show(screened_m=screened_m, t_in=t_in, movie=movie, t=t.name, address_t=t.address, datetime=date_time, t_admin_id=current_user.id, available_seats=available_seats, cost=cost)
                db.session.add(new_s)
                db.session.commit()
                return jsonify({'message': 'Your Show is being added', 'show': new_s}), 201
            else:
                return jsonify({'message': 'Fill all the fields', 'movies': movie, 'theaters': t}), 400
    else:
        return jsonify({'message': 'Unauthorized access'}), 403


# @view.route('/delete_shows/<int:id>', methods=['POST', 'GET'])
# @login_required
# def delete_shows(id):
#     print('started')
#     if current_user.is_admin:
#         show = Show.query.get(int(id))
#         print(show)
#         db.session.delete(show)
#         db.session.commit()

#         return redirect(url_for('views.my_theaters'))

#     else:
#         print(2)
#         return redirect(url_for('movies.home'))


@view.route('/api/delete_shows/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_shows(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        show = Show.query.get(int(id))
        if show:
            db.session.delete(show)
            db.session.commit()
            return jsonify(message='Show deleted successfully'), 200
        else:
            return jsonify(message='Show not found'), 404
    else:
        return jsonify(message='Unauthorized access'), 403



# @view.route('show_tickets/<int:id>')
# @jwt_required()  #@login_required
# def show_tickets(id):
    # if current_user.is_admin:
    #     ti = Ticket.query.filter_by(booked_show=int(id)).all()
    #     show = Show.query.get(int(id))
    #     return render_template('show_tickets.html', user=current_user, tickets=ti, show=show, ticket_count=len(ti))
    # else:
    #     return render_template('home.html', user=current_user, movies=movies)
    from flask import jsonify

# @view.route('api/show_tickets/<int:id>')
# @jwt_required()
# def show_tickets(id):
#     if current_user.is_admin:
#         ti = Ticket.query.filter_by(booked_show=int(id)).all()
#         show = Show.query.get(int(id))
#         return jsonify({
#             'tickets': [t.serialize() for t in ti],
#             'show': show.serialize(),
#             'ticket_count': len(ti)
#         })
#     else:
#         return jsonify({}), 403
        

@view.route('api/show_tickets/<int:id>')
@jwt_required()
def show_tickets(id):
    current_user_id = get_jwt_identity()  # get user id from JWT
    current_user = RegisteredUser.query.get(current_user_id)  # get user from database

    if current_user.is_admin:
        ti = Ticket.query.filter_by(booked_show=int(id)).all()
        show = Show.query.get(int(id))
        return jsonify({
            'tickets': [t.serialize() for t in ti],
            'show': show.serialize(),
            'ticket_count': len(ti)
        })
    else:
        return jsonify({}), 403




def save_images(poster):
    hash_photo = secrets.token_urlsafe(10)
    _, file_extension = os.path.splitext(poster.filename)
    image_name = hash_photo + file_extension
    file_path = os.path.join(current_app.root_path, 'static/movie_posters', image_name)
    poster.save(file_path)
    return image_name

