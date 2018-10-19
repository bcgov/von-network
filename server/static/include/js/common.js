function encodeQueryString(query) {
  var ret = '';
  if(query) {
    var keys = [];
    for(var k in query) {
      keys.push(k);
    }
    keys.sort();
    if(keys.length) ret = '?';
    for(var i = 0; i < keys.length; i++) {
      if(i) ret += '&';
      ret += encodeURIComponent(keys[i]) + '=' + encodeURIComponent(query[keys[i]]);
    }
  }
  return ret;
}
