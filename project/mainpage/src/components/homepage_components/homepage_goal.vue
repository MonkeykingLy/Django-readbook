<!-- Written by Yangyu GAO -->
<template>
    <div class="goal mid" id="app_goal">
        <h3 class="title">{{ goal_title }}</h3>

		<!-- if not set goal yet -->
        <div v-if="this.goalStatus===0">
            <div class="text_part">
                <p class="sub-title">Set a monthly goal</p>
            </div>
            <div class="input-group">
                <!-- input format: number in range [0, 99] -->
                <el-input
                        placeholder="input a number"
                        v-model="textGoal"
                        oninput="value=value.replace(/\D|^0/g,'')"
                        maxLength='2'
                        clearable>
                </el-input>
                <el-button type="warning" plain @click="setGoal()" class="set-goal">Set Goal</el-button>
            </div>
        </div>
	
		<!-- if set goal -->
        <div v-else>
			<!-- if read book less than monthly goal -->
            <div class="text_part" v-if="Number(bookData[0].totalBook - bookData[0].read) > 0">
                <p>{{ bookData[0].read }} books completed</p>
                <p>{{ Number(bookData[0].totalBook - bookData[0].read) }} books need to be read</p>
            </div>

			<!-- if read book larger than monthly goal -->
			<div class="text_part" v-else>
				<p style="color: firebrick">Congratulate! You have complete your monthly goal.</p>
			</div>
			
			<!-- show goal progress by a progress bar -->
            <el-progress :text-inside="true" :show-text="false"
                         :stroke-width="26"
                         :percentage="bookData[0].totalBook===0 ? 100 :bookData[0].read/bookData[0].totalBook * 100"
                         class="process-bar">
            </el-progress>

            <!-- Click to reset goal, open a dialog window -->
            <el-button type="primary" plain @click="openResetGoal" class="reset-button">Reset Goal</el-button>
            
            <!-- dialog window, with format judge -->
            <el-dialog title="Reset Monthly Goal" :visible.sync="dialogFormVisible">
                <el-form :model="form" :rules="resetGoalRule" :ref="form" status-icon>
                    <el-form-item label="Set a new goal: " :label-width="formLabelWidth" prop="value">
                        <el-input v-model.number="form.value" autocomplete="off" minlength="1" maxlength="2"></el-input>
                    </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                    <!-- click to send reset goal data -->
                    <el-button @click="cancelGoal">Cancel</el-button>
                    <!-- click to  -->
                    <el-button type="primary" @click="resetGoal(form)">Confirm</el-button>
                </div>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    import {getCurGoal, postCurGoal} from "../../network/requests";

    /* get date */
    let now = new Date()
    let nowMonth = now.getMonth() + 1
    let nowYear = now.getFullYear()

    export default {
        name: 'homepage-goal',
        data() {
            let checkGoal = (rule, value, callback) => {
                const goalReg = /^\+?[1-9][0-9]*$/
                if (!value) {
                    this.$forceUpdate()
                    return callback(new Error('please input a number'))
                } else {
                    setTimeout(() => {
                        if (goalReg.test(value)) {
                            callback()
                        } else {
                            callback(new Error('please input a number in range [1,99]'))
                        }
                    }, 100)
                }
                
            }
            
            return {
                bookData: [{read: '', totalBook: ''}],
                goal_title: nowYear + "-" + nowMonth + " Reading Challenge",
                response: {},
                target: null,
                already_done: null,
                goalStatus: 0,  // 0: false, 1: true
                textGoal: '',
                dialogFormVisible: false,
                form: {
                    value: '',
                },
                formLabelWidth: '120px',
                resetGoalRule: {
                    value: [
                        {required: true, validator: checkGoal, trigger: 'blur'}
                    ]
                }
            }
        },

        methods: {
            openResetGoal() {
                this.dialogFormVisible = true
                this.$forceUpdate()
            },
            
            resetGoal(formName) {
                /* judge format */
                this.$refs[formName].validate(valid => {
                    if(valid) {
                        /* send input data to backend */
                        this.setGoal(this.form.value)

                        /* close window, reset input */
                        this.dialogFormVisible = false
                        this.form.value = ''
                    } else {
                        return false;
                    }
                })
            },
            
            /* close window, reset input */
            cancelGoal() {
                this.dialogFormVisible = false
                this.form.value = ''
                this.$forceUpdate()
            },

			/* get current user's monthly goal, if not yet set, change goalStatus to 0, else to 1 */
            getGoal() {
				let params = {year:nowYear,month:nowMonth}
                getCurGoal(params).then(res=>{
                    if(res.already_done === 0 && res.target === 0) {
                        this.goalStatus = 0
                    } else {
						this.goalStatus = 1
					}

                    this.bookData[0].read = res.already_done
                    this.bookData[0].totalBook = res.target
                }).catch(error => {
                    console.log(error)
                });
            },

			/* if no input, pop error window, end function */
            setGoal(value = this.textGoal) {
				if(value === '') {
                    this.$message.error('Please input a goal number.')
                    return
                }

                // if have input, send new data to server
                let data = {month_goal:{month:nowMonth,year:nowYear ,target:value}}
                postCurGoal(data).then(res=>{
                    this.goalStatus = 1
                    this.$forceUpdate()
                    this.$set(this.bookData[0], "read", res.already_done)
                    this.$set(this.bookData[0], "totalBook", value)
                }).catch(error => {
                    console.log(error)
                });
            }
        },

        created() {
            this.getGoal()
        },
    }
</script>

<style lang="less" scoped>
    .goal {
        margin: auto;
        height: 240px;
        width: 270px;
        border-style: solid;
        border-radius: 2px;
        border-color: bisque;
        background-color: ivory;
        padding-top: 30px;
    }

    .mid {
        margin-top: 60px;
    }

    .sub-title {
        margin-top: 10px;
    }

    .input-group {
        margin-top: 25px;
        float: left;
        height: 40px;
    }

    .el-input {
        margin: 5px 2px 0 2px;;
        width: 60%;
        float: left;
    }

    .set-goal {
        margin: 5px 2px 0 2px;
        height: 100%;
    }

    .el-progress {
        width: 230px;
        margin: 0 auto;
    }
    
    .reset-button {
		margin-top: 20px;
    }
</style>




