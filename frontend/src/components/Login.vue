<template>
  <div class="flex h-screen w-full flex-col md:flex-row bg-background-light dark:bg-background-dark font-display text-neutral-900 dark:text-gray-100 antialiased overflow-hidden">
    <!-- Left Side: Visual/Branding Panel -->
    <div class="relative hidden md:flex md:w-1/2 lg:w-3/5 h-full overflow-hidden">
      <div class="absolute inset-0 bg-neutral-900/40 z-10"></div>
      <img alt="Traditional fabric details" class="absolute inset-0 w-full h-full object-cover object-center" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDFi63XszhliZA7vXU_AEpBjTNg13TJx7LOL3uqIp43xwoo6dpTbprX4Dcoiotbqi_KQwOXwFeBmEElUcWWzp8T7gmvVEY2fnm7AEam4owVuCksSWtAmiDJOqg-94QPOcU8sD5fDIBFVR1JC0wu_UOVxa_0X_vzD_7qTbBRn96ESPtigei2minfQzPXRNQLl8fJMHIn3XoFKHPZ7HufUAiiDEQ7lwA2S41kH05zDdVtMIGA7uMmlC3_0885opiHYLljvK3uwo950xqr"/>
      <!-- Branding Overlay -->
      <div class="relative z-20 flex flex-col justify-between h-full p-12 lg:p-20">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-primary flex items-center justify-center rounded-lg">
            <span class="material-icons text-background-dark">diamond</span>
          </div>
          <span class="text-2xl font-bold tracking-tight text-white uppercase">Al-Turath</span>
        </div>
        <div class="max-w-md">
          <h1 class="text-5xl lg:text-7xl font-extrabold text-white leading-tight mb-6">
            The Art of <span class="text-primary italic">Tradition.</span>
          </h1>
          <p class="text-lg text-gray-200 font-light leading-relaxed">
            Experience the elegance of custom-tailored Arabic and Sudanese wear, crafted with generations of expertise.
          </p>
        </div>
        <div class="flex items-center gap-6 text-sm text-gray-300">
          <div class="flex items-center gap-2">
            <span class="material-icons text-primary text-sm">verified</span>
            <span>Authentic Materials</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="material-icons text-primary text-sm">straighten</span>
            <span>Custom Measurements</span>
          </div>
        </div>
      </div>
    </div>
    <!-- Right Side: Form Panel -->
    <div class="w-full md:w-1/2 lg:w-2/5 h-full flex flex-col justify-center items-center p-8 lg:p-16 bg-background-light dark:bg-background-dark overflow-y-auto">
      <!-- Mobile Brand Logo -->
      <div class="md:hidden flex items-center gap-3 mb-12">
        <div class="w-8 h-8 bg-primary flex items-center justify-center rounded-lg">
          <span class="material-icons text-background-dark text-lg">diamond</span>
        </div>
        <span class="text-xl font-bold tracking-tight text-neutral-900 dark:text-white uppercase">Al-Turath</span>
      </div>
      <div class="w-full max-w-md">
        <!-- Header Tabs -->
        <div class="mb-10 text-center">
          <h2 class="text-3xl font-bold text-neutral-900 dark:text-white mb-2">Welcome Back</h2>
          <p class="text-sand-muted">Enter your details to access your wardrobe</p>
        </div>
        <!-- Form Selection (Static for this view) -->
        <div class="flex p-1 bg-neutral-gold/20 dark:bg-neutral-gold/40 rounded-xl mb-8">
          <button class="flex-1 py-2.5 text-sm font-semibold rounded-lg bg-primary text-background-dark shadow-sm">
            Login
          </button>
          <button @click="$emit('switch', 'register')" class="flex-1 py-2.5 text-sm font-semibold rounded-lg text-sand-muted hover:text-white">
            Register
          </button>
        </div>
        <!-- Auth Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div class="space-y-2">
            <label class="text-sm font-medium text-sand-muted ml-1" for="email">Email Address</label>
            <div class="relative">
              <span class="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-sand-muted text-lg">mail_outline</span>
              <input v-model="email" class="w-full pl-12 pr-4 py-3 bg-white dark:bg-neutral-gold/10 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-neutral-900 dark:text-white transition-all placeholder:text-neutral-400" id="email" placeholder="name@example.com" type="email" required/>
            </div>
          </div>
          <div class="space-y-2">
            <div class="flex justify-between items-center ml-1">
              <label class="text-sm font-medium text-sand-muted" for="password">Password</label>
              <a class="text-xs font-medium text-primary hover:underline" href="#">Forgot password?</a>
            </div>
            <div class="relative">
              <span class="material-icons absolute left-4 top-1/2 -translate-y-1/2 text-sand-muted text-lg">lock_open</span>
              <input v-model="password" class="w-full pl-12 pr-4 py-3 bg-white dark:bg-neutral-gold/10 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl focus:ring-2 focus:ring-primary focus:border-transparent outline-none text-neutral-900 dark:text-white transition-all placeholder:text-neutral-400" id="password" placeholder="••••••••" type="password" required/>
            </div>
          </div>
          <div class="flex items-center gap-2 ml-1">
            <input class="w-4 h-4 rounded border-neutral-gold/30 text-primary focus:ring-primary bg-transparent" id="remember" type="checkbox"/>
            <label class="text-sm text-sand-muted" for="remember">Remember me for 30 days</label>
          </div>
          <button :disabled="loading" class="w-full py-4 bg-primary hover:bg-primary/90 text-background-dark font-bold rounded-xl shadow-lg shadow-primary/10 transition-all flex items-center justify-center gap-2" type="submit">
            <span v-if="loading">Signing In...</span>
            <span v-else>Sign In</span>
          </button>
          <p v-if="error" class="text-red-500 text-sm text-center font-medium mt-2">{{ error }}</p>
        </form>
        <!-- Divider -->
        <div class="relative my-10">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-neutral-gold/20 dark:border-neutral-gold/30"></div>
          </div>
          <div class="relative flex justify-center text-xs uppercase">
            <span class="bg-background-light dark:bg-background-dark px-4 text-sand-muted tracking-widest">Or continue with</span>
          </div>
        </div>
        <!-- Social Logins -->
        <div class="grid grid-cols-2 gap-4">
          <button class="flex items-center justify-center gap-3 px-4 py-3 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl hover:bg-neutral-gold/10 transition-colors">
            <img alt="Google" class="w-5 h-5" src="https://lh3.googleusercontent.com/aida-public/AB6AXuCOZ8_GOEC-uiXcN_wf-jMKuC-jiVjqVm2_Czf-0kDdosBITFMYmvfd3fsstYzQQDv569KG3fihSaFR7gxvI3xoBzV_2hXE1Cw45qOq14KL6xTNji17w4bAVFSNeKZli2vdo11cI57V37thOQLTRTyXYKEG_Q_W1N03gWIXKM6YPDY6YdP4mGCMTnG-hnyc7Jr-ACwqtoaiVQjcA8dhDG7dXBx60OHHBxB54V05jLfwyksC1eepJMc_8RrLYFd8PpmXQOFpOZ6y4erx"/>
            <span class="text-sm font-semibold">Google</span>
          </button>
          <button class="flex items-center justify-center gap-3 px-4 py-3 border border-neutral-gold/30 dark:border-neutral-gold/50 rounded-xl hover:bg-neutral-gold/10 transition-colors">
            <img alt="Apple" class="w-5 h-5 dark:invert" src="https://lh3.googleusercontent.com/aida-public/AB6AXuDPA20sVhxZexvikcUggzTxhsRvuKbNUdkSiiyxuOjt4RV-6jE45kKN5kkGlZhSJ8aXZMJ-694qF83YWyUMryCCNw0UPQA_QfCqivK7PmNbUtHfbhfsFaSUGyBNk066Vxg8fxsrABd7LXaszfR8QdDEn6UfE80EmVb0ABaTPprruNIlYYvLowu_xTWy5wPPohVsvFXhHkJzImNUJXOMiF1RTf25NskljE5jqcC4DTFsFCwlrVgujVWoNO4Qgk3Gvjx8K54EZ3JQlKK0"/>
            <span class="text-sm font-semibold">Apple</span>
          </button>
        </div>
        <!-- Footer Link -->
        <p class="mt-10 text-center text-sm text-sand-muted">
          Don't have an account? 
          <a @click.prevent="$emit('switch', 'register')" class="font-bold text-primary hover:underline underline-offset-4 ml-1 cursor-pointer" href="#">Create an account</a>
        </p>
        <!-- Legal -->
        <div class="mt-16 flex justify-center gap-6 text-[10px] uppercase tracking-widest text-sand-muted/60">
          <a class="hover:text-primary transition-colors" href="#">Privacy Policy</a>
          <a class="hover:text-primary transition-colors" href="#">Terms of Service</a>
          <a class="hover:text-primary transition-colors" href="#">Help Center</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;
      try {
        const response = await fetch('http://localhost:5000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.message || 'Login failed');
        }

        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        this.$emit('login-success', data);
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
