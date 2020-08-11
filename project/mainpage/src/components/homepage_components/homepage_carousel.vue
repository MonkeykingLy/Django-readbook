<!-- Written by Yangyu GAO -->
<template>
    <div class="block">
        <el-carousel trigger="click" height="900px">
            <el-carousel-item v-for="item in img_list" :key="item.url">
                <img :src='item.url' alt/>
            </el-carousel-item>
        </el-carousel>
    </div>
</template>

<script>
    export default {
        name: "carousel",
        data() {
            return {
                img_list: [
                    { url: require("../../img/carousel_imgs/pic0.jpg") },
                    { url: require("../../img/carousel_imgs/pic1.jpg") },
                    { url: require("../../img/carousel_imgs/pic2.jpg") }
                ]
            }
        }
    }
</script>

<style lang="less" scoped>
    .el-carousel__item h3 {
        color: #475669;
        font-size: 14px;
        opacity: 0.75;
        line-height: 150px;
        margin: 0;
    }

    .el-carousel__item:nth-child(2n) {
        background-color: #99a9bf;
    }

    .el-carousel__item:nth-child(2n+1) {
        background-color: #d3dce6;
    }

    img {
        width: 100%;
        height: 100%;
    }
</style>