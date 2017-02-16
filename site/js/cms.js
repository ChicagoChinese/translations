Vue.component('mde', {
  template: '#mde-template',
  props: ['value'],
  mounted() {
    let elem = this.$refs.textarea
    this.mde = new SimpleMDE({element: elem})
    this.mde.codemirror.on('change', () => {
      elem.value = this.mde.value()
    })
  },
  watch: {
    value: function(newVal) {
      this.mde.value(newVal)
    }
  }
})

const ContentEdit = {
  template: '#content-edit-template',
  props: ['doc']
}

const MetadataEdit = {
  template: '#metadata-edit-template',
  props: ['doc']
}

const routes = [
  {path: '/', component: MetadataEdit},
  {path: '/content', component: ContentEdit}
]

const app = new Vue({
  el: '#app',
  data: {
    category: 'lyrics',
    docs: [],
    isNew: false,
    currentDoc: null,   // the selected doc
    workingDoc: {}      // connected to the form inputs
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
      return slug === this.workingDoc.slug
    },
    choseCategory() {
      this.updateDocs()
      this.currentDoc = null
      this.workingDoc = {}
    },
    choseDoc(slug) {
      axios.get(`/api/translation/${this.category}-${slug}/`).then(res => {
        this.currentDoc = res.data
        this.workingDoc = res.data
      })
    },
    cancel() {
      this.workingDoc = Object.assign({}, this.currentDoc)
    },
    submit(evt) {
      let payload = getPayload(this.workingDoc)
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
          this.currentDoc = res.data
          this.workingDoc = res.data
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
      this.currentDoc = null
      this.workingDoc = {}
      this.isNew = true
      this.$el.querySelector('input[name=slug]').focus()
    }
  }
})


function getPayload(doc) {
  let payload = Object.assign({}, doc)
  for (let key in payload) {
    let value = payload[key]
    if (value === '') {
      delete payload[key]
    }
  }
  return payload
}
