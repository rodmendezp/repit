<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col">
            <h1>Welcome!</h1>
            <form ref="form" method="post" class="form-group register-form" @submit.prevent="onSubmit">
                <div class="block">
                    <label for="id_email">Email</label>
                    <input v-model="form.email.value"
                           :class="form.email.classes"
                           @input="validateClasses(form.email)"
                           placeholder="your@email.com" required
                           ref="email" type="email" name="email" id="id_email"/>
                </div>
                <div class="block">
                    <label for="id_password">Password</label>
                    <input v-model="form.password.value"
                           :class="form.password.classes"
                           ref="password" type="password" name="password" id="id_password"
                           placeholder="Password" required/>
                </div>
                <div class="align-items-center" style="text-align: center">
                    <button type="submit" class="btn btn-primary">Sign In</button>
                </div>
            </form>
            <div class="not-account">
                <p class="p-font">Do not have an account? <router-link class="btn btn-primary" to="signup" tag="button">Sign Up</router-link></p>
            </div>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    import FormValidation from '@/mixins/formValidation';

    export default {
        name: 'SignInView',
        mixins: [
            FormValidation,
        ],
        data() {
            return {
                form: {
                    email: {
                        value: '',
                        classes: {
                            'form-control': true,
                            'form-control-lg': true,
                            'is-valid': false,
                            'is-invalid': false,
                        },
                        validations: {
                            'is-valid': ['notEmpty', 'isEmail'],
                            'is-invalid': ['isEmpty', 'notEmail'],
                        },
                    },
                    password: {
                        value: '',
                        classes: {
                            'form-control': true,
                            'form-control-lg': true,
                        },
                        validations: {
                            'is-valid': ['notEmpty'],
                            'is-invalid': ['isEmpty'],
                        },
                    },
                },
            };
        },
        methods: {
            onSuccess(message) {
                this.state = 'success';
                this.submitResponse = message;
            },
            onError(message) {
                this.state = 'error';
                this.submitResponse = message;
                this.form.password.classes['is-invalid'] = true;
            },
            loading() {
                this.state = 'loading';
            },
            loadingUser() {
                this.state = 'loading_user';
            },
            onSubmit() {
                const formData = new FormData();
                const xhr = new XMLHttpRequest();
                const fields = this.form;
                const fieldNames = Object.keys(fields);
                for (let i = 0; i < fieldNames.length; i += 1) {
                    const fieldName = fieldNames[i];
                    const field = fields[fieldName];
                    if (!this.isValid(field.value, field.validations['is-valid'])) {
                        console.log('Unexpected form submission. Aborting');
                    }
                    if (this.isInvalid(field.value, field.validations['is-invalid'])) {
                        console.log('Unexpected form submission. Aborting');
                    }
                    console.log('append ', fieldName, ' = ', field.value);
                    formData.append(fieldName, field.value);
                }
                formData.append('to', '/app');
                console.log(formData);
                xhr.open('POST', '/accounts/login/', true);
                /* eslint no-undef: 0 */
                xhr.setRequestHeader('X-CSRFToken', CSRF_INPUT.value);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4) {
                        const response = JSON.parse(xhr.response);
                        // Redirect to case
                        if (xhr.status === 302) {
                            window.location.replace(response.url);
                        }
                        // Incorrect password case
                        if (xhr.status === 400) {
                            this.onError('Invalid form submission.');
                        }
                    }
                };
                xhr.onloadend = () => {
                    if (xhr.status === 404) {
                        console.warn('Error 404: Please contact our team if the problem persist.');
                        this.onError('We are really sorry but something unexpected happened. Please try again later.');
                    }
                };
                xhr.onerror = () => {
                    console.warn('An unexpected error occurred when contacting server.');
                    this.onError('We are really sorry but something unexpected happened. Please try again later.');
                };
                xhr.send(formData);
            },
        },
    };
</script>

<style lang="sass">
    @import "~@/styles/auth/main.scss"

    .block
        display: inline-flex

    .block label
        display: inline-block
        width: 200px
        text-align: right
        color: white
    .block input
        margin-left: 10px

    .register-form
        max-width: 600px
        margin-left: auto
        margin-right: auto

    .p-font
        font-size: 20px
        font-weight: 500
        color: white

    .not-account
        bottom: 0
        position: fixed
        text-align: center
</style>
