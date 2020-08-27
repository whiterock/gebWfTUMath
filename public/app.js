var app = new Vue({
  el: '#app',
  data: {
    sem: 'Hello Vue!',
    updated: 'some days ago',
    lvas: {}
  },
  created: function() {
    fetch('data.json')
    .then(res => res.json())
    .then(res => {
      this.lvas = res.data;
      this.updated = res.updated;
      this.sem = res.sem;
    })
  },
})