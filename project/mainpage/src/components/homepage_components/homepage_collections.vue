<!-- Written by Yangyu GAO -->
<template>
    <div class="collection">
        <div class="collection-head">
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

        <!-- get collections base on selection -->
        <div class="collection-body">
            <!-- divider, show collection's name -->
            <el-divider content-position="center">10 books recent added in {{value}}</el-divider>

            <!-- main part of collection: with image, title, rating, brief description and jump button -->
            <div class="wrap">
				<!-- show top-10 recent books -->
                <div class="content" v-for="item in books" :key="item.imageLink">
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
                        <img :src="item.imageLink" class="img" alt slot="reference"/>
                    </el-popover>
					<!-- click to jump -->
                    <el-button class="book-detail" @click="jump_one_book(item)">More Details</el-button>
                </div>
            </div>
		</div>
    </div>
</template>

<script>
    import {getCollectionmultdata} from '../../network/requests'

    export default {
        data() {
            return {
                books: [],       // current collection's books
                options: [],     // collections' content
                value: '',       // collection name
                collections: [], // result from api package
                item: '', // one book param
                visible: false,
            }
        },

        methods: {
            // check which collection is now selecting
            currentSel(selVal) {
                this.value = selVal;
                let obj = {}
                obj = this.options.find((item)=>{
                    return item.value === selVal;
                });
                this.getCollectionBooks(obj.key)
            },

            getCollectionNames(res) {
                const len = res.length
                let option
                for(let i = 0; i < len; i++) {
                    // get collections' name
                    option = {}
                    option["key"] = res[i].id
                    option["value"] = res[i].name
                    this.options.push(option)
                }
            },

            // get books from specific collection through collection id
            getCollectionBooks(col_id) {
                this.books = []  // refresh books' list

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
                    if(book["description"].length > 200) {
                      book["description"] = book["description"].slice(0, 200) + "..."
                    }
                    book["avg_rating"] = parseInt(obj.books[i].avg_rating)
                    this.books.push(book)
                }
                this.books = this.books.slice(0, 10)
            },

            jump_one_book(value) {
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
        },

        mounted() {
            getCollectionmultdata().then(res=>{
                this.collections = res
                this.value = this.collections[0].name
                this.getCollectionNames(res)   // return collection get from api
                this.getCollectionBooks(this.collections[0].id) // default select first collection
            })
            .catch(error => {
                console.log(error)
            });
        }
    }


</script>

<style lang="less" scoped>
    .collection {
        background-color: aliceblue;
        border-radius: 2px;
        border-color: bisque;
        margin: 0 auto;
        width: 100%;
        height: 100%;
    }

    .collection-head {
        padding-top: 60px;
        margin-right: 50px;
        text-align: right;
    }

    .wrap {
        margin-top: 30px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
    }

    .el-divider__text {
        font-size: 20px;
        background-color: aliceblue;
    }

    .content {
        margin: 10px 30px 30px 30px;
        width: 180px;
    }

    .img {
        width: 180px;
        height: 240px;
    }

    .book-detail {
        margin-top: 10px;
    }
</style>