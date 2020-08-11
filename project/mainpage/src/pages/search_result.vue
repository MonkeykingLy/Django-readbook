

<template>
	<div class="box">
		<div>
			<Header></Header>
		</div>

		<div class="body">
			<h2 v-show="isShow">Search {{key_word}}</h2>
			<book_list v-if="isShow" :books="result_list"></book_list>
			<!--show all books in every collections for a user-->
			<div v-show="isShowUser">
				<div  class="user_box">
					user: {{this.key_word}}
				</div>

				<el-select  @change="current_value(value)" class="choose" v-model="value" placeholder=" Choose a collection">
					<el-option
									v-for="item in options"
									:key="item.value"
									:label="item.label"
									:value="item.name">
					</el-option>
				</el-select>
				<div class="user_result">
					<el-divider content-position="center" class="divider">{{value}}</el-divider>

					<div class="item_box" v-for="book in book_array" v-bind:key="book.ISBN">
						<div class="book_item img-box">
							<img :src="book.imageLink" style="width:90%;height: 100% " alt="" @click="jump_one_book(book)">
						</div>

						<div class="info-box text-block">
							<div><h5 style="word-break: break-all">{{book.title}}</h5></div>
							<el-rate
											v-model="book.avg_rating"
											disabled
											show-score
											text-color="#ff9900"
											score-template="{value}">
							</el-rate>

							<div><p>Author: {{book.authors}}</p></div>
							<div><p>Publisher: {{book.publisher}}</p></div>
							<div><p>publish_date: {{book.publish_date}}</p></div>
							<div><p>category: {{book.categories}}</p></div>
						</div>
					</div>

				</div>
			</div>
		</div>
	</div>
</template>

<script>
import book_list from '../components/search_result_components/book_list'
import {getSearchResult1, filtersearchbook1,getSearchUserResult1} from '../network/requestsWithoutLogin'
import Header from '../components/homepage_components/homepage_header'

export default {
	name: 'search_result',
	data () {
		return {
			token_log: localStorage.getItem('token'),
			search_type: 'Title',
			key_word: '',
			score: 0,
			result_list: [],
			isShow: false,
			isShowUser:false,
			user: '',
			post_value: {},
			options: [], //all collection's name
			value: '', //current choosen collection
			books:[], //array contains collection name and books
			book_array:[], //current book in choosen collection

		}
	},
	
	components: {
		// search_model,
		book_list,
		Header,

	},
	methods: {

		//divided the books into pages, every page contains 10 books
		slite_pages(value) {
			let len = value.length
			for (let j = 0; j < len; j++) {
				value[j].avg_rating = parseFloat(value[j].avg_rating)
			}
			let list = []
			let start = 0
			let num = parseInt(value.length / 10)
			let i
			for (i = 0; i <= num; i++) {
				list.push({total_book: value.length, page: i, book_li: value.slice(start, (i + 1) * 10)})
				start = (i + 1) * 10
			}
			let result = value.slice(start, i * 10)
			if (result.length) {
				list.push({total_book: value.length, page: i, book_li: value.slice(start, (i + 1) * 10)})
			}
			return list
		},
		// search based on user get the result
		getUserResult(val){
			getSearchUserResult1(val).then(res => {
				if(res.status===400){
					this.$message({message: 'cannot find user: ' + this.key_word, showClose: true,})
					this.isShowUser=false
					return 'cannot find user '+this.key_word
				}
				this.options=[]
				this.books=[]


				this.value = res[0].collections[0].name
				for (let i in res){

					let one_collection=res[i].collections
					for (let j in one_collection){
						this.options.push({keys:j,name:one_collection[j].name}) //get all collections' name
						this.books.push({name:one_collection[j].name,value:one_collection[j].books}) //get all books based on collection name

					}
				}

				//show books in current collection
				let temp=this.books.find(item =>item.name===this.value)
				this.book_array=temp.value
				for(let i in this.book_array){
					this.book_array[i].avg_rating=parseFloat(this.book_array[i].avg_rating)
				}
			}).catch(res=>{

				console.log(res)})
		},
		//when selection options has changed
		current_value(value){
			this.value=value
			let temp=this.books.find(item =>item.name===this.value)
			this.book_array=temp.value
			for(let i in this.book_array){
				this.book_array[i].avg_rating=parseFloat(this.book_array[i].avg_rating)
			}
		},

		//search result based on title/author/user
		getResult: function (val) {
			if(val.key_word==="" && val.search_type==='' && val.score===""){
				this.$message({message: 'try to search a book based on  author/title/user', showClose: true,})
				this.$router.push('/')

			}

			this.key_word = val.key_word
			if (val.search_type !== '') {
				this.search_type = val.search_type

			}
			this.score = parseFloat(val.score)

			// if search not based on rating, which means not choose rating range
			if (isNaN(this.score)) {
				// case0 search based on user
				if (this.search_type === 'user') {
					this.isShow = false

					this.post_value = {search_type: this.search_type, key_word: this.key_word}
					this.getUserResult(this.post_value)
					this.isShowUser=true


					}
				//search based on Title or authors
				else {
					this.isShowUser=false
					this.post_value = {search_type: this.search_type, key_word: this.key_word}
				// console.log(this.post_value)
				getSearchResult1(this.post_value).then(res => {
						if (res.status === 400) {
							this.$message({message: 'no book satisfied the search condition: ' + this.key_word, showClose: true,})
							this.isShow = false
							this.isShowUser=false

							let temp = this.key_word
							this.key_word = this.search_type + temp + '. There is no related book'
						} else {
							//if get the response, the show the result
							this.result_list = this.slite_pages(res)
							this.isShow = true
						}
					}).catch(err => {

						console.log(err)
					})
				}
			}
			// search based on rating range
			else {
				if (this.search_type === 'user') {
					this.isShow = false

					this.post_value = {search_type: this.search_type, key_word: this.key_word}
					this.getUserResult(this.post_value)
					this.isShowUser=true
				}
				else{
					this.isShowUser=false

					this.post_value = {search_type: this.search_type, key_word: this.key_word, filter_rating: this.score}
					filtersearchbook1(this.post_value).then(res => {
						if (res.status === 400) {
							this.$message({message: 'no book satisfied the search condition: ' + this.key_word, showClose: true,})

							this.isShow = false
							this.isShowUser=false
							let temp = this.key_word
							this.key_word = this.search_type + temp + '. There is no related book'

						} else {


							console.log(res)

							//get the result
							this.result_list = this.slite_pages(res)
							this.isShow = true
						}
					}).catch(err => {

						console.log(err)
					})
				}


			}
		},
		jump_one_book (value) {  //jump to book detail page
			this.$router.push({
				name: 'one_book',

				query: {
					book_id: value.id,
					authors: value.authors,
					title: value.title,
					ISBN: value.ISBN,
					publisher: value.publisher,
					publisher_data: value.publish_date,
					imageLink: value.imageLink,
					category: value.categories
				}

			})
		},


	},
	//listen to the route, if changed reload the page
	watch: {
		'$route' () {
			this.getResult(this.$route.query)
			this.search_type = 'Title'
		},

	},
	computed:{

	},

	mounted () {
		this.getResult(this.$route.query)
		this.search_type = 'Title'

	},

}
</script>

<style lang="less" scoped>
	.body {
		width: 70%;
		margin: auto;
	}

	h2 {
		height: 30px;
		margin: 10px 0 20px 0;
	}

	.choose{
		width: 22%;
		margin-top: 30px;
		margin-left: 80%;
		display: inline-block;
	}

	.book_item {
		display: inline-block;
		margin: 20px 20px 20px 5px

	}
	.img-box{
		width: 150px;
		height: 200px;
	}

	.text-block{
		display: inline-block;
		vertical-align: top;
		width: 52%;
		word-break: break-all;
	}

	.user_result{
		margin-top: 20px;
	}

	.user_box{
		position: absolute;
		margin-top: 40px;
		margin-left: 48%;
	}
	.info-box{
		display: inline-block;
		margin: 0 20px 20px 5px
	}
	p{
		line-height: 1;
	}
</style>