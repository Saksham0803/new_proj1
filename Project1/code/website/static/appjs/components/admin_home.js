const AdminHome = Vue.component('AdminHome', {
    template: `
    <div>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <!-- your navigation here -->
      </nav>
      <div class="banner">
        <img src="../static/banner.png" alt="banner">
      </div>
      <div class="cards-list">
        <div v-if="movies.length > 0" v-for="movie in movies" :key="movie.id" class="card">
          <div class="card_image">
            <a :href="'/select_theaters/' + movie.id" class="card_image">
              <img :src="'/static/movie_posters/' + movie.poster">
            </a>
          </div>
          <a :href="'/select_theaters/' + movie.id" class="link-dark">
            <div class="card_title" style="padding-bottom:10px">
              <p>{{ movie.title }}</p>
            </div>
            <div class="card_title">
              rating - {{ movie.rating }}
            </div>
            <div class="card_title">
              Genre - {{ movie.Genre }}
            </div>
          </a>
        </div>
        <h2 v-else>No Movies Yet</h2>
      </div>
    </div>
    `,
    data: function() {
      return {
        movies: [],
      };
    },
    methods: {
      fetchMovies: function() {
        axios.get('/api/movies')
          .then(response => {
            this.movies = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      },
    },
    created: function() {
      this.fetchMovies();
    },
  });
  