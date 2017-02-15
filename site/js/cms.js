const app = new Vue({
  el: '#app',
  data: {
    category: 'lyrics',
    docs: [],
    workingCopy: {}
  },
  mounted() {
    axios.get(`/api/category/${this.category}/`).then(res => {
      this.docs = res.data
    })
  },
  methods: {
    isSelected(slug) {
      return slug === this.workingCopy.slug
    },
    choseDoc(slug) {
      axios.get(`/api/translation/${this.category}-${slug}/`).then(res => {
        this.workingCopy = res.data
      })
    },
    cancel() {
      this.workingCopy = {}
    },
    submit(evt) {
      console.log('submit')
    }
  }
})
