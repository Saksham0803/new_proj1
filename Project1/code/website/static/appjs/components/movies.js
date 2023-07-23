const Movies = Vue.component('Movies', {
    template: `
      <div class="movies">
        <h5 class="fw-bold">Movies</h5>
        <a href="/add_movies" class="btn btn-outline-dark btn-sm">Add Movies</a>
        <div class="cards-list" v-if="movies.length > 0">
          <div class="card" v-for="movie in movies" :key="movie.id">
            <div class="card_image">
              <a :href="'/select_theaters/' + movie.id" class="card_image">
                <img :src="'/static/movie_posters/' + movie.poster" />
              </a>
            </div>
            <div class="card_title">
              <p>{{ movie.title }}</p>
            </div>
            <div class="card_title">
              <a :href="'/update_movies/' + movie.id" class="card-link">Update</a>,
              <a :href="'/delete_movies/' + movie.id" class="card-link">Delete</a>
            </div>
          </div>
        </div>
        <h2 v-else>No Movies Yet</h2>
      </div>
    `,
    data() {
      return {
        movies: [] // Assume this data comes from an API or some other data source
      };
    },
    methods: {
      fetchMovies() {
        // Fetch the movies data from an API and assign it to the movies data property
        // This is just a placeholder, replace with your actual API call
        axios.get('/api/movies')
          .then(response => {
            this.movies = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      },
      deleteMovie(movieId) {
        // Delete a movie by its ID
        // This is just a placeholder, replace with your actual API call
        axios.delete(`/api/movies/${movieId}`)
          .then(() => {
            // Remove the movie from the movies array
            this.movies = this.movies.filter(movie => movie.id !== movieId);
          })
          .catch(error => {
            console.error(error);
          });
      }
    },
    mounted() {
      this.fetchMovies();
    }
  });
  