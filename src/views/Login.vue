<template>
  <el-form label-position="top">
    <el-form-item label="帳號">
      <el-input v-model="username"></el-input>
    </el-form-item>
    <el-form-item label="密碼">
      <el-input v-model="password"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="save">儲存</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data: () => ({
    username: '',
    password: ''
  }),
  beforeMount () {
    let data = window.localStorage.getItem('user')
    if (data) {
      data = JSON.parse(data)
      this.username = data.username
      this.password = data.password
    }
  },
  methods: {
    save: function () {
      window.localStorage.setItem('user', JSON.stringify(
        {
          username: this.username,
          password: this.password
        }
      ))
      this.$message({
        message: '儲存成功',
        type: 'success'
      })
    }
  }
}
</script>
