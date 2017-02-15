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
      let payload = getFormPayload(evt.target)
      let url = `/api/translation/${this.category}-${payload.slug}/`
      axios.put(url, payload).then(res => {
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


function getFormPayload(form) {
  let formData = new FormData(form)
  let payload = {}
  for (let [k, v] of formData.entries()) {
    payload[k] = v
  }
  return payload
}
