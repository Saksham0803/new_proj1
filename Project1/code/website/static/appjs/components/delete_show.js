const DeleteShows = Vue.component('DeleteShows', {
    data() {
        return {
            shows: [],
            messages: [],
        };
    },
    created() {
        this.fetchShows();
    },
    methods: {
        fetchShows() {
            axios.get('/api/shows')
                .then(response => {
                    this.shows = response.data.shows;
                    this.messages = response.data.messages;
                });
        },
        deleteShow(showId) {
            axios.delete(`/api/delete_shows/${showId}`)
                .then(response => {
                    this.shows = this.shows.filter(show => show.id !== showId);
                    this.messages.push(response.data.message);
                });
        }
    },
    template: `
        <div>
            <navbar-component :shows="shows"></navbar-component>
            <alert-component :messages="messages"></alert-component>
            
            <div class="container">
                <shows-component :shows="shows" @delete-show="deleteShow"></shows-component>
            </div>
        </div>
    `,
    components: {
        'navbar-component': NavbarComponent,
        'alert-component': AlertComponent,
        'shows-component': ShowsComponent
    }
});
