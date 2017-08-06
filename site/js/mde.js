/*
Source: https://github.com/F-loat/vue-simplemde/blob/master/markdown-editor.vue
*/
Vue.component('mde', {
  template: '#mde-template',
  props: ['value'],
  mounted() {
    this.mde = new SimpleMDE({
      element: this.$el,
      initialValue: this.value
    })
    // Send changes up to the component that is bound to the input event.
    this.mde.codemirror.on('change', () => {
      this.$emit('input', this.mde.value())
    })
  },
  watch: {
    value: function(newVal) {
      if (newVal !== this.mde.value()) {
        this.mde.value(newVal)
      }
    }
  }
})
