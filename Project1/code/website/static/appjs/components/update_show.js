const UpdateShow = Vue.component('UpdateShow', {
    template: `
    <div>
        <!-- Your navigation code here -->
        <h3 style="display: flex; justify-content: center;align-items: center;padding-top:5%; font-weight:700">Update Show</h3>
        <div class="form" style="display: flex; justify-content: center;align-items: center;padding-top:10px;padding-bottom:70px">
        <form @submit.prevent="updateShow">
            <div class="mb-3">
                <label class="form-label">{{ show.movie }}</label>
                <select class="form-select" aria-label="Select Theater" v-model="show.movie">
                    <option v-for="movie in movies" :key="movie.title" :value="movie.title">{{ movie.title }}</option>
                </select>
            </div>
            <!-- Your other form fields here -->
            <button type="submit" class="btn btn-primary">Update Show</button>
        </form>
        </div>
    </div>
    `,
    data() {
        return {
            show: {},
            movies: [],
            theaters: [],
            messages: [],
        };
    },
    methods: {
        updateShow() {
            axios.put(`/api/update_show/${this.show.id}`, this.show)
                .then(response => {
                    // handle success
                    this.messages.push('Show updated successfully');
                })
                .catch(error => {
                    // handle error
                    this.messages.push('Failed to update show');
                });
        },
    },
    created() {
        this.fetchShowData();
    },
    methods: {
        fetchShowData() {
            // Fetch movies
            axios.get('/api/movies')
                .then(response => {
                    this.movies = response.data;
                });
            // Fetch theaters
            axios.get('/api/theaters')
                .then(response => {
                    this.theaters = response.data;
                });
            // Fetch show details
            axios.get(`/api/show/${this.show.id}`)
                .then(response => {
                    this.show = response.data;
                });
        },
    },
});
