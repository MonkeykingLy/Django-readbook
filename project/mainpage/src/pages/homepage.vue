<!-- Written by Yangyu GAO -->
<template>
    <div id="app">
		<!-- header -->
        <div class="header">
            <Header></Header>
        </div>

        <div class="content">
            <!-- before login -->
            <Carousel v-if="token_log == null"></Carousel>
            <CardBook v-if="token_log == null"></CardBook>

			<!-- after login -->
            <div class="after-login">
                <el-row>
                    <el-col :span="6" v-if="token_log != null">
                        <div class="grid-content bg-purple">
                            <!-- left hand side: current goal -->
                            <Goal></Goal>
                            <Rec></Rec>
                        </div>
                    </el-col>

                    <el-col :span="18" v-if="token_log != null">
                        <div class="grid-content bg-purple">
                            <!-- right hand side: collections -->
                            <BriefCollections></BriefCollections>
                        </div>
                    </el-col>
                </el-row>
            </div>
        </div>

		<!-- Footer -->
        <div class="footer">
            <Footer></Footer>
        </div>
    </div>
</template>

<script>
    import Header from '../components/homepage_components/homepage_header.vue'
    import Carousel from '../components/homepage_components/homepage_carousel.vue'
    import CardBook from '../components/homepage_components/mainpagebooks.vue'
    import Footer from '../components/homepage_components/homepage_footer.vue'
    import Goal from '../components/homepage_components/homepage_goal.vue'
    import Rec from '../components/homepage_components/homepage_rec.vue'
    import BriefCollections from '../components/homepage_components/homepage_collections.vue'

    export default {
        data() {
          return {
              token_log: localStorage.getItem('token')
          }
        },
	
		/* components used in homepage */
        components:{
            Header, Carousel, CardBook, Footer, Goal, Rec, BriefCollections,
        },

        name: 'App'
    }
</script>

<style lang="less" scoped>
    html, body {
        height: 100%;
		width: 100%;
        margin: 0;
        padding: 0;
    }

    #app {
        font-family: 'Avenir', Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        position: absolute;
		width: 100%;
        flex-direction: column;
        background: aliceblue;
    }

    .header {
        height: 60px;
    }

    .content {
        flex: 1;
		min-height: calc(100vh - 135px);
    }

    .footer {
        width: 100%;
        height: 60px;
    }

    .grid-content {
        min-height: 36px;
        height: 100%;
    }
</style>