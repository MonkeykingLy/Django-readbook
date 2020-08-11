
<template>
	<div>
<!--		current page and display all books, every book show img, average_rating,title,author,publisher,publisher_data, category-->
		<div class="info" style="margin-bottom: 10px">Totally related books: {{books[real_page-1].total_book}}</div>
		<div class="info">Current page: {{books[real_page-1].page+1}}.</div>


		<div class="all_book" v-for="item in books[real_page-1].book_li" :key="item.ISBN">

			<div class="item_box">
				<div class="book_item img-box">
					<img :src="item.imageLink" style="width:90%;height: 100% " alt="" @click="jump_one_book(item)">
				</div>

				<div class="info-box text-block">
					<div><h5 style="word-break: break-all">{{item.title}}</h5></div>
					<el-rate
									v-model="item.avg_rating"
									disabled
									show-score
									text-color="#ff9900"
									score-template="{value}">
					</el-rate>

					<div><p>Author: {{item.authors}}</p></div>
					<div><p>Publisher: {{item.publisher}}</p></div>
					<div><p>publish_date: {{item.publish_date}}</p></div>
					<div><p>category: {{item.categories}}</p></div>

				</div>
			</div>


		</div>
		<div style="display:flex; justify-content: center">

			<el-pagination
							background
							@current-change="getpage"
							:page-size="10"
							:pager-count="11"
							layout="prev, pager, next"
							:total=books[0].total_book>
			</el-pagination>
		</div>


	</div>
</template>

<script>
export default {
	data () {
		return {
			token_log: localStorage.getItem('token'),
			real_page: 1,


		}
	},

	name: 'book_list',
	props: {
		//books is received from father search_result page
		books: {
			type: Array,
			default () {
				return [{
					book_li: {authors: 'Joseph Eddy Fontenrose', publisher: 'Biblo & Tannen Publishers'},
					page: 0,
					total_book: 1
				}]
			}

		}
	},

	watch: {
		books (val) {
			this.real_page = 1
			this.books = val
		}

	},


	methods: {

		getpage (value) {
			this.real_page = value

		},
		isShow () {
			if (typeof (this.books.page) === 'undefined') {
				return false
			}

		},
		jump_one_book (value) {
			// console.log(value)
			this.$router.push({
				name: 'one_book',

				query: {
					// item:value
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


}
</script>

<style lang="less" scoped>

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
		width: 68%;
		word-break: break-all;
	}
	.info-box{
		display: inline-block;
		margin: 0 20px 20px 5px
	}


	.info {
		font-size: 14px;
		opacity: 0.7;
	}

	p {
		line-height: 1;
	}
	.el-pagination{
		margin:40px 0 100px 0;
	}


</style>