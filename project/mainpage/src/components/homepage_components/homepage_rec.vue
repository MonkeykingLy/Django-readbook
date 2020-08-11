<!-- Written by Yangyu GAO -->
<template>
    <div class="rec">
        <div class="rec-body">
            <strong>New Book Recommendations</strong>
            <el-button type="primary" plain class="rec-button" @click="jump_rec">Recommendation</el-button>
        </div>
    </div>
</template>

<script>
	export default {
		methods: {
			jump_rec() {
				this.$router.push('/recommendation')
			}
		}
	}
</script>

<style lang="less" scoped>
    .rec {
        margin-top: 50px;
    }

    .rec-body {
		border-color: bisque;
		background-color: ivory;
        margin: auto;
		border-style: solid;
        height: 200px;
        width: 270px;
        border-radius: 2px;
        //background: aqua;
        padding-top: 50px;
    }

    .rec-button {
        margin-top: 80px;
    }
</style>