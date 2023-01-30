Vue.filter(
  'concat',
  function (values) {
    return (values || []).join(", ");
  }
);

Vue.filter(
  'format_time',
  function (value) {
    return new Date(value * 1000).toLocaleString();
  }
);

const INDY_TXN_TYPES = {
  "0": "NODE",
  "1": "NYM",
  "3": "GET_TXN",
  "4": "TXN_AUTHOR_AGREEMENT",
  "5": "TXN_AUTHOR_AGREEMENT_AML",
  "6": "GET_TXN_AUTHOR_AGREEMENT",
  "7": "GET_TXN_AUTHOR_AGREEMENT_AML",
  "8": "DISABLE_ALL_TXN_AUTHR_AGRMTS",
  "100": "ATTRIB",
  "101": "SCHEMA",
  "102": "CRED_DEF",
  "103": "DISCLO",
  "104": "GET_ATTR",
  "105": "GET_NYM",
  "107": "GET_SCHEMA",
  "108": "GET_CLAIM_DEF",
  "109": "POOL_UPGRADE",
  "110": "NODE_UPGRADE",
  "111": "POOL_CONFIG",
  "112": "CHANGE_KEY",
  "113": "REVOC_REG_DEF",
  "114": "REVOC_REG_ENTRY",
  "115": "GET_REVOC_REG_DEF",
  "116": "GET_REVOC_REG",
  "117": "GET_REVOC_REG_DELTA",
  "118": "POOL_RESTART",
  "119": "VALIDATOR_INFO",
  "120": "AUTH_RULE",
  "121": "GET_AUTH_RULE",
  "122": "AUTH_RULES"
}

const INDY_ROLE_TYPES = {
  "0": "TRUSTEE",
  "2": "STEWARD",
  "100": "TGB",
  "101": "ENDORSER",
}

const LEDGER_TXNS = [
  "0", "1", "4", "5", "100", "101", "102", "112", "113", "114", "120"
];

var app = new Vue({
  el: '#vue-ledger',
  data: {
    error: false,
    ident: null,
    ledger: 'domain',
    loaded: false,
    loading: false,
    nav: {
      loaded: false,
      total: 0
    },
    page: 1,
    page_size: 10,
    query: '',
    reqno: 0,
    txn_type: '',
    txns: [],
  },
  mounted: function () {
    if (window.history && history.pushState) {
      window.addEventListener('popstate', this.load.bind(this));
    }
    this.load();
  },
  computed: {
    haveFilter: function () {
      return this.query !== '' || this.txn_type !== '';
    },
    ledgerOptions: function () {
      return [
        { value: 'domain', label: 'Domain' },
        { value: 'pool', label: 'Pool' },
        { value: 'config', label: 'Config' },
      ];
    },
    txnTypeOptions: function () {
      var opts = [];
      for (var idx = 0; idx < LEDGER_TXNS.length; idx++) {
        var k = LEDGER_TXNS[idx];
        opts.push({ value: k, label: INDY_TXN_TYPES[k] });
      }
      opts.sort(function (a, b) { return parseInt(a.value) < parseInt(b.value); });
      return opts;
    }
  },
  methods: {
    load: function () {
      this.loadPageParams();
      this.loadPage();
    },
    txnType: function (val) {
      return INDY_TXN_TYPES[val] || val;
    },
    roleType: function (val) {
      return INDY_ROLE_TYPES[val] || val || '(none)';
    },
    loadPageParams: function () {
      var query = this.getPageParams();
      this.page = parseInt(query.page || 1, 10);
      this.page_size = parseInt(query.page_size || 10, 10);
      var path = document.location.pathname;
      path = path.replace(/^.*\/browse\//, '');
      var parts = path.split('/');
      this.ledger = parts[0] || 'domain';
      this.ident = parts[1] || null;
      this.query = query.query || '';
      this.txn_type = query.txn_type || '';
    },
    getPageParams: function () {
      // would be automatic but we're not using vue-router
      var q = document.location.search;
      var ret = {};
      if (q) {
        q = q.substring(1);
        var parts = q.split('&');
        for (var i = 0; i < parts.length; i++) {
          keyval = parts[i].split('=', 2);
          if (keyval.length == 2) {
            ret[decodeURIComponent(keyval[0])] = decodeURIComponent(keyval[1]);
          }
        }
      }
      return ret;
    },
    showEntry: function (ident) {
      this.navToPage(ident);
    },
    showLedger: function (value) {
      this.ledger = value;
      this.navToPage(null, { page: 1 });
    },
    updateLedger: function () {
      this.navToPage(null, { page: 1, query: this.query, txn_type: this.txn_type });
    },
    updateQuery: function (q) {
      this.query = q;
      this.updateLedger();
    },
    clearFilter: function () {
      this.navToPage(null, { page: 1, query: '', txn_type: '' });
    },
    entryUrl: function (ident) {
      var url = '/browse/' + this.ledger;
      if (ident) url += '/' + ident;
      return url;
    },
    navToPage: function (ident, params) {
      var url = this.entryUrl(ident);
      var query = this.getPageParams();
      if (params) {
        for (var k in params)
          query[k] = params[k];
      }
      url += encodeQueryString(query);
      if (window.history && history.pushState) {
        history.pushState(null, null, url);
        this.loadPageParams();
        this.loadPage();
      } else {
        document.location = url;
      }
    },
    loadPage: function () {
      this.loading = true;
      var url = '/ledger/' + encodeURIComponent(this.ledger)
      var ident = this.ident;
      if (ident)
        url += '/' + encodeURIComponent(this.ident);
      else
        url += encodeQueryString({ page: this.page, page_size: this.page_size, query: this.query, type: this.txn_type });
      var self = this;
      var reqno = ++this.reqno;
      fetch(url).then(
        function (res) {
          if (self.reqno == reqno && res.status) {
            if (res.status == 200) {
              res.json().then(function (result) {
                self.onReceive(result, ident);
              });
            } else {
              self.onError(res, ident);
            }
          }
        }
      ).catch(
        function (err) {
          if (self.reqno == reqno) {
            self.onError(err, ident);
          }
        }
      );
    },
    pageRange: function (data) {
      var display_range = 3;
      var current = null;
      var start = null;
      var last = null;
      var end = null;
      var ret = [];
      if (data) {
        current = data.page;
        last = Math.ceil(data.total / data.page_size);
        end = Math.min(Math.max(display_range * 2 + 1, current + display_range), last);
        start = Math.max(1, Math.min(current - display_range, last - display_range * 2));
      } else {
        current = this.page;
        end = last = this.page;
        start = Math.max(1, current - display_range);
      }
      if (start > 1) {
        ret.push({
          index: 1,
          link: true
        });
        if (start > 2) {
          ret.push({
            text: "...",
          });
          start++;
        }
      }
      for (var i = start; i <= end; i++) {
        ret.push(
          {
            active: i == current,
            index: i,
            link: true
          }
        );
      }
      if (last > end) {
        if (last > end + 1) {
          ret.pop();
          ret.push({
            text: "...",
          });
        }
        ret.push({
          index: last,
          link: true
        });
      }
      return ret;
    },
    toggleData: function (index) {
      this.txns[index].expanded = !this.txns[index].expanded;
    },
    onReceive: function (data, ident) {
      if (ident) {
        this.nav = { loaded: false, ident: true };
        this.loadTxns([data]);
      } else {
        var pages = this.pageRange(data);
        var last = pages.length ? pages[pages.length - 1].index : data.page;
        this.nav = {
          loaded: true,
          first: data.first_index,
          last: data.last_index,
          total: data.total,
          has_prev: data.page > 1,
          has_next: data.page < last,
          pages: pages,
        };
        this.loadTxns(data.results);
      }
      this.error = false;
      this.loaded = true;
      this.loading = false;
    },
    loadTxns: function (results) {
      var txns = [];
      for (var idx = 0; idx < results.length; idx++) {
        var wrapper = results[idx];
        var txn = {
          index: idx,
          wrapper: wrapper,
          auditPath: wrapper.auditPath,
          reqSignature: wrapper.reqSignature,
          rootHash: wrapper.rootHash,
          txn: wrapper.txn,
          txnMetadata: wrapper.txnMetadata,
          data: wrapper.txn.data,
          json: JSON.stringify(wrapper, null, 2),
          expanded: false
        };
        txns.push(txn);
      }
      this.txns = txns;
    },
    onError: function (res, ident) {
      var err = "Error loading transaction data.";
      if (ident) {
        if (res && res.status == 404) err = 'Transaction not found';
        this.nav = { loaded: false, ident: true };
      } else {
        if (res && res.status == 404) err = 'Page not found';
        this.nav = {
          loaded: true,
          has_prev: this.page > 1,
          has_next: false,
          pages: this.pageRange()
        };
      }
      this.error = err;
      this.loaded = false;
      this.loading = false;
    },
    gotoPage: function (page) {
      this.navToPage(null, { page: page });
    },
    prevPage: function () {
      this.gotoPage(Math.max(1, this.page - 1));
    },
    nextPage: function () {
      this.gotoPage(this.page + 1);
    }
  }
});

