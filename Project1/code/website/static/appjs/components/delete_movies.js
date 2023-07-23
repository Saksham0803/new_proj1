const DeleteMovies = Vue.component('DeleteMovies', {
    data() {
        return {
            movies: [],
            messages: [],
        };
    },
    created() {
        this.fetchMovies();
    },
    methods: {
        fetchMovies() {
            axios.get('/api/movies')
                .then(response => {
                    this.movies = response.data.movies;
                    this.messages = response.data.messages;
                });
        },
        deleteMovie(movieId) {
            axios.delete(`/api/delete_movies/${movieId}`)
                .then(response => {
                    this.movies = this.movies.filter(movie => movie.id !== movieId);
                    this.messages.push(response.data.message);
                });
        }
    },
    template: `
        <div>
            <navbar-component :movies="movies"></navbar-component>
            <alert-component :messages="messages"></alert-component>
            
            <div class="container">
                <movies-component :movies="movies" @delete-movie="deleteMovie"></movies-component>
            </div>
        </div>
    `,
    components: {
        'navbar-component': NavbarComponent,
        'alert-component': AlertComponent,
        'movies-component': MoviesComponent
    }
});
