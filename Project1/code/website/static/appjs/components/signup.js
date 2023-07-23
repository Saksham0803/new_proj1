const Signup = Vue.component('Signup', {
    template: `
    <div>
      <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: #D14D72; padding: 5px;">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">Showtime</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
              <li class="nav-item">
                <a class="nav-link" href="#">Login</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <div>
        <h3>Register</h3>
        <form @submit.prevent="submitForm">
          <div>
            <label>Name</label>
            <input type="text" v-model="name" required minlength="3">
          </div>
          <div>
            <label>Email address</label>
            <input type="email" v-model="email" required>
          </div>
          <div>
            <label>Password</label>
            <input type="password" v-model="password1" required minlength="6">
          </div>
          <div>
            <label>Confirm password</label>
            <input type="password" v-model="password2" required minlength="6">
          </div>
          <p>Already registered? <a href="/login">Login</a> </p>
          <button type="submit">Register</button>
        </form>
      </div>
    </div>
    `,
    data: function() {
      return {
        name: '',
        email: '',
        password1: '',
        password2: '',
      };
    },
    methods: {
      submitForm: function() {
        if (this.password1 !== this.password2) {
          alert("Passwords don't match");
        } else if (this.name.length < 3) {
          alert('Name must contain greater than 4 Characters');
        } else {
          axios.post('/sign_up', {
            name: this.name,
            email: this.email,
            password: this.password1,
          })
          .then(function (response) {
            if (response.data.success) {
              window.location.href = '/home';
            } else {
              alert(response.data.message);
            }
          })
          .catch(function (error) {
            console.error(error);
          });
        }
      },
    },
  });
  