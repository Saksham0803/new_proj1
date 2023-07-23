const ShowTickets = Vue.component('ShowTickets', {
    data() {
        return {
            user: {}, // replace this with actual user data
            tickets: [],
            show: {},
            ticket_count: 0,
            messages: []  // replace this with actual messages
        };
    },
    created() {
        this.fetchTickets();
    },
    methods: {
        fetchTickets() {
            axios.get('/api/show_tickets/' + this.id)
                .then(response => {
                    this.tickets = response.data.tickets;
                    this.show = response.data.show;
                    this.ticket_count = response.data.ticket_count;
                });
        },
    },
    template: `
        <div>
            <!-- Put your HTML code here -->
            <!-- Remember to replace Flask template syntax with Vue.js template syntax -->
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <!-- ... -->
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        {{ user.is_admin ? user.name + ', Admin' : user.name }}
                    </a>
                    <!-- ... -->
                </li>
                <!-- ... -->
            </nav>
            <div v-for="(category, message) in messages" :key="message" class="alert" :class="'alert-' + category" role="alert">
                {{ message }}
                <!-- ... -->
            </div>
            <div class="container-fluid align-self-center">
                <!-- ... -->
                <div class="card" v-for="ticket in tickets" :key="ticket.id" style="margin-right:24px">
                    <!-- ... -->
                </div>
                <!-- ... -->
            </div>
        </div>
    `
});
