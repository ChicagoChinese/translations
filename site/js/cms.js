Vue.component('mde', {
  template: '#mde-template',
  props: ['value'],
  mounted() {
    let elem = this.$refs.textarea
    // this.mde = new SimpleMDE({element: elem})
  }
})

const app = new Vue({
  el: '#app',
  data: {
    category: 'lyrics',
    docs: [],
    isNew: false,
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
      let url, requestFn
      if (this.isNew) {
        url = `/api/category/${this.category}/`
        requestFn = axios.post
      } else {
        url = `/api/translation/${this.category}-${payload.slug}/`
        requestFn = axios.put
      }
      requestFn(url, payload).then(res => {
        if (res.status === 200 && this.isNew) {
          this.isNew = false
          this.workingCopy = res.data
          this.updateDocs()
        }
        if (res.status !== 200) {
          console.log('Error:', res.data)
        }
      })
    },
    updateDocs() {
      axios.get(`/api/category/${this.category}/`).then(res => {
        this.docs = res.data
      })
    },
    newDoc() {
      this.$el.querySelector('input[name=slug]').focus()
      this.workingCopy = {}
      this.isNew = true
    }
  }
})


function getFormPayload(form) {
  let formData = new FormData(form)
  let payload = {}
  for (let [k, v] of formData.entries()) {
    if (v !== '') {
      payload[k] = v
    }
  }
  return payload
}
