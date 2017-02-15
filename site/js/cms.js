const app = new Vue({
  el: '#app',
  data: {
    category: 'lyrics',
    docs: [],
    workingCopy: null
  },
  mounted() {
    console.log('mounted')
    axios.get(`/api/category/${this.category}/`).then(res => {
      console.log(res)
      this.docs = res.data
    })
  }
})
