<template>
    <div class="row full-height align-items-center">
        <div class="col"></div>
        <div class="col">
            <form ref="form" method="post" class="form-group register-form" @submit.prevent="onSubmit">
                <div class="block">
                    <label for="id_email">Email</label>
                    <input v-model="form.email.value"
                           :class="form.email.classes"
                           @input="validateClasses(form.email); checkUser();"
                           ref="email" type="email" name="email" id="id_email"
                           placeholder="your@email" required/>
                </div>
                <div class="block">
                    <label for="id_first_name">First Name</label>
                    <input v-model="form.first_name.value"
                           :class="form.first_name.classes"
                           @input="validateClasses(form.first_name)"
                           ref="first_name" type="text" name="first_name" id="id_first_name"
                           placeholder="First Name" required/>
                </div>
                <div class="block">
                    <label for="id_last_name">Last Name</label>
                    <input v-model="form.last_name.value"
                           :class="form.last_name.classes"
                           @input="validateClasses(form.last_name)"
                           ref="last_name" type="text" name="last_name" id="id_last_name"
                           placeholder="Last Name" required />
                </div>
                <div class="block">
                    <label for="id_password">Password</label>
                    <input v-model="form.password.value"
                           :class="form.password.classes"
                           @input="validateClasses(form.password); validateClasses(form.confirm_password);"
                           ref="password" type="password" name="password" id="id_password"
                           placeholder="Password" required />
                </div>
                <div class="block">
                    <label for="id_confirm_password">Confirm Password</label>
                    <input v-model="form.confirm_password.value"
                           :class="form.confirm_password.classes"
                           @input="validateClasses(form.confirm_password); validateClasses(form.password);"
                           ref="confirm_password" type="password"
                           name="confirm_password" id="id_confirm_password"
                           placeholder="Password Confirmation " required />
                </div>
                <div class="align-items-center" style="text-align: center">
                    <button :disabled="mailExists" type="submit" class="btn btn-primary">SingUp</button>
                </div>
            </form>
        </div>
        <div class="col"></div>
    </div>
</template>

<script>
    import FormValidation from '@/mixins/formValidation';
    import bButton from 'bootstrap-vue/es/components/button/button';

    export default {
        name: 'SignUpView',
        mixins: [
            FormValidation,
        ],
        data() {
            return {
                mailExists: false,
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
                    first_name: {
                        value: '',
                        classes: {
                            'form-control': true,
                            'form-control-lg': true,
                            'is-valid': false,
                            'is-invalid': false,
                        },
                        validations: {
                            'is-valid': ['notEmpty'],
                            'is-invalid': ['isEmpty'],
                        },
                    },
                    last_name: {
                        value: '',
                        classes: {
                            'form-control': true,
                            'form-control-lg': true,
                            'is-invalid': false,
                            'is-valid': false,
                        },
                        validations: {
                            'is-valid': ['notEmpty'],
                            'is-invalid': ['isEmpty'],
                        },
                    },
                    password: {
                        value: '',
                        classes: {
                            'form-control': true,
                            'form-control-lg': true,
                            'is-invalid': false,
                            'is-valid': false,
                        },
                        validations: {
                            'is-valid': [
                                'notEmpty',
                                { name: 'minLength', params: { min: 8 } },
                            ],
                            'is-invalid': [
                                'isEmpty',
                                { name: 'maxLength', params: { max: 7 } },
                            ],
                        },
                    },
                    confirm_password: {
                        value: '',
                        classes: {
                            'form-control': true,
                            'form-control-lg': true,
                            'is-invalid': false,
                            'is-valid': false,
                        },
                        validations: {
                            'is-valid': [
                                'notEmpty',
                                { name: 'equalTo', params: { field: 'password' } },
                            ],
                            'is-invalid': [
                                'isEmpty',
                                { name: 'notEqualTo', params: { field: 'password' } },
                            ],
                        },
                    },
                },
            };
        },
        components: {
            bButton,
        },
        methods: {
            loading() {
                this.state = 'loading';
            },
            idle() {
                this.state = 'idle';
            },
            checkUser() {
                this.mailExists = false;
                if (!this.form.email.classes['is-valid']) return;
                this.loading();
                const xhr = new XMLHttpRequest();
                xhr.addEventListener('load', () => {
                    if (xhr.readyState === 4) {
                        this.idle();
                        if (xhr.status === 302 || xhr.status === 200) {
                            this.mailExists = true;
                            this.form.email.classes['is-valid'] = false;
                            this.form.email.classes['is-invalid'] = true;
                        }
                    }
                });
                xhr.open('GET', `is_user/?email=${this.form.email.value}`);
                xhr.send();
            },
            onSuccess(message) {
                this.state = 'success';
                this.submitResponse = message;
            },
            onError(message) {
                this.state = 'error';
                this.submitResponse = message;
            },
            onSubmit() {
                this.loading();
                this.$router.push('/');
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
                    formData.append(fieldName, field.value);
                }
                xhr.open('POST', '/accounts/register/', true);
                /* eslint no-undef: 0 */
                xhr.setRequestHeader('X-CSRFToken', CSRF_INPUT.value);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

                xhr.onreadystatechange = () => {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 302 || xhr.status === 200) {
                            const response = JSON.parse(xhr.response);
                            console.log(response);
                            this.onSuccess('Please check your mailbox');
                        }
                    } else {
                        console.log(xhr);
                        this.onError('Invalid form submission');
                    }
                };
                xhr.onloadend = () => {
                    if (xhr.status === 404) {
                        console.warn('Error 404: Please contact our team if the problem persists');
                        this.onError();
                    }
                };
                xhr.onerror = () => {
                    console.warn('An unexpected error ocurred when contacting server');
                    this.onError();
                };
                xhr.send(formData);
            },
        },
    };
</script>

<style lang="sass">
    @import '~@/styles/auth/main.scss';

    .block
        display: inline-flex

    .block label
        display: inline-block
        width: 300px
        text-align: right
        color: white
    .block input
        margin-left: 10px

    .register-form
        max-width: 600px
        margin-left: auto
        margin-right: auto

</style>
