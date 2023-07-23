const AddShow = Vue.component('AddShow', {
    template: `
      <div>
        <form @submit.prevent="addShow">
          <div class="mb-3">
            <label class="form-label">Movie</label>
            <select class="form-select" v-model="newShow.movie">
              <option v-for="movie in movies" :value="movie">{{ movie }}</option>
            </select>
          </div>
          <!-- More form fields... -->
          <button type="submit" class="btn btn-primary">Add Show</button>
        </form>
      </div>
    `,
    data() {
      return {
        movies: [],
        theaters: [],
        newShow: {
          movie: '',
          // Other fields...
        },
      };
    },
    methods: {
      addShow() {
        axios.post('/api/add_show', this.newShow)
          .then(() => {
            this.newShow = {
              movie: '',
              // Other fields...
            };
          })
          .catch(error => {
            console.error(error);
          });
      },
      fetchMoviesAndTheaters() {
        axios.get('/api/movies_and_theaters')
          .then(response => {
            this.movies = response.data.movies;
            this.theaters = response.data.theaters;
          })
          .catch(error => {
            console.error(error);
          });
      },
    },
    mounted() {
      this.fetchMoviesAndTheaters();
    },
  });

  