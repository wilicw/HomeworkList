<template>
  <el-form label-position="top">
    <el-form-item label="標題">
      <el-input v-model="text"></el-input>
    </el-form-item>
    <el-form-item label="標籤">
      <el-select v-model="tag" placeholder="選擇作業標籤">
        <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="科目">
      <el-select v-model="subject" placeholder="選擇作業科目">
        <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id"></el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="期限">
      <el-date-picker
        type="date"
        v-model="time"
        placeholder="選擇日期">
      </el-date-picker>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submit">儲存</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import api from '@/api'
import _ from 'lodash'
export default {
  name: 'Edit',
  props: ['tags', 'subjects', 'id', 'lists'],
  data: () => ({
    text: '',
    tag: '',
    subject: '',
    time: ''
  }),
  mounted () {
    this.preset()
  },
  watch: {
    id: function (val) {
      console.log(val)
      this.preset()
    }
  },
  methods: {
    preset: function () {
      const id = this.id
      if (!id) {
        return null
      }
      const item = _.findLast(this.lists, (o) => o.id === id)
      this.text = item.text
      this.tag = item.tag
      this.subject = item.subject
      this.time = new Date(item.time)
    },
    submit: async function () {
      const user = JSON.parse(window.localStorage.getItem('user'))
      if (this.time && this.text && user && this.tag && this.subject) {
        const d = this.time
        const time = (new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime())
        let response
        if (this.id) {
          response = (await api.postHw(this.id, this.text, this.tag, this.subject, time, user.username, user.password)).data
        } else {
          response = (await api.putHw(this.text, this.tag, this.subject, time, user.username, user.password)).data
        }
        if (response.error) {
          this.$message({
            message: response.error,
            type: 'error'
          })
        } else {
          this.$message({
            message: '',
            type: 'success'
          })
        }
      } else {
        this.$message({
          message: '資料缺失',
          type: 'warning'
        })
      }
    }
  }
}
</script>
