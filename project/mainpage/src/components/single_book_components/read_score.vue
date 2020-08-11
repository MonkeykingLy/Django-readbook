
<template>
	<div class="read_score">
		<span class="span1" style="font-size: 14px">Website average rating</span>
		<span class="score">{{average}}</span>
		<el-rate
						class="rate"
						v-model="average"
						disabled
						text-color="#ff9900"
						score-template="{average}">
		</el-rate>

		<ul>
			<li>5 star<el-progress class="percentage"  :percentage="this.rating_list.five"></el-progress></li>
			<li>4 star<el-progress class="percentage"  :percentage="this.rating_list.four"></el-progress></li>
			<li>3 star<el-progress class="percentage"  :percentage="this.rating_list.three"></el-progress></li>
			<li>2 star<el-progress class="percentage"  :percentage="this.rating_list.two"></el-progress></li>
			<li>1 star<el-progress class="percentage"  :percentage="this.rating_list.one"></el-progress></li>
		</ul>



		<span class="span3"> {{this.read}} people have read this book</span>

	</div>

</template>

<script>
// import { getSingleBookmultdata} from '../../network/requests'
export default {
	name: 'read_score',
	data () {
		return {
			token_log: localStorage.getItem('token'),
			average: 0,
			number: Number(0),
			book_id: String,
			value: 0,
			books: [],
			collections: [],
			receive_from_rating: 0,
			TotalCount: '',
			isShow: true,
			read:0,
			rating_list: {
				five: 0,
				four: 0,
				three: 0,
				two: 0,
				one: 0,
				read:0

			},
			count: 100,


		}
	},
	props: {
		res: Object,
		default: {}
	},
	methods:{
		init(val){
			console.log(val)
			this.read=val.rating_analyse.how_many_user_read
			this.average = val.averageScore
			this.book_id = val.book_id
			this.TotalCount = val.TotalCount
			this.rating_list.five = parseFloat((val.rating_analyse.five * 100).toFixed(1))
			this.rating_list.four = parseFloat((val.rating_analyse.four * 100).toFixed(1))
			this.rating_list.three = parseFloat((val.rating_analyse.three * 100).toFixed(1))
			this.rating_list.two = parseFloat((val.rating_analyse.two * 100).toFixed(1))
			this.rating_list.one = parseFloat((val.rating_analyse.one * 100).toFixed(1))
		},
	},

	// request method page initial and get average score of this book
	updated () {
		console.log(this.res.rating_analyse)
		this.average = this.res.averageScore
		this.book_id = this.res.book_id
		this.TotalCount = this.res.TotalCount
		this.read=this.res.rating_analyse.how_many_user_read
		this.rating_list.five = parseFloat((this.res.rating_analyse.five * 100).toFixed(1))
		this.rating_list.four = parseFloat((this.res.rating_analyse.four * 100).toFixed(1))
		this.rating_list.three = parseFloat((this.res.rating_analyse.three * 100).toFixed(1))
		this.rating_list.two = parseFloat((this.res.rating_analyse.two * 100).toFixed(1))
		this.rating_list.one = parseFloat((this.res.rating_analyse.one * 100).toFixed(1))
		console.log(this.rating_list)


	}
}


</script>
<style lang="less" scoped>

	.read_score {
		position: absolute;
		float: right;
		width: 260px;

	}

	span {
		display: block;
		font-size: 12px;
	}
	li{
		list-style: none;
		color: gray;
	}
	ul{
		padding: 0;
		color: gray;
	}
	.percentage{
		width: 70%;
		display: inline-block;
		margin-left: 10px;
	}
	/deep/ .el-rate__text{
		font-size: 20px;
	}
	.score{
		display: inline-block;
		margin: 0 5px 0 0;
		/*margin-right: 10px;*/
		font-size: 18px;
		color: #F7BA2A;
		vertical-align: top;

	}
	.rate{
		display: inline-block;
		/*vertical-align: top;*/

	}
	/deep/ .el-progress-bar{
		width: 90%;
	}
	.span1{
		margin-bottom: 5px;
	}
	.span3{
		font-size: 14px;

	}
</style>

