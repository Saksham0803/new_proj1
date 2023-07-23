const UpdateTheater = Vue.component('UpdateTheater', {
    data() {
        return {
            theater: {
                id: this.$route.params.id,
                name: '',
                address: ''
            }
        }
    },
    methods: {
        updateTheater() {
            axios.put('/api/update_theatre/' + this.theater.id, this.theater)
                .then(response => {
                    this.$router.push('/my_theaters');
                })
                .catch(error => {
                    console.log(error);
                });
        }
    },
    mounted() {
        axios.get('/api/theatre/' + this.theater.id)
            .then(response => {
                this.theater = response.data.theater;
            })
            .catch(error => {
                console.log(error);
            });
    },
    template: `
    <div>
        <!-- Your navigation code here -->
        <h3 style="display: flex; justify-content: center;align-items: center;padding-top:5%; font-weight:700">Update Theater</h3>
        <div class="form" style="display: flex; justify-content: center;align-items: center;padding-top:10px;padding-bottom:70px">
            <form @submit.prevent="updateTheater">
                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input type="Text" class="form-control" placeholder="Name of your theater" v-model="theater.name">
                </div>
                <div class="mb-3">
                    <label class="form-label">Address</label>
                    <input type="Text" class="form-control" placeholder="Enter exact address" v-model="theater.address">
                </div>
                <button type="submit" class="btn btn-primary ">Submit</button>
            </form>
        </div>
    </div>
    `
});