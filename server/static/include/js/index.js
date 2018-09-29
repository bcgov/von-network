function fetch_validator_status (callb) {
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

function display_validator_status(status, evt, statusCode) {
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
        console.log(body.children[i]);
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

    var txns = [],
      tx_avgs = info.Metrics['average-per-second'],
      tx_counts = info.Metrics['transaction-count']
    txns.push('' + tx_counts.config + ' config')
    txns.push('' + tx_counts.ledger + ' ledger')
    txns.push('' + tx_counts.pool + ' pool')
    txns.push('' + tx_avgs['read-transactions'] + '/s read')
    txns.push('' + tx_avgs['write-transactions'] + '/s write')
    div.querySelector('.nodeval-txns').innerText = txns.join(', ')

    div.classList.remove('template')
  }
}

$(function () {
  fetch_validator_status(display_validator_status)

  // override forms to submit json
  $('form').submit(function (event) {
    const form = this
    event.preventDefault()

    // serialize data as json
    const data = {}
    $(form).serializeArray().forEach(input => {
      if (input.value) data[input.name] = input.value
    })

    $(form).find('button[type=submit]').toggleClass('loading')

    $.ajax({
      method: 'POST',
      url: $(form).attr('action'),
      data: JSON.stringify(data),
      contentType: 'application/json'
    }).done(function (response) {
      $(form).find('button[type=submit]').toggleClass('loading')
      $('#seed').text(response.seed)
      $('#did').text(response.did)
      $('#verkey').text(response.verkey)
      $('.register-result').show().css('display', 'block')
    })
  })
})
