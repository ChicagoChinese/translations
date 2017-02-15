const app = new Vue({
  el: '#app',
  data: {
    category: 'lyrics',
    docs: [],
    workingCopy: null
  },
  mounted() {
    axios.get(`/api/category/${this.category}/`).then(res => {
      this.docs = res.data
    })
  },
  methods: {
    choseDoc(slug) {
      axios.get(`/api/translation/${this.category}-${slug}/`).then(res => {
        this.workingCopy = res.data
      })
    }
  }
})
