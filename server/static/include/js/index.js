
var app = new Vue({
  el: '#vue-outer',
  data: {
    anonymous: true,
    init_error: null,
    ready: false,
    reg_info: { reg_type: 'seed', did: null, verkey: null, role: 'ENDORSER', seed: null, alias: null },
    reg_error: null,
    reg_result: null,
    register_new_dids: false,
    loading: false,
    status: null,
    syncing: false
  },
  computed: {
    role_options: function () {
      return [
        { value: 'ENDORSER', label: 'Endorser' }
      ];
    }
  },
  mounted: function () {
    this.fetchStatus();
  },
  methods: {
    fetchStatus: function () {
      var self = this;
      fetch('/status?validators=' + (this.ready ? '1' : '')).then(function (response) {
        if (response.ok) {
          response.json().then(function (result) {
            var prev_ready = self.ready;
            self.anonymous = result.anonymous;
            self.init_error = result.init_error;
            self.ready = result.ready;
            self.register_new_dids = result.register_new_dids;
            self.syncing = result.syncing;
            if (self.ready) {
              self.status = result.validators ? self.formatValidatorStatus(result.validators) : null;
              setTimeout(function () { self.fetchStatus(); }, prev_ready ? 60000 : 1000);
            } else {
              setTimeout(function () { self.fetchStatus(); }, 10000);
            }
          });
        }
      }).catch(
        function (err) {
          console.error("Error fetching server config:", err);
        }
      );
    },
    formatValidatorStatus: function (status) {
      var formatted = {
        err: !Array.isArray(status),
        rows: []
      };

      if (!formatted.err) {
        for (var idx = 0; idx < status.length; idx++) {
          var node = status[idx],
            info = node.Node_info;

          // Skip nodes with error condition
          if(node.error) {
            console.error(`Received error status for validator node ${info.Name}:`, node.error);
            continue;
          }

          var result = {};

          result.name = info.Name;
          result.did = info.did;
          result.state = node.state;
          if (!result.state && node.enabled)
            result.state = 'unknown';
          result.indy_version = (node.software || node.Software || {})['indy-node'] || '?';

          var upt = info.Metrics.uptime,
            upt_s = upt % 60,
            upt_m = Math.floor(upt % 3600 / 60),
            upt_h = Math.floor(upt % 86400 / 3600),
            upt_d = Math.floor(upt / 86400),
            upt_parts = []
          if (upt_d) { upt_parts.push('' + upt_d + ' days') };
          if (upt_h || upt_parts.length) { upt_parts.push('' + upt_h + ' hours') };
          if (upt_m || upt_parts.length) { upt_parts.push('' + upt_m + ' minutes') };
          upt_parts.push('' + upt_s + ' seconds');
          result.uptime = upt_parts.join(', ');

          if (node.Pool_info.Unreachable_nodes_count) {
            result.unreachable = node.Pool_info.Unreachable_nodes.join(', ');
          } else {
            result.unreachable = null;
          }

          result.progress = node.Pool_info.Reachable_nodes_count / node.Pool_info.Total_nodes_count;
          result.dash_array = 339.292;
          result.dash_offset = result.dash_array * (1 - result.progress);

          var shorten = function (val) {
            if (typeof val === 'number') {
              if (val > 1000000) {
                return (val / 1000000).toPrecision(3) + 'M';
              }
              if (val > 1000) {
                return (val / 1000).toPrecision(3) + 'K';
              }
              if (Math.trunc(val) == val) {
                return val;
              }
              return val.toPrecision(3);
            }
            return val;
          }
          var txns = [],
            tx_avgs = info.Metrics['average-per-second'],
            tx_counts = info.Metrics['transaction-count'];
          txns.push('' + shorten(tx_counts.config) + ' config');
          txns.push('' + shorten(tx_counts.ledger) + ' ledger');
          txns.push('' + shorten(tx_counts.pool) + ' pool');
          txns.push('' + shorten(tx_avgs['read-transactions']) + '/s read');
          txns.push('' + shorten(tx_avgs['write-transactions']) + '/s write');
          result.txns = txns.join(', ');

          formatted.rows.push(result);
        }
      }

      return formatted;
    },
    register: function () {
      this.loading = true;
      this.reg_error = null;
      this.reg_result = null;
      var self = this;
      var info = { role: this.reg_info.role, alias: this.reg_info.alias };
      if (this.reg_info.reg_type == 'seed') {
        info.did = this.reg_info.did;
        info.seed = this.reg_info.seed;
      } else {
        info.did = this.reg_info.did;
        info.verkey = this.reg_info.verkey;
      }
      fetch('/register', {
        method: 'POST',
        body: JSON.stringify(info),
        headers: {
          'Content-Type': 'application/json'
        }
      }).then(
        function (res) {
          if (res.status == 200) {
            res.json().then(function (result) {
              self.reg_result = result;
              self.loading = false;
            });
          } else {
            console.log(res);
            self.reg_error = true;
            self.loading = false;
          }
        }
      ).catch(
        function (err) {
          self.reg_error = true;
          self.loading = false;
        }
      );
    }
  }
});
