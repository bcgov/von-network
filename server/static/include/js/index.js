var statusTimeout = null;
var statusLoaded = false;

function updateStatus() {
  if(statusTimeout) clearTimeout(statusTimeout);
  fetchValidatorStatus(function(result) {
    displayValidatorStatus(result);
    statusTimeout = setTimeout(updateStatus, 60000);
  });
}

function fetchValidatorStatus (callb) {
  var oReq = new XMLHttpRequest()
  oReq.addEventListener('load', function (evt) {
    callb(oReq.response, evt, oReq.status)
  })
  oReq.addEventListener('error', function (evt) {
    callb(null, evt, oReq.status)
  })
  oReq.responseType = 'json'
  oReq.open('GET', './status')
  oReq.send()
}

function displayValidatorStatus(status, evt, statusCode) {
  var panel = document.querySelector('.panel-node-status')
  var load = panel && panel.querySelector('.loading')
  var errPanel = panel && panel.querySelector('.error')
  var notReadyPanel = panel && panel.querySelector('.not-ready')
  var notReady = statusCode == 503;
  var err = !notReady && !Array.isArray(status);
  if (load) load.style.display = 'none'

  if (notReadyPanel) notReadyPanel.style.display = notReady ? null : 'none';
  if (errPanel) errPanel.style.display = err ? null : 'none';

  if (!panel) return
  var tpl = panel.querySelector('.node-status.template')
  if(tpl) {
    var body = tpl.parentNode;
    for(var i = body.children.length-1; i >= 0; i--) {
      if(body.children[i].classList.contains('node-status') && body.children[i] != tpl) {
        body.removeChild(body.children[i]);
      }
    }
  }
  if (!tpl || notReady || err) return

  for (var idx = 0; idx < status.length; idx++) {
    var node = status[idx],
        info = node.Node_info;
    var div = tpl.cloneNode(true)
    tpl.parentNode.appendChild(div)
    div.querySelector('.nodeval-name').innerText = info.Name
    div.querySelector('.nodeval-did').innerText = info.did
    var state = node.state
    if (!state) state = 'unknown'
    if (!node.enabled) state += ' (disabled)'
    div.querySelector('.nodeval-state').innerText = state
    div.querySelector('.nodeval-indyver').innerText = (node.software || node.Software || {})['indy-node'] || '?'

    var upt = info.Metrics.uptime,
      upt_s = upt % 60,
      upt_m = Math.floor(upt % 3600 / 60),
      upt_h = Math.floor(upt % 86400 / 3600),
      upt_d = Math.floor(upt / 86400),
      upt_parts = []
    if (upt_d) { upt_parts.push('' + upt_d + ' days') }
    if (upt_h || upt_parts.length) { upt_parts.push('' + upt_h + ' hours') }
    if (upt_m || upt_parts.length) { upt_parts.push('' + upt_m + ' minutes') }
    upt_parts.push('' + upt_s + ' seconds')
    div.querySelector('.nodeval-uptime').innerText = upt_parts.join(', ')

    var unreach = div.querySelector('.node-unreach')
    if (node.Pool_info.Unreachable_nodes_count) {
      div.querySelector('.nodeval-unreach').innerText = node.Pool_info.Unreachable_nodes.join(', ')
    } else {
      unreach.style.display = 'none'
    }

    var progress = node.Pool_info.Reachable_nodes_count / node.Pool_info.Total_nodes_count;
    var progressCircle = div.querySelector('.progress-circle');
    if(progressCircle) {
      var max = progressCircle.getAttribute('stroke-dasharray');
      if(max) {
        progressCircle.style.strokeDashoffset = max * (1 - progress);
      }
    }

    var shorten = function(val) {
      if(typeof val === 'number') {
        if(val > 1000000) {
          return (val / 1000000).toPrecision(3) + 'M';
        }
        if(val > 1000) {
          return (val / 1000).toPrecision(3) + 'K';
        }
        if(Math.trunc(val) == val) {
          return val;
        }
        return val.toPrecision(3);
      }
      return val;
    }
    var txns = [],
      tx_avgs = info.Metrics['average-per-second'],
      tx_counts = info.Metrics['transaction-count']
    txns.push('' + shorten(tx_counts.config) + ' config')
    txns.push('' + shorten(tx_counts.ledger) + ' ledger')
    txns.push('' + shorten(tx_counts.pool) + ' pool')
    txns.push('' + shorten(tx_avgs['read-transactions']) + '/s read')
    txns.push('' + shorten(tx_avgs['write-transactions']) + '/s write')
    div.querySelector('.nodeval-txns').innerText = txns.join(', ')

    div.classList.remove('template')
  }
}

$(function () {
  updateStatus();
});

var app = new Vue({
  el: '#vue-register',
  data: {
    reg_info: {reg_type: 'seed', did: null, verkey: null, role: 'TRUST_ANCHOR', seed: null, alias: null},
    reg_error: null,
    reg_result: null,
    loading: false
  },
  computed: {
    role_options: function() {
      return [
        {value: 'TRUST_ANCHOR', label: 'Trust Anchor'}
      ];
    }
  },
  mounted: function() {
  },
  methods: {
    register: function() {
      this.loading = true;
      this.reg_error = null;
      this.reg_result = null;
      var self = this;
      var info = {role: this.reg_info.role, alias: this.reg_info.alias};
      if(this.reg_info.reg_type == 'seed') {
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
        }}).then(
          function(res) {
            if(res.status == 200) {
              res.json().then(function(result) {
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
          function(err) {
            self.reg_error = true;
            self.loading = false;
          }
        );
    }
  }
});
