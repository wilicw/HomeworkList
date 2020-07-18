<template>
  <el-container>
    <el-header>
      <p class="title">
        <span @click="$router.push('/')">聯絡簿</span>
        <i v-if="admin" @click="$router.push('/add')" class="add el-icon-plus"></i></p>
    </el-header>
    <el-main>
      <router-view :tags="dataTags" :subjects="dataSubjects"></router-view>
    </el-main>
  </el-container>
</template>

<script>
import api from '@/api'
export default {
  name: 'app',
  data: () => ({
    admin: false,
    dataTags: [],
    dataSubjects: []
  }),
  beforeMount () {
    this.admin = window.localStorage.getItem('user')
    this.fetchData()
  },
  methods: {
    fetchData: async function () {
      this.dataTags = (await api.getTags()).data
      this.dataSubjects = (await api.getSubjects()).data
    }
  }
}
</script>

<style scoped lang="sass">
  .add
    float: right
    color: #AAAAAA
  .title
    vertical-align: middle
    font-size: 1.5em
  .el-main
    margin: 0 auto
    max-width: 800px
    overflow: hide
</style>
