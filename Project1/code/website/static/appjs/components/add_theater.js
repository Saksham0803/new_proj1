const AddTheater = Vue.component('AddTheater', {
    data: function() {
      return {
        newTheater: {
          name: '',
          address: ''
        },
        messages: {}
      }
    },
    methods: {
      addTheater: function() {
        axios.post('/add_theaters', {
          name: this.newTheater.name,
          address: this.newTheater.address
        })
        .then(response => {
          this.messages.success = 'Your Theater is being added';
          this.newTheater.name = '';
          this.newTheater.address = '';
        })
        .catch(error => {
          this.messages.error = 'Fill all the fields';
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
        <form @submit.prevent="addTheater">
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input type="Text" class="form-control" placeholder="Name of your theater" v-model="newTheater.name">
          </div>
          <div class="mb-3">
            <label class="form-label">Address</label>
            <input type="Text" class="form-control" placeholder="Enter exact address" v-model="newTheater.address">
          </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        <div v-for="(message, category) in messages" :key="category" 
           :class="['alert', 'alert-dismissible', 'fade', 'show', alertClass(category)]" role="alert">
          {{ message }}
          <button type="button" class="btn-close" @click="dismissMessage(category)"></button>
        </div>
      </div>
    `
  });
  