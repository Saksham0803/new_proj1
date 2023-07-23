const SelectTheater = Vue.component('SelectTheater', {
    template: `
    <div>
      <!-- your navigation here -->
      <div class="container">
        <div class="col">
          <h1 style="padding-top: 2%;">
            <div class="fw-bold">{{ movie.title }}</div> In Theatres
          </h1>
          <hr/>
          <p><strong>Book your show</strong></p>
          <div class="container pt-4 pb-4">
            <div class="row row-cols-auto">
              <div v-for="show in shows" :key="show.id" class="card">
                <div class="card-body">
                  <h5 class="card-title1">
                    <div>
                      <a v-if="user.is_authenticated && !user.is_admin" :href="'/book_ticket/' + show.id" class="link-dark">{{ show.t }}</a>
                      <div v-else class="fw-bold">{{ show.t }}</div>
                    </div>
                  </h5>
                  <p class="card-text">{{ show.address_t }}</p>
                  <p class="card-text">{{ show.datetime }}</p>
                  <hr/>
                  Cost <div class="fw-bold">{{ show.cost }} Rs</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    `,
    data: function() {
      return {
        user: null,
        shows: [],
        movie: null,
      };
    },
    methods: {
      fetchUser: function() {
        axios.get('/api/user')
          .then(response => {
            this.user = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      },
      fetchShows: function() {
        axios.get('/api/shows/' + this.$route.params.id)
          .then(response => {
            this.shows = response.data.shows;
            this.movie = response.data.movie;
          })
          .catch(error => {
            console.error(error);
          });
      },
    },
    created: function() {
      this.fetchUser();
      this.fetchShows();
    },
  });
  