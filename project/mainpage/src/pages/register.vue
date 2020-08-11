<template>
<div class="register_wrap">
	<div class="header">
		<Header></Header>
	</div>
	<div class="wrap_register register_form">
		<el-form ref="RegisterFormRef" :model="RegisterForm" :rules="RegisterFormRules" :label-position="labelPosition" label-width="80px">
			<!-- Header font -->
			<div class="register_title_wrap">
				<div class="register_title">Register</div>
			</div>
			<div class="register_form">
			<!-- The user name -->
			<el-form-item label="Username" prop="username">
				<el-input v-model="RegisterForm.username" placeholder="username" prefix-icon="iconfont icon-user"></el-input>
			</el-form-item>
			<!-- Email -->
			<el-form-item label="Email" prop="email">
				<el-input type="email" v-model="RegisterForm.email" placeholder="e-mail" prefix-icon="iconfont icon-email"></el-input>
			</el-form-item>
			<!-- Password -->
			<el-form-item label="Password" prop="password">
				<el-input type="password" v-model="RegisterForm.password" placeholder="password" prefix-icon="iconfont icon-lock"></el-input>
			</el-form-item>
			<!-- CheckPass -->
			<el-form-item label="CheckPass" prop="checkpass">
				<el-input type="password" v-model="RegisterForm.checkpass" placeholder="confirm password" prefix-icon="iconfont icon-lock"></el-input>
			</el-form-item>
			<!-- button -->
			<el-form-item class="btns">
				<el-button type="primary" @click="register('RegisterForm')">Register</el-button>
				<el-button type="info" @click="formreset">Reset</el-button>
			</el-form-item>
			</div>
			<div class="other">
				An existing account? <router-link to='/login'>login</router-link>
			</div>
		</el-form>
	</div>
</div>
</template>


<script>
	import Header from '../components/homepage_components/homepage_header.vue'
	export default {
		components:{
			Header
		},
		data () {
		// Verify that the mailbox format is correct
		let checkEmail = (rule, value, callback) => {
			const mailReg = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(.[a-zA-Z0-9_-])+/
			if (!value) {
                return callback(new Error('Please enter email address'))
			}
			setTimeout(() => {
				if (mailReg.test(value)) {
                    callback()
				} else {
                    callback(new Error('Incorrect email format'))
				}
			}, 100)
		}
		// Verify password
		let validatePass = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('Please enter your password.'))
			} else {
				if (this.RegisterForm.checkpass !== '') {
                    this.$refs.RegisterFormRef.validateField('checkpass')
				}
				callback()
			}
		}
		// Secondary verification password
		let validatePass2 = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('Please enter your password again'))
			} else if (value !== this.RegisterForm.password) {
				callback(new Error('The password is inconsistent!'))
			} else {
				callback()
			}
		}
		return {
			labelPosition: 'left',
			// V-model bound objects
			RegisterForm: {
				username: '',
				password: '',
				checkpass: '',
				email: ''
			},
			// Register the form validation rules
			RegisterFormRules: {
				// Username verification
				username: [
					{ required: true, message: 'Please enter the username', trigger: 'blur' },
					{ min: 3, max: 10, message: 'The length is between 3 and 10 characters', trigger: 'blur' }
				],
				password: [
					{ required: true, validator: validatePass, trigger: 'blur' },
					{ min: 6, max: 10, message: 'The length is between 6 and 10 characters', trigger: 'blur' }
				],
				checkpass: [
					{ required: true, validator: validatePass2, trigger: 'blur' }
				],
				email: [
					{ required: true, validator: checkEmail, trigger: 'blur' }
				]
			}
		}
	},
	methods: {
		formreset() {
			this.$refs.RegisterFormRef.resetFields()
		},
		register() {
			this.$refs.RegisterFormRef.validate(valid => {
				if(!valid){
					return
				}
			this.$axios({
				method: 'post',
				url: 'http://127.0.0.1:8000/api/register/',
				data: this.RegisterForm
			}).then(res => {
				console.log(res);
				this.$refs.RegisterFormRef.validate(async valid => {
				if(!valid){return}
				this.$axios({
					method: 'post',
					url: 'http://127.0.0.1:8000/api/login/',
					data: this.RegisterForm
				}).then(res => {
					window.localStorage.setItem('username',this.RegisterForm.username)
					window.localStorage.setItem('token', res.data.token)
					this.$message.success(this.RegisterForm.username+' login successfully')
					this.$router.push('/')
				}).catch(err=>{
				console.log(err);
				this.$message.error('Username is exist');
				})
			})
			}).catch(err=>{
				console.log(err);
				this.$message.error('Username is exist');
				})
			})
			
		}
	}
	}
</script>

<!-- Add "scoped" attribu
te to limit CSS to this component only -->
<style lang="less">
body, html{
	height: 100%;
	//overflow: hidden;
}

.register_wrap{
	position: absolute;
	height: 100%;
	width: 100%;
	background: url(../assets/register_img.jpg) no-repeat fixed;
	background-size: cover;
	background-origin: border-box;
}

.wrap_register{
	position: absolute;
	height: 90%;
	width: 100%;
}

.register_form {
  // The layout of the registration list
  .el-form{
    position: absolute;
    top: 50%;
    margin-top: -293px;
    right: 100px;
    width: 590px;
    height: 586px;
    background-image: repeating-linear-gradient(135deg,rgba(0,0,0,0.1),rgba(167,178,222,.5));
    border-radius: 30px;
  }

  // title Center + font
  .register_title{
    text-align: center;
    font: 50px/98px bolder sans-serif;
    font-style: italic;
    color: whitesmoke;
    margin-top: 25px;
    margin-bottom: 15px;
  }

  // Processing of each single column table
  .register_form .el-form-item{
    height: 53px;
    margin-left: 40px;
  }

  .register_form .el-form-item__label{
    color: whitesmoke;
    margin-right: 30px;
  }

  // Modify the length of the input field
  .register_form .el-input{
    width: 300px;
  }

  .other{
    text-align: center;
    //font: bolder;
    color: white;
    font-size: 18px;
  }
}
</style>
