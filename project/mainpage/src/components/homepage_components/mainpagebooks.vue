<!-- Written by Yangyu GAO -->
<template>
    <div id="app1">
        <el-divider content-position="center" class="divider">Today's Popular</el-divider>
        <el-row :gutter="30" type="flex" justify="center">
            <el-col :span="4" v-for="item in books" :key="item.imageLink">
                <el-card :body-style="{ padding: '0px' }">
                    <div class="bottom">
                        <!-- Hover part: put cursor on the book image show details -->
                        <el-popover
                                placement="right"
                                width="400"
                                trigger="hover">
                            <div>
                                <b>{{item.title}}</b>
                                <el-rate
                                        v-model="item.avg_rating"
                                        disabled
                                        show-score
                                        text-color="#ff9900"
                                        score-template="{value}">
                                </el-rate>
                                {{item.description}}
                            </div>
                            <img :src="item.imageLink" class="image" alt slot="reference"/>
                        </el-popover>
                        <el-button class="book-detail" @click="jump_one_book(item)">More Details</el-button>
                        <!-- End Hover -->
                    </div>
                </el-card>
            </el-col>
        </el-row>
    </div>
</template>

<script>
    export default {
        name: "mainpagebooks",
        data() {
            return {
                currentDate: new Date(),
                books: []
            };
        },
      methods:{
          jump_one_book(value) {
              console.log(value)
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
      },

      mounted() {
          this.$axios({
              method: 'get',
              url: 'http://127.0.0.1:8000/api/mainpagerec/',
              // data: this.loginForm
          }).then(res => {
              let len = res.data.length
              for(let i = 0; i < len; i++) {
                  res.data[i].avg_rating = parseInt(res.data[i].avg_rating)
                  let des = res.data[i].description
                  if(des.length > 200) {
                      res.data[i].description = res.data[i].description.slice(0, 200) + "..."
                  }
                  this.books.push(res.data[i])
              }
          }).catch(error => {
              console.log(error)
          });
      }
    }
</script>

<style lang="less" scoped>
    .bottom {
        margin-top: 13px;
        line-height: 12px;
    }

    .button {
        padding: 0;
        /*float: center;*/
    }

    .el-row {
        margin: 40px 0 40px 0;
        text-align:center;
        width: 100%;
    }

    .el-card {
        height: 360px;
        width: 200px;
        /*margin-left: 20px;*/
    }

    .image {
        /*margin-top: 13.5px;*/
        width: 175px;
        height: 265px;
    }

    .el-divider {
        margin-top: 50px;
    }

    .el-divider__text {
        font-size: 20px;
        background: aliceblue;
    }

    .book-detail {
        margin-top: 10px;
    }
</style>