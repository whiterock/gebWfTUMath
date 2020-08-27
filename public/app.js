var app = new Vue({
  el: '#app',
  data: {
    sem: [],
    updated: 'some time ago',
    lvas: {},
    sem_selected: {},
    kind_selected: {
        'VO': true,
        'UE': true,
        'VU': true,
        'XY': true
    }
  },
  created: function() {
    fetch('data.json')
    .then(res => res.json())
    .then(res => {
      this.lvas = res.data;
      this.updated = res.updated;
      this.sem = res.sem;
      for (const val of this.sem) {
        Vue.set(this.sem_selected, val, true);
      }
    })
  },
  methods:{
    toggle_sem: function (sem_tt) {
      Vue.set(this.sem_selected, sem_tt, !this.sem_selected[sem_tt]);
      //this.sem_selected[sem_tt] = !this.sem_selected[sem_tt]
      this.$forceUpdate();
    },
    toggle_kind: function(kind_tt) {
      Vue.set(this.kind_selected, kind_tt, !this.kind_selected[kind_tt])
    }
  },
  computed:{
    lvas_filtered: function() {
      var result = {};
      for (const [key, value] of Object.entries(this.lvas)) {
        result[key] = value.filter(function(item) {
          if (item['kind'] in {'VO': true, 'VU': true, 'UE': true}) {
            return this.sem_selected[item['sem']] && this.kind_selected[item['kind']];
          } else {
            return this.sem_selected[item['sem']] && this.kind_selected['XY'];
          }
        }, this);
      }
      return result;
    }
  }
})