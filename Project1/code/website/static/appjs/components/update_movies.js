const UpdateMovies = Vue.component('UpdateMovies', {
    data() {
        return {
            movie: {},
            messages: [],
        };
    },
    created() {
        this.fetchMovie();
    },
    methods: {
        fetchMovie() {
            axios.get(`/api/movies/${this.$route.params.id}`)
                .then(response => {
                    this.movie = response.data.movie;
                    this.messages = response.data.messages;
                });
        },
        updateMovie() {
            let formData = new FormData();
            formData.append('title', this.movie.title);
            formData.append('Genre', this.movie.Genre);
            formData.append('rating', this.movie.rating);
            formData.append('poster', this.movie.poster);

            axios.post(`/api/update_movies/${this.movie.id}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                this.messages.push(response.data.message);
            });
        }
    },
    template: `
        <div>
            <navbar-component :user="user" @logout="logout"></navbar-component>
            <alert-component :messages="messages"></alert-component>
            
            <div class="container">
                <form @submit.prevent="updateMovie">
                    <div>
                        <label>Title</label>
                        <input v-model="movie.title" required>
                    </div>
                    <div>
                        <label>Genre</label>
                        <input v-model="movie.Genre" required>
                    </div>
                    <div>
                        <label>Rating (out of 5)</label>
                        <input v-model="movie.rating" min="0" max="5" step="0.01" required>
                    </div>
                    <div>
                        <label>Poster</label>
                        <input type="file" @change="onFileChange">
                    </div>
                    <button type="submit">Update</button>
                </form>
            </div>
        </div>
    `,
    components: {
        'navbar-component': NavbarComponent,
        'alert-component': AlertComponent
    }
});
