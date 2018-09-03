<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col">
            <h1>Welcome!</h1>
            <form ref="form" method="post" @submit.prevent="onSubmit">
                <label for="id_email">Email</label>
                <input v-model="form.email.value"
                       placeholder="your@email.com" required
                       ref="email" type="email" name="email" id="id_email"/>
                <label for="id_password">Password</label>
                <input v-model="form.password.value"
                       ref="password" type="password" name="password" id="id_password"
                       placeholder="Password" required/>
            </form>
            <p>Do not have an account? <router-link to="signup" tag="button">Sign up</router-link></p>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    export default {
        name: 'SignInView',
        data() {
            return {
                form: {
                    email: {
                        value: '',
                    },
                    password: {
                        value: '',
                    },
                },
            };
        },
    };
</script>

<style lang="sass">
    @import "~@/styles/auth/main.scss"
</style>
