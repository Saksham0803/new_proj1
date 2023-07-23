const BookTickets = Vue.component('BookTickets', {
    data: function() {
        return {
            show: {
                movie: '',
                theater: '',
                cost_per_seat: '',
                seats_available: ''
            },
            no_of_seats: '',
            messages: {}
        }
    },
    methods: {
        bookTicket: function() {
            axios.post('/book_ticket/' + this.show.id, {
                no_of_seats: this.no_of_seats
            })
            .then(response => {
                this.messages.success = 'Your ticket is being booked';
                this.no_of_seats = '';
            })
            .catch(error => {
                this.messages.error = 'Please fill all the fields';
            });
        },
        alertClass: function(category) {
            return `alert-${category}`;
        },
        dismissMessage: function(category) {
            delete this.messages[category];
        }
    },
    template: `
        <div>
            <form @submit.prevent="bookTicket">
                <!-- Form fields similar to the HTML code -->
            </form>
            <div v-for="(message, category) in messages" :key="category" 
                :class="['alert', 'alert-dismissible', 'fade', 'show', alertClass(category)]" role="alert">
                {{ message }}
                <button type="button" class="btn-close" @click="dismissMessage(category)"></button>
            </div>
        </div>
    `
});
