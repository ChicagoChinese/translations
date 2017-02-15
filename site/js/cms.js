const app = new Vue({
  el: '#app',
  data: {
    category: 'lyrics',
    docs: [],
    workingCopy: {}
  },
  mounted() {
    this.updateDocs()
  },
  computed: {
    submitButtonDisabled() {
      return Object.keys(this.workingCopy).length === 0
    }
  },
  methods: {
    isSelected(slug) {
      return slug === this.workingCopy.slug
    },
    choseCategory() {
      this.updateDocs()
      this.workingCopy = {}
    },
    choseDoc(slug) {
      axios.get(`/api/translation/${this.category}-${slug}/`).then(res => {
        this.workingCopy = res.data
      })
    },
    cancel() {
      // Form will revert to original values.
      this.workingCopy = Object.assign({}, this.workingCopy)
    },
    submit(evt) {
      let formData = new FormData(evt.target)
      let payload = {}
      for (let [k, v] of formData.entries()) {
        payload[k] = v
      }
      axios.put(`/api/translations/${this.category}-${slug}/`, payload).then(res => {
        console.log(res.data)
      })
    },
    updateDocs() {
      axios.get(`/api/category/${this.category}/`).then(res => {
        this.docs = res.data
      })
    }
  }
})
