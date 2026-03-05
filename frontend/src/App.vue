<template>
  <div id="app">
    <Login v-if="view === 'login'" @switch="view = $event" @login-success="handleLoginSuccess" />
    <Register v-else-if="view === 'register'" @switch="view = $event" />
    <div v-else-if="view === 'dashboard'" class="p-10 text-center">
      <h1 class="text-3xl font-bold mb-4">Welcome to Al-Turath Dashboard</h1>
      <p class="mb-6">Hello, {{ user.full_name }}!</p>
      <button @click="logout" class="px-6 py-2 bg-primary text-background-dark font-bold rounded-lg">Logout</button>
    </div>
  </div>
</template>

<script>
import Login from './components/Login.vue'
import Register from './components/Register.vue'

export default {
  name: 'App',
  components: {
    Login,
    Register
  },
  data() {
    return {
      view: 'login',
      user: JSON.parse(localStorage.getItem('user')) || null
    }
  },
  created() {
    if (this.user) {
      this.view = 'dashboard';
    }
  },
  methods: {
    handleLoginSuccess(data) {
      this.user = data.user;
      this.view = 'dashboard';
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      this.user = null;
      this.view = 'login';
    }
  }
}
</script>

<style>
/* Add Material Icons font if not already available */
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&display=swap');

:root {
  --primary: #eebd2b;
  --background-light: #f8f7f6;
  --background-dark: #221d10;
  --neutral-gold: #3d3624;
  --sand-muted: #a69d85;
}

body {
  margin: 0;
  padding: 0;
}
</style>
