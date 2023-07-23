const AddMovies = Vue.component('AddMovies', {
    template: `
      <div>
        <form @submit.prevent="addMovie">
          <div class="mb-3">
            <label class="form-label">Title</label>
            <input type="text" class="form-control" placeholder="Movie's Title" v-model="newMovie.title">
          </div>
          <div class="mb-3">
            <label class="form-label">Genre</label>
            <input type="text" class="form-control" v-model="newMovie.Genre" required>
          </div>
          <div class="mb-3">
            <label class="form-label">Rating (out of 5)</label>
            <input type="number" class="form-control" v-model="newMovie.rating" min="0" max="5" required>
          </div>
          <button type="submit" class="btn btn-primary">Add Movie</button>
        </form>
      </div>
    `,
    data() {
      return {
        newMovie: {
          title: '',
          Genre: '',
          rating: '',
        },
      };
    },
    methods: {
      addMovie() {
        axios.post('/api/add_movie',localStorage.getItem('access_token'), this.newMovie)
          .then(() => {
            this.newMovie = {
              title: '',
              Genre: '',
              rating: '',
            };
          })
          .catch(error => {
            console.error(error);
          });
      },
    },
  });
  