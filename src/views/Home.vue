<template>
<div>
  <div v-for="list in lists" :key="list.id">
    <el-card class="box-card">
      <p>{{ timeToString(list.time) }} <strong>{{ list.text }}</strong> <span v-if="admin" class="tool"><i @click="del(list.id)" class="el-icon-delete"></i> / <i @click="edit(list.id)" class="el-icon-edit"></i></span></p>
      <p>{{ findSubject(list.subject) }} {{ findTag(list.tag) }}</p>
    </el-card>
    <br>
  </div>
  <el-dialog title="修改" :visible.sync="dialog" width="80%">
    <Edit :tags="tags" :subjects="subjects" :id="id" :lists="lists"></Edit>
  </el-dialog>
</div>
</template>

<script>
import api from '@/api'
import _ from 'lodash'
import Edit from '@/views/Edit'
export default {
  name: 'Home',
  props: ['tags', 'subjects'],
  components: {
    Edit
  },
  data: () => ({
    dialog: false,
    lists: [],
    admin: null
  }),
  async beforeMount () {
    this.admin = window.localStorage.getItem('user')
    this.fetchData()
  },
  methods: {
    edit: function (id) {
      if (!this.admin) {
        return
      }
      this.dialog = true
      this.id = id
    },
    del: async function (id) {
      if (!this.admin) {
        return
      }
      this.$confirm('是否刪除', '警告', {
        confirmButtonText: '是',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const response = (await api.delHw(id, JSON.parse(this.admin).username, JSON.parse(this.admin).password)).data
        this.fetchData()
        if (response.error) {
          this.$message({
            message: response.error,
            type: 'error'
          })
        } else {
          this.$message({
            message: 'Success',
            type: 'success'
          })
        }
      })
    },
    fetchData: async function () {
      const today = (new Date(new Date().getFullYear(), new Date().getMonth(), new Date().getDate()).getTime())
      this.lists = _.sortBy((await api.getHw(today)).data, ['time'])
    },
    findSubject: function (id) {
      return _.findLast(this.subjects, (o) => o.id === id).name
    },
    findTag: function (id) {
      return _.findLast(this.tags, (o) => o.id === id).name
    },
    timeToString: function (time) {
      const d = new Date(time)
      return `${d.getMonth() + 1}/${d.getDate()}`
    }
  }
}
</script>

<style lang="sass">
  .box-card
    margin: 0
    width: 85vw
    max-width: 800px
  .tool
    float: right
</style>
