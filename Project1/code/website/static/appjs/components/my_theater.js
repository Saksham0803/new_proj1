const MyTheaters = Vue.component('MyTheaters', {
    data() {
        return {
            my_theater: {},
            messages: [],
        };
    },
    created() {
        this.fetchData();
    },
    methods: {
        fetchData() {
            axios.get('/api/my_theaters')
                .then(response => {
                    this.my_theater = response.data.my_theater;
                    this.messages = response.data.messages;
                });
        }
    },
    template: `
        <div>
            <navbar-component :my_theater="my_theater"></navbar-component>
            <alert-component :messages="messages"></alert-component>
            
            <div class="container">
                <theaters-component :my_theater="my_theater"></theaters-component>
                <shows-component :my_theater="my_theater"></shows-component>
            </div>
        </div>
    `,
});
