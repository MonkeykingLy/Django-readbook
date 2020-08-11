<template>
    <div id="app">
        <router-view v-if="isRouterAlive"/>
    </div>
</template>

<script>
    export default {

        components:{

        },
		provide(){
			return{
				reload: this.reload
			};
		},
		data(){
			return{
				style: '',
				isRouterAlive: true
			};
		},
		methods: {
			reload() {
				this.isRouterAlive = false;
				this.$nextTick(function() {
					this.isRouterAlive = true;
				});
			}
		}
    }
</script>

<!-- The introduction of stylus -->
<style lang="stylus" rel="stylesheet/stylus">
</style>
