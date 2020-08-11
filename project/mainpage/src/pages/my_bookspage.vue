<template>
	<div id="app2">
		<div class="header">
			<Header></Header>
		</div>
		<!-- three part in this page
			1. u can search a book inside your collection
			2. show all books from your all collections
			3. display all books in one collection and u can remove that book in this collection-->
		<div class="search_model">
			<!-- search a book inside your collection-->
			<el-input v-model="input" placeholder="Search a book inside your collections" @keyup.enter.native="jump_this_book">
				<el-button  style="display: inline-block" slot="append" icon="el-icon-search" @click="jump_this_book"></el-button>
			</el-input>

		</div>

		<div class="body">
			<!-- choose one collection and display books in a collection-->
			<div class="choose_collection">
				<el-button style="width: 100%" @click="isShow=true;show2=false;show=false;reload_page()" size="small">All books</el-button>
				<p style="margin-top:20px; border-bottom: 1px solid gray"></p>
				<p style="display: inline-block; margin:auto 10px">Your collections:</p>
				<el-select class="collections" v-model="value" placeholder="please select a collection" @change="currentSel(value)">
					<el-option
									v-for="item in options"
									:key="item.value"
									:label="item.label"
									:value="item.value"
					>
					</el-option>
				</el-select>
			</div>

			<div class="collection_book" >
				<!-- show all books from  your all  collections-->
				<div v-show="isShow" >
					<el-divider content-position="center" class="divider">All books</el-divider>

					<div  v-for="item in all_books" :key="item.ISBN">
						<div class="book_item img-box" >
							<img :src="item.imageLink" style="width:90%;height: 100% " alt="" @click="jump_one_book(item)"/>
						</div>

						<div class="text-block">
							<div><h5 style="word-break: break-all">{{item.title}}</h5></div>
							<el-rate
											v-model="item.avg_rating"
											disabled
											show-score
											text-color="#ff9900"
											score-template="{value}">
							</el-rate>
							<div class="size">
								<div><p>Author: {{item.authors}}</p></div>
								<div><p>Publisher: {{item.publisher}}</p></div>
								<div><p>publish_date: {{item.publish_date}}</p></div>
								<div><p>category: {{item.categories}}</p></div>

							</div>

						</div>

					</div>
				</div>
    
				<!-- show all books when search in your collections-->
				<div v-show="show">
					<el-divider content-position="center" class="divider">search result in your collections</el-divider>
					<div v-for="(item,index) in search_book" :key="index">
						<div class="book_item img-box" >
							<img :src="item.imageLink" style="width:90%;height: 100% " alt=""  @click="jump_one_book(item)">
						</div>
						<div class="text-block">
							<div><h5 style="word-break: break-all">{{item.title}}</h5></div>
							<el-rate
											v-model="item.avg_rating"
											disabled
											show-score
											text-color="#ff9900"
											score-template="{value}">
							</el-rate>
							<div class="size">
								<div><p>Author: {{item.authors}}</p></div>
								<div><p>Publisher: {{item.publisher}}</p></div>
								<div><p>publish_date: {{item.publish_date}}</p></div>
								<div><p>category: {{item.categories}}</p></div>
							</div>
						</div>
					</div>
				</div>


				<!-- show current collection name-->
				<!-- show book info: img, author, title, rating .....-->
				<div v-show="show2">
					<el-divider content-position="center" class="divider">{{value}}</el-divider>

					<div v-for="item in books2" :key="item.imageLink">
						<div class="book_item img-box">
							<img :src="item.imageLink" class="img" style="width:90%;height: 100% " @click="jump_one_book(item)" />
						</div>
						<div class="text-block right_border">
							<div><h5 style="word-break: break-all">{{item.title}}</h5></div>
							<el-rate
											v-model="item.avg_rating"
											disabled
											show-score
											text-color="#ff9900"
											score-template="{value}">
							</el-rate>
							<div class="size">
								<div><p>Author: {{item.authors}}</p></div>
								<div><p>Publisher: {{item.publisher}}</p></div>
								<div><p>publish_date: {{item.publish_date}}</p></div>
								<div><p>category: {{item.categories}}</p></div>

							</div>
						</div>
						<div class="operate book_item">
							<el-tag type="success"> {{item.read}}</el-tag>



							<el-popconfirm
											confirmButtonText='confirm'
											cancelButtonText='cancel'
											icon="el-icon-info"
											iconColor="red"
											title="Confirm to delete this book from current collection"
											@onConfirm="del(value,item)"

							>
								<el-button style="display: block" slot="reference">Remove this book</el-button>
							</el-popconfirm>
						</div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script>

import {getCollectionmultdata,delBookfromCollection,getSingleBookmultdata} from '../network/requests'
import Header from '../components/homepage_components/homepage_header'
export default {
	name: 'my_bookspage',
	data () {
		return {
			token_log: localStorage.getItem('token'),
			books:[],
			all_books:[],
			name:'',
			input:'',
			isShow:true,
			search_book:[],
			show:false,
			show2:false,  // one book info
			books2: [],       // current collection's books
			options: [],     // collections' content
			value: '',       // collection name
			// cur_key: 0,      // collection id
			collections: [], // result from api package
			item: '', // one book param
			delbookform: {
				collection_id: '',
				book_id:''
			},
		}
	},
	components: {
		Header,
	},
	mounted () {
		getCollectionmultdata().then(res=>{


			this.books=res
			this.getAllBooks(res)

			// all collections
			this.collections = res
			this.getCollectionNames(res)   // get all collection name from the api

		}).catch(res=>{
			console.log(res)})

	},
	methods: {
		del(name,book){ //delete this book from current collection

			let len=this.books.length

			for(let i =0;i<len;i++){
				if (this.books[i].name===name){

					this.delbookform.collection_id=this.books[i].id
					this.delbookform.book_id=book.id
				}

			}

			delBookfromCollection(this.delbookform).then(res=>{
				console.log(res)})
			location.reload()
		},

		getAllBooks(val){
			let len=val.length
			// console.log(val)
			let books_name=[]
			for (let i=0;i<len;i++){
				let new_len=val[i].books.length
				let books=val[i].books


				for(let j=0;j<new_len;j++){


					// console.log(books_name)
					if (books_name.indexOf(books[j].title)===-1){
						// console.log(books[j].id)

						books_name.push(books[j].title)
						let post_value = {book_id: books[j].id}

						getSingleBookmultdata(post_value).then(res=>{
							if(res.read_or_not){
								books[j].read='have read'

							}else{
								books[j].read='not read'

							}
							// book['read']=obj.books[i].read_or_not
						})
						books[j].avg_rating=parseFloat(books[j].avg_rating)
						this.all_books.push(books[j])

					}
				}
			}
			console.log(this.all_books)
		},
		jump_this_book(){
			this.search_book=[]
			this.isShow=false
			this.show2=false
			this.show=true
   
			let len=this.all_books.length
			for(let i=0;i<len;i++){
				let title=this.all_books[i].title.toLowerCase()
				let input=this.input.toLowerCase()
				if ( title.indexOf(input)!==-1  ){
					this.search_book.push(this.all_books[i])

				}

			}
		},
		// get  books from current collection
		currentSel(selVal) {
			this.value = selVal;
			// console.log(typeof this.value)
			let obj = {}
			obj = this.options.find((item)=>{
				return item.value === selVal;
			});
			this.getCollectionBooks(obj.key)
			this.isShow=false
			this.show=false
			this.show2=true
		},

		getCollectionNames(res) {
			const len = res.length
			let option
			for(let i = 0; i < len; i++) {
				// get all collections' name
				option = {}
				option["key"] = res[i].id
				option["value"] = res[i].name
				this.options.push(option)
			}
		},

		// get books from specific collection through collection id
		getCollectionBooks(col_id) {
			this.books2 = []  // refresh books' list
			let obj = {}
			obj = this.collections.find((item) => {
				return item.id === col_id;
			});
   
			let book
			let len = obj.books.length
			for(let i = 0; i < len; i++) {
				book = {}
				book["id"] = obj.books[i].id
				// console.log(obj.books[i].id)
				book["authors"] = obj.books[i].authors
				book["title"] = obj.books[i].title
				book["imageLink"] = obj.books[i].imageLink
				book["ISBN"] = obj.books[i].ISBN
				book["publisher"] = obj.books[i].publisher
				book["publish_date"] = obj.books[i].publish_date
				book["categories"] = obj.books[i].categories
				book["avg_rating"] = parseFloat(obj.books[i].avg_rating)
				book["read"]=obj.books[i].read





				this.books2.push(book)
			}
			console.log(this.books2)
		},
		reload_page(){
			location.reload()

		},

		jump_one_book(value) {
			this.$router.push({
				name: 'one_book',
				query: {
					// item:value
					book_id: value.id,
					authors: value.authors,
					title: value.title,
					ISBN: value.ISBN,
					publisher: value.publisher,
					imageLink: value.imageLink,
					publisher_data:value.publish_date,
					category:value.categories
				}
			})
		},
	}
}
</script>

<style lang="less" scoped>
    .header {
        text-align: center;
    }
    
	.body{
		width: 80%;
		margin: auto;
	}

	.choose_collection{
		margin-top: 50px;
		width: 15%;
		vertical-align: top;
		display: inline-block;
	}

	.collection_book{
		width: 70%;
		height: 90%;
		margin-left: 5%;
		vertical-align: top;
		display: inline-block;
	}
	.book_item{
		display: inline-block;
		margin: 20px 20px 20px 5px;
	}

	.img-box{
		width: 150px;
		height: 200px;
        cursor:pointer;
	}

	.text-block{
		display: inline-block;
		vertical-align: top;
		width: 52%;
		word-break: break-all;
	}

	.search_model{
		width: 22%;
		margin: 20px 25%;
	}

	.collections{
		margin-top: 10px;
	}

	.size{
		font-size: 15px;
	}

	p{
		line-height: 1;
	}

	.operate{
		display: inline-block;
		vertical-align: top;
	}

	.right_border{
		border-right: 1px solid gray;
	}
 
	/deep/ .el-divider__text{
		font-size: 20px;
	}
	.el-tag{
		margin-bottom: 10px;
	}
</style>