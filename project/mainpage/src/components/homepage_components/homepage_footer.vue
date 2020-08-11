<!-- Written by Yangyu GAO -->
<template>
    <div class="footer">
		<div class="text">
			<span>UNSW COMP9900 Group Project</span>
			<span class="footer-divider"> | </span>
            <span>©2020-2021</span>
		</div>
        <div class="icon">
            <!-- click jump to github page -->
            <img src="../../../github.png" title="click to view github page" height="32" width="32" @click="goGit" alt/>
        </div>
        <div class="text">
            Group: <b>capstone project orchid malevolence</b>
        </div>
    </div>
</template>

<script>
    export default {
        name: "homepage_footer",
        
        methods: {
            goGit() {
                window.open("https://github.com/unsw-cse-capstone-project/capstone-project-orchid-malevolence",
                    "_blank")
            }
        }
    }
</script>

<style lang="less" scoped>
    .footer {
        padding-top: 15px;
        background: #99a9bf;
		justify-content: center;
        display: flex;
    }

	.text {
        margin: 15px 10px 0 10px;
        float: left;
	}

    .span {
        font-size: 22px;
    }
    
    .icon {
      float: left;
      margin-top: 5px;
      cursor:pointer;
    }
</style>