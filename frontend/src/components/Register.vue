<template>
  <div class="flex h-screen w-full flex-col md:flex-row bg-background-light dark:bg-background-dark font-display text-neutral-900 dark:text-gray-100 antialiased overflow-hidden">
    <!-- Left Side: Visual/Branding Panel -->
    <div class="relative hidden md:flex md:w-1/2 lg:w-3/5 h-full overflow-hidden">
      <div class="absolute inset-0 bg-neutral-900/40 z-10"></div>
      <img alt="Traditional fabric details" class="absolute inset-0 w-full h-full object-cover object-center" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDFi63XszliZA7vXU_AEpBjTNg13TJx7LOL3uqIp43xwoo6dpTbprX4Dcoiotbqi_KQwOXwFeBmEElUcWWzp8T7gmvVEY2fnm7AEam4owVuCksSWtAmiDJOqg-94QPOcU8sD5fDIBFVR1JC0wu_UOVxa_0X_vzD_7qTbBRn96ESPtigei2minfQzPXRNQLl8fJMHIn3XoFKHPZ7HufUAiiDEQ7lwA2S41kH05zDdVtMIGA7uMmlC3_0885opiHYLljvK3uwo950xqr"/>
      <div class="relative z-20 flex flex-col justify-between h-full p-12 lg:p-20">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-primary flex items-center justify-center rounded-lg">
            <span class="material-icons text-background-dark">diamond</span>
          </div>
          <span class="text-2xl font-bold tracking-tight text-white uppercase">Al-Turath</span>
        </div>
        <div class="max-w-md">
          <h1 class="text-5xl lg:text-7xl font-extrabold text-white leading-tight mb-6">
            Join the <span class="text-primary italic">Heritage.</span>
          </h1>
          <p class="text-lg text-gray-200 font-light leading-relaxed">
            Create your account to start designing your custom traditional garments with the finest materials.
          </p>
        </div>
        <div class="flex items-center gap-6 text-sm text-gray-300">
          <div class="flex items-center gap-2">
            <span class="material-icons text-primary text-sm">assignment_ind</span>
            <span>Personal Profile</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="material-icons text-primary text-sm">history</span>
            <span>Order Archive</span>
          </div>
        </div>
      </div>
    </div>
    <!-- Right Side: Form Panel -->
    <div class="w-full md:w-1/2 lg:w-2/5 h-full flex flex-col justify-center items-center p-8 lg:p-16 bg-background-light dark:bg-background-dark overflow-y-auto">
      <div class="md:hidden flex items-center gap-3 mb-12">
        <div class="w-8 h-8 bg-primary flex items-center justify-center rounded-lg">
          <span class="material-icons text-background-dark text-lg">diamond</span>
        </div>
        <span class="text-xl font-bold tracking-tight text-neutral-900 dark:text-white uppercase">Al-Turath</span>
      </div>
      <div class="w-full max-w-md">
        <div class="mb-10 text-center">
          <h2 class="text-3xl font-bold text-neutral-900 dark:text-white mb-2">Create Account</h2>
          <p class="text-sand-muted">Start your journey with Al-Turath</p>
        </div>
        <div class="flex p-1 bg-neutral-gold/20 dark:bg-neutral-gold/40 rounded-xl mb-8">
          <button @click="$emit('switch', 'login')" class="flex-1 py-2.5 text-sm font-semibold rounded-lg text-sand-muted hover:text-white">
            Login
          </button>
          <button class="flex-1 py-2.5 text-sm font-semibold rounded-lg bg-primary text-background-dark shadow-sm">
            Register
          </button>
        </div>
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div class="space-y-1">
            <label class="text-sm font-medium text-sand-muted ml-1" for="name">Full Name</label>
            <div class="relative">
              <span class="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-sand-muted text-lg">person_outline</span>
              <input v-model="full_name" class="w-full pl-12 pr-4 py-3 bg-white dark:bg-neutral-gold/10 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-neutral-900 dark:text-white transition-all" id="name" placeholder="John Doe" type="text" required/>
            </div>
          </div>
          <div class="space-y-1">
            <label class="text-sm font-medium text-sand-muted ml-1" for="email">Email Address</label>
            <div class="relative">
              <span class="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-sand-muted text-lg">mail_outline</span>
              <input v-model="email" class="w-full pl-12 pr-4 py-3 bg-white dark:bg-neutral-gold/10 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-neutral-900 dark:text-white transition-all" id="email" placeholder="name@example.com" type="email" required/>
            </div>
          </div>
          <div class="space-y-1">
            <label class="text-sm font-medium text-sand-muted ml-1" for="password">Password</label>
            <div class="relative">
              <span class="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-sand-muted text-lg">lock_open</span>
              <input v-model="password" class="w-full pl-12 pr-4 py-3 bg-white dark:bg-neutral-gold/10 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-neutral-900 dark:text-white transition-all" id="password" placeholder="••••••••" type="password" required/>
            </div>
          </div>
          <button :disabled="loading" class="w-full py-4 bg-primary hover:bg-primary/90 text-background-dark font-bold rounded-xl shadow-lg shadow-primary/10 transition-all flex items-center justify-center gap-2 mt-4" type="submit">
            <span v-if="loading">Creating Account...</span>
            <span v-else>Register Now</span>
          </button>
          <p v-if="error" class="text-red-500 text-sm text-center font-medium mt-2">{{ error }}</p>
          <p v-if="success" class="text-green-500 text-sm text-center font-medium mt-2">Registration successful! Please log in.</p>
        </form>
        <p class="mt-8 text-center text-sm text-sand-muted">
          Already have an account? 
          <a @click.prevent="$emit('switch', 'login')" class="font-bold text-primary hover:underline underline-offset-4 ml-1 cursor-pointer" href="#">Sign In</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      full_name: '',
      email: '',
      password: '',
      loading: false,
      error: null,
      success: false
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true;
      this.error = null;
      this.success = false;
      try {
        const response = await fetch('http://localhost:5000/api/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            full_name: this.full_name,
            email: this.email,
            password: this.password,
            role: 'customer'
          })
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Registration failed');
        }

        this.success = true;
        setTimeout(() => {
          this.$emit('switch', 'login');
        }, 2000);
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
