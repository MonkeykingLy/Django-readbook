

<template>
	<div>
		<Header></Header>

		<div class="body">

			<div class="title"><h3 style="word-break: break-all">{{book.title}}</h3></div>

			<div class="img-box" >
				<img  :src="book.imageLink" style="width:90%;height: 100% " alt="">
			</div>

			<div class="book_item text-block">
				<div><p>Author: {{book.authors}}</p></div>
				<div><p>Publisher: {{book.publisher}}</p></div>
				<div><p>Publish date: {{book.publisher_data}}</p></div>
				<div><p>ISBN: {{book.ISBN}}</p></div>
				<div><p>Categories: {{book.category}}</p></div>
				<el-tag v-show="token_log" type="success"> {{this.result.have_read}}</el-tag>



			</div>

			<div class="read_score">
				<read_score ref="child2" :res="result"></read_score>
			</div>
			<div class="btn_add">
				<!--component add to collection-->
				<add_collection :bookID="result.book_id" :book_name="book.book_id" ></add_collection>
			</div>

			<div class="rating">
				<!--component rating and commit-->
				<rating_commit ref="child" @val="receive_from_rating" :currentuser_rating="result.user_rating" :bookID="result.book_id" ></rating_commit>
			</div>
			<!--show all reviews-->
			<h3 style="margin:10px 0">Reviews:</h3>
			<div v-for="(item,index) in this.result.review_book" class="get_review_box" v-bind:key="item.id">
				<span class="username">{{item.user}}</span>
					<el-rate class="inner_socre"
							v-model="item.rating"
							disabled
							text-color="#ff9900"
							score-template="{value}">
			</el-rate>
				<span class="inner_data">{{item.create_time}}</span>
				<div v-show="isShow" class="inner_content">
					<span style="overflow-wrap:break-word;">{{item.content}}</span>
					<span class="number">{{item.like_count_num}}</span>
					<img :class="{active:currentIndex===index}" class="agree_img" @click="changeNumber(item,index)" :src="item.like_status===1? require('../img/single_book_child/agree_true.png'): require('../img/single_book_child/agree.png')" alt="">

				</div>
			</div>
		</div>
	</div>
</template>

<script>
import Header from '../components/homepage_components/homepage_header'
import {getSingleBookmultdata1} from '../network/requestsWithoutLogin'
import {getSingleBookmultdata} from '../network/requests'

import {postLikeIt} from '../network/requests'
import read_score from '../components/single_book_components/read_score'
import add_collection from '../components/single_book_components/add_collection'
import rating_commit from '../components/single_book_components/rating_commit'
export default {
	name: 'one_book',
	data () {
		return {
			token_log: localStorage.getItem('token'),
			id: null,
			currentIndex: 0, //for loop in reviews, get the current index
			review: [],
			value: Number,
			book: {},
			postvlaue: {  //post value of like it
				// "review_id":value.id,
				"review_id": String,
				// "book_id":this.result.book_id,
				"book_id": String,
				"likeit": {
					"status": null
				}
			},
			isShow:true,// if review content is empty, then become false
			isActive: true,
			book_id: null,
			result: {
				rate: Number,
				TotalCount: Number,
				averageScore: Number,
				book_id: "",
				user_rating:0,
				read:0,

				review_book: []

			},
			update_cont: 0
		}

	},
	components: {
		Header,
		read_score,
		rating_commit,
		add_collection,
	},

	created () {
		this.getData();

	},


	methods: {
		receive_from_rating(){
			let post_value = {book_id: this.book.book_id}
			getSingleBookmultdata(post_value).then(res => {
				console.log(res)
				// let that=this
				let rating_list=res.rating_analyse
				let count=rating_list.how_many_user_scored
				let five=rating_list.five*count*5
				let four=rating_list.four*count*4
				let three=rating_list.three*count*3
				let two=rating_list.two*count*2
				let one=rating_list.one*count*1
				let averagescore=(five+four+three+two+one)/count
				// this.result.TotalCount=count
				this.result = res
				this.result.user_rating=res.user_rating_review.user_rating
				this.result.rate = res.rating_analyse.rating
				this.result.read=res.rating_analyse.how_many_user_read
				this.result.TotalCount = res.rating_analyse.how_many_user_scored
				this.result.averageScore = res.rating_analyse.average_rating
				this.result.book_id = res.id
				this.result.review_book = res.review_book
				// this.result = res
				// this.result.rate = res.rating_analyse.rating
				// this.result.TotalCount = res.rating_analyse.how_many_user_scored
				// this.result.averageScore = res.rating_analyse.average_rating
				// this.result.book_id = res.id
				// this.result.review_book = res.review_book

				this.result.averageScore=parseFloat(averagescore.toFixed(1))
				if(res.read_or_not){
					this.result.have_read='have read'

				}else{
					this.result.have_read='not read'

				}
				this.$refs.child2.init(this.result)

				this.sort_commit(this.result)
			}).catch(res => {
				console.log(res)
			})



		},
		// sort the commit
		sort_commit(val){
			let newValue=[]
			newValue.push(val)
			let len=newValue[0].review_book.length
			let temp={}
			let maxIndex=0
			for(let i in newValue[0].review_book){
				maxIndex=parseInt(i)
				for (let j =parseInt(i)+1;j<len;j++){
					if (newValue[0].review_book[maxIndex].like_count_num<newValue[0].review_book[j].like_count_num){
						maxIndex=j
					}
				}
				temp=newValue[0].review_book[i]
				newValue[0].review_book[i]=newValue[0].review_book[maxIndex]
				newValue[0].review_book[maxIndex]=temp
			//
			}

		},
		// get all info about this book
		getData () {
			this.book = this.$route.query
			let post_value = {book_id: this.book.book_id}


			// if user has login
			if (this.token_log) {
				getSingleBookmultdata(post_value).then(result => {
					console.log(result)
					this.result = result
					this.result.user_rating=result.user_rating_review.user_rating
					this.result.rate = result.rating_analyse.rating
					this.result.read=result.rating_analyse.how_many_user_read
					this.result.TotalCount = result.rating_analyse.how_many_user_scored
					this.result.averageScore = result.rating_analyse.average_rating
					this.result.book_id = result.id
					this.result.review_book = result.review_book
					// console.log(result.read_or_not)
					if(result.read_or_not){
						this.result.have_read='have read'

					}else{
						this.result.have_read='not read'

					}
					this.$refs.child.init(this.result.user_rating)
					// this.$refs.child2.init(this.result.rating_analyse.how_many_user_read)
					this.$refs.child2.init(this.result)

					// console.log(this.result)

					this.sort_commit(this.result)

				}).catch(res => {
					console.log(res)
				})
			} else {
				//request book info like average score, reviews, totalcount of how many people have read
				getSingleBookmultdata1(post_value).then(result => {
					this.result = result
					this.result.rate = result.rating_analyse.rating
					this.result.TotalCount = result.rating_analyse.how_many_user_scored
					this.result.averageScore = result.rating_analyse.average_rating
					this.result.book_id = result.id
					this.result.review_book = result.review_book
					this.result.read=result.rating_analyse.how_many_user_read

					this.$refs.child2.init(this.result)

					this.sort_commit(this.result)

				}).catch(res => {
					console.log(res)
				})
			}


		},
		//agree the the review or not
		changeNumber (val, index) {
			if(this.token_log){
				this.currentIndex = index //change the image or not based on like or not
				this.postvlaue.book_id = this.result.book_id //post book_id of this review
				this.postvlaue.review_id = val.id  //post review_id of this book

				if (!val.like_status) { //if not click like before
					val.like_status = 1
					this.postvlaue.likeit.status = 1

				} else {   //if have already click like
					val.like_status = 0
					this.currentIndex = -1
					this.postvlaue.likeit.status = -1
				}
				postLikeIt(this.postvlaue).then(res => {
					if (val.like_status === 1) {
						val.like_count_num += 1
					} else {
						val.like_count_num -= 1
					}
					console.log(res)
				}).catch(res => {
					console.log(res)
				})

			}
			else{
				this.$message({message: 'please login: ', type: 'warning',showClose: true,})

			}



		},
	}
}
</script>

<style lang="less" scoped>
	.body{
		width: 70%;
		margin: 80px auto;
		position: relative;
	}
	.title{
		margin: 20px 0;
	}

	.img-box{
		width: 200px;
		height: 250px;
		display: inline-block;

	}
	.text-block{
		display: inline-block;
		vertical-align: top;

		width: 50%;
		word-break: break-all
	}
	.read_score{
		padding-left: 10px;
		display: inline-block;
		vertical-align: top;
		border-left: solid 1px gray;

	}
	.rating{
		margin: 15px 5px;
		display: inline-block;
		vertical-align: top;


		/*font-size: 18px;*/
	}
	.btn_add{
		width: 20%;
		display: inline-block;
		vertical-align: top;
		margin-top: 220px;
	}

	.get_review_box{
		width: 95%;
		border-top: 2px solid gray;
		height: 10%;
	}

	.username{
		color: #3377aa;
		margin-right: 20px;
		display: inline-block;
	}
	.inner_socre{
		margin-right: 10px;
		display: inline-block;

	}
	.inner_data{
		color: #666666;
		margin-right: 10px;
		display: inline-block;

	}
	.inner_content{
		display: block;
		margin: 10px 0;
	}
	.agree_img{
		display:inline-block ;
		float: right;
		right: 30px;
		top: 10px;
		width: 20px;
		height: 20px;
	}
	.number{
		display:inline-block;
		float: right;
		margin-left: 5px;
		right:10px;
		top:10px
	}
	.active{
		color: pink;
	}



</style>