<template>
<div class="wrap">
	<div class="header">
		<Header></Header>
	</div>
	
	<div class="content">
		<el-tabs :tab-position="tabPosition" style="height: 100%;">	
			<!-- Collection -->
			<el-tab-pane label="Collection">
				<div class="collection" >
					<div class="clearfix">
					<!-- select -->
					<div class="collection_head">
						<el-select v-model="value" placeholder="please select a collection"
									@change="currentSel(value)">
							<el-option
									v-for="item in options"
									:key="item.label"
									:value="item.value"
							>
							</el-option>
						</el-select>
					</div>
			
					<!-- create an new collection -->
					<div class="collection_add">
						<el-button @click="dialogFormVisible = true" class="collection_add_button">Create a new collection</el-button>
						<el-dialog title="Create a new collection" :visible.sync="dialogFormVisible">
							<el-form ref="collectionformRef" :model="collectionform" :rules="collectionformRules">
								<el-form-item label="Collection Name" :label-width="formLabelWidth" prop="name">
									<el-input v-model="collectionform.name" autocomplete="off"></el-input>
								</el-form-item>
							</el-form>
							<div slot="footer" class="dialog-footer">
								<el-button @click="dialogFormVisible = false">cancel</el-button>
								<el-button type="primary" @click="submit">confirm</el-button>
							</div>
						</el-dialog>
					</div>
					
					<!-- reset collection name -->
					<div class="collection_reset">
						<el-button  @click="dialogFormVisible2 = true" class="collection_change_button">Rename collection</el-button>
						<el-dialog title="reset collection" :visible.sync="dialogFormVisible2">
							<el-form ref="recollectionFormRef" :model="recollectionForm" :rules="recollectionformRules">
								<el-form-item label="rename collection" :label-width="formLabelWidth" prop="new_name">
									<el-input v-model="recollectionForm.new_name" autocomplete="off"></el-input>
								</el-form-item>
							</el-form>
							<div slot="footer" class="dialog-footer">
								<el-button @click="dialogFormVisible2 = false">cancel</el-button>
								<el-button type="primary" @click="change">confirm</el-button>
							</div>
						</el-dialog>
					</div>
					
					<!-- delete collection -->
					<div class="collection_dele">
						<el-popover
							placement="top"
							width="230"
							v-model="visible">
						<p>Are you sure to delete the collection?</p>
						<div style="text-align: right; margin: 0">
							<el-button size="mini" @click="visible = false">cancel</el-button>
							<el-button size="mini" @click="delete_button">confirm</el-button>
						</div>
							<el-button slot="reference" class="collection_dele_button">Delete collection</el-button>
						</el-popover>
					</div>
				</div>
				<!-- Line showing the current collection name -->
				<el-divider content-position="center">{{value}}</el-divider>
					
					<!-- Collection body, display diagram & Title -->
					<div class="coll_wrap">
						<div class="coll_content" v-for="item in books" :key="item.imageLink">
							<img :src="item.imageLink" class="img" alt/>
							<el-button class="book-detail" @click="jump_one_book(item)">More Details</el-button>
						</div>
					</div>
				</div>
			</el-tab-pane>
			
			<!-- Personal information -->
			<el-tab-pane label="Personal Information">
				<div class="person_information">
					<div class="Per_info_title">
						Personal Information
					</div>
					
					<div class="Per_info">
						
						<el-form ref="PerinfoFormRef" :model="PerinfoForm" label-width="80px" class="register_form">
							<!-- username -->
							<el-form-item label="Username" prop="username">
								<el-input v-model="PerinfoForm.username" placeholder="username" prefix-icon="el-icon-user" :disabled="true"></el-input>
							</el-form-item>
							<!-- email -->
							<el-form-item label="Email" prop="email">
								<el-input type="email" v-model="PerinfoForm.email" placeholder="email" prefix-icon="el-icon-message" :disabled="true"></el-input>
							</el-form-item>
							<!-- join date -->
							<el-form-item label="join date" prop="join date">
								<el-input v-model="PerinfoForm.regisdate" placeholder="join date" prefix-icon="el-icon-date" :disabled="true"></el-input>
							</el-form-item>
							<!-- birthday -->
							<el-form-item label="birthday" prop="birthday">
								<el-date-picker v-model="PerinfoForm.date_of_birth" type="date" placeholder="birthday" :picker-options="pickerOptions0"></el-date-picker>
							</el-form-item>
							<!-- gender -->
							<el-form-item label="Gender" prop="gender">
								<el-radio-group v-model="PerinfoForm.gender">
									<el-radio label="Male"></el-radio>
									<el-radio label="Female"></el-radio>
								</el-radio-group>
							</el-form-item>
							<!-- confirm -->
							<el-form-item class="btns">
								<el-button type="primary" @click="confirm">confirm</el-button>
							</el-form-item>
						</el-form>
					</div>
				</div>
			</el-tab-pane>
			
			<!-- goal detail in current year -->
			<el-tab-pane label="History Goal">
				<div class="history_goal_title">
					Goal details in this year
				</div>
				<div class="history_goal">
					<div>
						<el-timeline :reverse="reverse">
							<el-timeline-item
								v-for="(activity, index) in activities"
								:key="index"
								>
								{{activity.content}}
							</el-timeline-item>
						</el-timeline>
					</div>
				</div>
			</el-tab-pane>
		</el-tabs>
	</div>
</div>
</template>

<script>
import Header from '../components/homepage_components/homepage_header.vue'
import {getperinfodata} from '../network/requests'
import {postperinfo} from '../network/requests'
import {getCollectionmultdata} from '../network/requests'
import {postnewcollection} from '../network/requests'
import {changecollectioname} from '../network/requests'
import {delecollection} from '../network/requests'
import {getCurGoal} from "../network/requests"

export default {
	components:{
		Header
	},
	inject: ["reload"],
	data() {
		// Verify name
		let name = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('Please enter your collection name.'))
			}else {
				callback()
			}
		}
		let new_name = (rule, value, callback) => {
			if (value === '') {
				callback(new Error('Please enter your collection name.'))
			}else {
				callback()
			}
		}
		return {
			//Set the location of the label
			tabPosition: 'left',
			
			// personal information
			pickerOptions0: {
				disabledDate(time) {
					return time.getTime() > Date.now() - 8.64e6 // birthday : only choose dates before today
				}
			},
			PerinfoForm: {
				id:'',
				username: '',
				email: '',
				regisdate: '',
				date_of_birth:'',
				gender: ''
			},
			
			// create an new collection
			token_log: localStorage.getItem('token'),
			options2:[],
			collectionform: {
				name: ''
			},
			dialogFormVisible: false,
			formLabelWidth: '150px',
			collectionformRules: {
				// collection name verification
				name: [
					{ required: true, validator: name, trigger: 'blur' },
					{ min: 1, max: 200, message: 'Please enter the collection name', trigger: 'blur' }
				]
			},
			
			// reset collection name 
			recollectionForm: {
				new_name: '',
				collection_id: ''
			},
			dialogFormVisible2: false,
			recollectionformRules: {
				// collection name verification
				new_name: [
					{ required: true, validator: new_name, trigger: 'blur' },
					{ min: 1, max: 200, message: 'Please enter the collection name', trigger: 'blur' }
				]
			},
			
			// delete collection
			delecollectionform: {
				collection_id: ''
			},
			visible: false,
			//Collection body, display diagram & Title
			books: [],       // current collection's books
			options: [],     // collections' content
			value: '',       // collection name
			collections: [], // result from api package
			img_list: [
				{
					imageLink: require("../img/test book image/harry.jpg"),
					title: 'Harry Porter',
					url: ''  
				},
			],
			
			// goal detail in current year
			addv: '',
			activities: [
				{ contents: 'need to add', key: 1 },
				{ contents: 'need to add', key: 2 },
				{ contents: 'need to add', key: 3 },
				{ contents: 'need to add', key: 4 },
				{ contents: 'need to add', key: 5 },
				{ contents: 'need to add', key: 6 },
				{ contents: 'need to add', key: 7 },
				{ contents: 'need to add', key: 8 },
				{ contents: 'need to add', key: 9 },
				{ contents: 'need to add', key: 10 },
				{ contents: 'need to add', key: 11 },
				{ contents: 'need to add', key: 12 }
			],
			reverse: false, // Specifies the node sort direction. Reverse order
			goal: {
				target : '',
				already_done: ''
			}
		}
	},
	methods: {
		// Personal information
		confirm() {
			this.$refs.PerinfoFormRef.validate(async valid => {
				if (!valid) { return }
				postperinfo(this.PerinfoForm).then(res=>{
					console.log(res);
					this.$message.success('Modify successfully');
				}).catch(err=>{
					console.log(err)
					this.$message.error('Modify failure');
				})
			})
		},
		
		// create an new collection
		submit() {
			let value = {name: this.collectionform.name}
			let exist = false
			for (let i = 0; i < this.options2.length; i++) {
				if (value.name === this.options2[i].name) {
					exist = true
					this.$message.error(' Name repetition ');
				}
			}
			if (exist === false) {
				this.$refs.collectionformRef.validate(async valid => {
					if (!valid) { return }
					postnewcollection(this.collectionform).then(res=>{
						console.log(res);
						this.$message.success('Successfully created');
						this.dialogFormVisible = false;
						this.reload();
					}).catch(err=>{
						console.log(err);
						this.$message.error('Create failure');
					})
				})
			}
		},

		// reset collection name
		change() {
			let value = {new_name: this.recollectionForm.new_name}
			let reexist = false
			for (let i = 0; i < this.options2.length; i++) {
				if (value.new_name === this.options2[i].name) {
					reexist = true
					this.$message.error(' Name repetition ');
				}
			}
			if (reexist === false) {
				this.$refs.recollectionFormRef.validate(async valid => {
					if (!valid) { return }
					changecollectioname(this.recollectionForm).then(res=>{
						console.log(res);
						this.$message.success('Modify successfully');
						this.dialogFormVisible2 = false;
						this.reload();
					}).catch(err=>{
						console.log(err)
						this.$message.error('Modify failure');
					})
				})
			}
		},
		
		//delete collection
		delete_button() {
			delecollection(this.delecollectionform).then(res=>{
				console.log(res);
				this.$message.success('delete successfully');
				this.reload();
			}).catch(err=>{
				console.log(err)
				this.$message.error('delete failure');
			})
		},
		
		// check which collection is now selecting
		currentSel(selVal) {
			this.value = selVal;
			let obj = {}
			obj = this.options.find((item)=>{
				return item.value === selVal;
			});
			this.getCollectionBooks(obj.key)
			this.delecollectionform.collection_id = obj.key
			this.recollectionForm.new_name = obj.value
			this.recollectionForm.collection_id = obj.key
		},
		
		getCollectionNames(res) {
			const len = res.length
			let option
			for(let i = 0; i < len; i++) {
				// 提取collections' name
				option = {}
				option["key"] = res[i].id
				option["value"] = res[i].name
				this.options.push(option)
			}
		},
		
		// get books from specific collection through collection id
		getCollectionBooks(col_id) {
			this.books = []  // refresh books' list
			console.log("now select: " + col_id)
		
			let obj = {}
			obj = this.collections.find((item) => {
				return item.id === col_id;
			});
			let book
			let len = obj.books.length
			for(let i = 0; i < len; i++) {
				book = {}
				book["id"] = obj.books[i].id
				book["authors"] = obj.books[i].authors
				book["title"] = obj.books[i].title
				book["imageLink"] = obj.books[i].imageLink
				book["ISBN"] = obj.books[i].ISBN
				book["publisher"] = obj.books[i].publisher
				book["publish_date"] = obj.books[i].publish_date
				book["categories"] = obj.books[i].categories
				book["join_date"] = obj.books[i].join_date
				book["description"] = obj.books[i].description
				book["avg_rating"] = parseInt(obj.books[i].avg_rating)
				this.books.push(book)
			}
		},
		
		// jump to book detail
		jump_one_book(value) {
			// console.log(value)
			this.$router.push({
				name: 'one_book',
				query: {
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
		
		// sorted by month
		sortBykey(ary, key) {
			return ary.sort(function (a, b) {
				let x = a[key]
				let y = b[key]
				console.log(key)
				return ((x < y) ? -1 : (x > y) ? 1 : 0)
			})
		},
		
		// get current goal
		getGoal() {
			let now = new Date()
			let nowYear = now.getFullYear()
			for(let month = 1; month < 13; month++){
				let curMonth = {year:nowYear, month:month}
				getCurGoal(curMonth).then(res=>{
					console.log(res.target)
					if(typeof(res.target) != undefined){
						this.addv = {content:'In month:'+month+'. Your goal is to read '+res.target+' books. you have already read '+res.already_done, key:month}
						//this.shiyan2.push(this.addv)
						this.activities[month-1] = this.addv
						//console.log(this.activities)
					}
					if(typeof(res.data.target) != undefined){
						this.addv = {content:'In month:'+month+'. Your goal is to read '+res.data.target+' books. you have already read '+res.data.already_done, key:month}
						//this.shiyan2.push(this.addv)
						this.activities[month-1] = this.addv
					}
					
				}).catch(error => {
					console.log(error)
				});
			}
		}
	},
	mounted: function () {
		this.$refs.PerinfoFormRef.validate(async valid => {
			if (!valid) { return }
			getperinfodata().then(result =>{
				// console.log(result)
				this.PerinfoForm.username = result.username
				this.PerinfoForm.email = result.email
				this.PerinfoForm.regisdate = result.join_date
				this.PerinfoForm.date_of_birth = result.date_of_birth
				this.PerinfoForm.gender = result.gender
				this.PerinfoForm.id = result.id
			}).catch((error)=>{
				console.log(error);
			})
		}),
		
		// Get collection in advance
		getCollectionmultdata().then(res=>{
			//console.log(res)
			this.collections = res
			this.value = this.collections[0].name
			this.getCollectionNames(res)   // Sort out the collection names returned by the API
			this.getCollectionBooks(this.collections[0].id) // default select first collection
			this.recollectionForm.new_name = this.collections[0].name
			this.recollectionForm.collection_id = this.collections[0].id
			this.delecollectionform.collection_id = this.collections[0].id
		})
		.catch(error => {
			console.log(error)
		})
	},
	
	// get current goal
	created() {
		this.getGoal()
		console.log(this.activities[0])
		this.sortBykey(this.activities, 'age')
		if(this.token_log){
			getCollectionmultdata().then(res=>{
				console.log(res)
		
				for (let i=0;i<res.length;i++){
					let j=res[i].id
					let k=res[i].name
					this.options2.push({id:j,name:k})
				}
			}).catch(res=>{
				console.log(res)
			})
		
		}
	}
}
</script>

<style lang="less" scoped>
	// total
	body, html{
		height: 100%;
		overflow: hidden;
	}
	
	// header: The navigation bar
	.header{
		margin-bottom: 10px;
	}
	
	// The outermost div
	.wrap{
		text-align: center;
		position: absolute;
		height: 100%;
		width: 100%;
		//background: url(../assets/person2.png) no-repeat fixed;
		background-color: aliceblue;
		background-size: cover;
		background-origin: border-box;
		//opacity:0.75;
		overflow-y: auto;
	}
	
	// The outermost tab
	.content{
		width: 90%;		
		margin: auto;
	}
	
	// Personal information
	.person_information{
		margin-left: 60px;
	}
	
	.Per_info_title{
		margin-top: 30px;
		font: 34px bolder;
	}
	
	.el-input{
		width: 300px;
	}
	
	.Per_info{
		margin-top: 50px;
	}
	
	// collection	
	// Remove the floating
	.clearfix{
		*zoom: 1;    
	}
	
	.clearfix:after{
		content: "";
		display: block;
		clear: both;
	}
	
	.collection_head{
		margin-left: 10px;
		margin-top: 20px;
		float: left;
	}
	
	.collection_add,.collection_reset, .collection_dele {
		margin-top: 10px;
		float: left;
	}
	
	// create an new collection
	.collection_add_button{
		margin-top: 10px;
		margin-left: 80px;
	}
	
	.collection_add{
		margin-top: 10px;
	}
	
	.el-divider {
		margin-top: 50px;
	}
	
	.el-divider__text {
		font-size: 30px;
		background-color: aliceblue;
	}
	
	// reset collection name
	.collection_change_button{
		margin-top: 10px;
		margin-left: 90px;
	}
	
	// delete collection
	.collection_dele_button{
		margin-top: 10px;
		margin-left: 100px;
	}
	
	// Collection body, display diagram & Title
	.coll_wrap {
		margin-top: 30px;
		display: grid;
		grid-template-columns: repeat(5, 1fr);
	}
	
	.coll_content {
		margin: 10px 30px 30px 15px;
	}
	
	.img {
		width: 180px;
		height: 250px;
	}
	
	// goal detail in current year
	.history_goal_title{
		margin-left: 30px;
		font: 34px bolder;
		margin-top: 20px;
	}
	
	.history_goal{
		margin-top: 20px;
	}

</style>
