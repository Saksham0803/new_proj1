const DeleteTheaters = Vue.component('DeleteTheaters', {
    data() {
        return {
            theaters: [],
            messages: [],
        };
    },
    created() {
        this.fetchTheaters();
    },
    methods: {
        fetchTheaters() {
            axios.get('/api/theaters')
                .then(response => {
                    this.theaters = response.data.theaters;
                    this.messages = response.data.messages;
                });
        },
        deleteTheater(theaterId) {
            axios.delete(`/api/delete_theaters/${theaterId}`)
                .then(response => {
                    this.theaters = this.theaters.filter(theater => theater.id !== theaterId);
                    this.messages.push(response.data.message);
                });
        }
    },
    template: `
        <div>
            <navbar-component :theaters="theaters"></navbar-component>
            <alert-component :messages="messages"></alert-component>
            
            <div class="container">
                <theaters-component :theaters="theaters" @delete-theater="deleteTheater"></theaters-component>
            </div>
        </div>
    `,
    components: {
        'navbar-component': NavbarComponent,
        'alert-component': AlertComponent,
        'theaters-component': TheatersComponent
    }
});
