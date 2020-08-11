<!-- Written by Yangyu GAO -->
<template>
    <el-menu :default-active="activeIndex2" class="el-menu-main" mode="horizontal" background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
        <!-- click to jump to homepage -->
		<el-menu-item @click="jump_homepage" title="homepage">
			<img src="../../../logo.png" height="38" width="65"/>
		</el-menu-item>
		
		<el-menu-item index="1" @click="jump_homepage">
			Home
        </el-menu-item>

		<!-- jump to my books page -->
        <el-menu-item index="6" @click="jump_my_books_page" v-if="token_log">
            My books
        </el-menu-item>

		<!-- search function entrance -->
        <div class="search">
            <el-select class="select_box1" v-model="select" slot="prepend" placeholder="select book/author">
                <el-option  label="Title" value="Title" ></el-option>
                <el-option label="Author" value="Authors" ></el-option>
                <el-option label="User" value="user"></el-option>
            </el-select>

			<el-select :disabled="isShow()" class="select_box1" v-model="score" slot="prepend" placeholder="average score range">
                <el-option label="all books" value="0" ></el-option>
                <el-option label="4-5 stars" value="4" ></el-option>
                <el-option  label="3-5 stars" value="3" ></el-option>
                <el-option label="2-5 stars" value="2" ></el-option>
                <el-option label="1-5 stars" value="1" ></el-option>
            </el-select>

			<el-input placeholder="input contents" v-model="input3" class="input-with-select"  @keyup.enter.native="jump_search_result"></el-input>

            <el-button  style="display: inline-block" slot="append" icon="el-icon-search" @click="jump_search_result"></el-button>
        </div>

        <!--  Click to register  -->
        <el-menu-item index="2" style="float:right" @click="jump_reg" v-if="token_log == null">
            Register
        </el-menu-item>

        <!-- Click to login -->
        <el-menu-item index="3" style="float:right" @click="jump_login" v-if="token_log == null">
            Login
        </el-menu-item>

		<!-- show only after login, click to logout -->
        <el-menu-item index="4" style="float:right" @click="jump_logout" v-if="token_log != null">
            Logout
        </el-menu-item>
	
		<!-- show only after login, click to see personal profile -->
        <el-menu-item index="5" style="float:right" @click="jump_Profile" v-if="token_log != null"
        title="My Profile">
			Hi, {{ username }}
        </el-menu-item>
    </el-menu>
</template>

<script>
export default {
    data() {
        return {
            token_log: localStorage.getItem('token'),       // get token
            // activeIndex: '1',
            activeIndex2: '1',
            input1: '',
            input2: '',
            input3: '',
            select: '',
            score: '',
			username: localStorage.getItem('username'),     // get username
        };
    },
	
	methods: {
        // judge whether show or not
        isShow(){
            if (this.select==='user'){
                return true
            }
        },

        jump_homepage() {
            this.$router.push('/')
        },

        jump_reg() {
            this.$router.push('register')
        },

        jump_login() {
            this.$router.push('login')
        },

        jump_Profile() {
            this.$router.push('person')
        },

        jump_logout() {
			this.$forceUpdate()
            window.localStorage.clear()
            this.$router.go(0)
        },

        jump_my_books_page() {
            this.$router.push('my_bookspage')
        },
		
        jump_search_result(){
            this.$router.push({
                name:'search_result',
                query: {
                    key_word:this.input3,
                    search_type:this.select,
                    score:this.score,
                }
            })
        }
    },
}
</script>

<style lang="less" scoped>
    .el-menu-main {
        position: relative;

    }

    .search {
        position: absolute;
        width: 50%;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
    }

    .el-select .el-input {
        width: 130px;
    }
    
    .input-with-select{
        background-color: #fff;
        width: 40%;
        margin-right: 5px;
        border-radius: 3px;
    }

    .select_box1{
        width: 22%;
        margin-right: 10px;
    }
</style>

