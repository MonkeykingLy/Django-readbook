<template>
<div class="login_wrap">
	<div class="header">
		<Header></Header>
	</div>
	
	<div class="wrap_login login_form">
		<el-form ref="loginFormRef" :model="loginForm" :label-position="labelPosition" label-width="80px">
			<!-- Header font -->
			<div class="login_title_wrap">
				<div class="login_title">Login</div>
			</div>
			<div class="login_form">
			<!-- Username -->
			<el-form-item label="Username" prop="username">
				<el-input v-model="loginForm.username" placeholder="username" prefix-icon="iconfont icon-user"></el-input>
			</el-form-item>
			<!-- Password -->
			<el-form-item label="Password" prop="password">
				<el-input type="password" v-model="loginForm.password" placeholder="password" prefix-icon="iconfont icon-lock"></el-input>
			</el-form-item>
			<!-- button -->
			<el-form-item class="btns">
				<el-button type="primary" @click="login">Login</el-button>
			</el-form-item>
			</div>
			<div class="login_other">
				No account number? <router-link to='/register'>register</router-link>
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
	return {
		labelPosition: 'left',
		loginForm: {
		username: '',
		password: ''
		}
	};
},
methods: {
	login () {
		this.$refs.loginFormRef.validate(async valid => {
		if(!valid){
			return
		}
		if (this.loginForm.username === '' || this.loginForm.password === '') {
			this.$message.warning('The account or password cannot be empty')
		} else {
		this.$axios({
			method: 'post',
			url: 'http://127.0.0.1:8000/api/login/',
			data: this.loginForm
		}).then(res => {
				window.localStorage.setItem('username',this.loginForm.username)
				window.localStorage.setItem('token', res.data.token)
				this.$message.success(this.loginForm.username+' login successfully')
				this.$router.push('/')
			}).catch(err=>{
				console.log(err);
				this.$message.error('Incorrect username or password')
			})

		}
		})
	}
}
}
</script>

<style lang="less">
body, html{
	height: 100%;
	//overflow: hidden;
}

.login_form {
  // The layout of the login list
  .el-form{
    position: absolute;
    top: 50%;
    margin-top: -293px;
    right: 100px;
    width: 590px;
    height: 586px;
    background-image: repeating-linear-gradient(135deg,rgba(0,0,0,.05),rgba(43,44,46,.5));
    border-radius: 30px;
  }
  
  // Processing of each single column table
  .login_form .el-form-item{
    height: 62.5px;
    margin-left: 80px;
  }

  .login_form .el-form-item__label{
    color: white;
    font-size: 17px;
    margin-right: 10px;
  }

  // Modify the length of the input field
  .login_form .el-input{
    width: 300px;
  }

  .login_other{
    text-align: center;
    //font: bolder;
    color: white;
    font-size: 18px;
  }
}

.login_wrap{
	position: absolute;
	height: 100%;
	width: 100%;
	background: url(../assets/login_img.jpg) no-repeat fixed;
	background-size: cover;
	background-origin: border-box;
}

.wrap_login{
	position: absolute;
	// background-color: deeppink;
	height: 90%;
	width: 100%;
}

// title Center + font
.login_title{
	text-align: center;
	font: 50px/168px bolder sans-serif;
	font-style: italic;
	color: white;
}
</style>
